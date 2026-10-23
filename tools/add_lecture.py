"""Turn a lecture's demo package into a lecture folder plus a release-asset zip.

    python tools/add_lecture.py PACKAGE.zip L11            # show the plan only
    python tools/add_lecture.py PACKAGE.zip L11 --apply    # do it

Sorting rules (override with --asset / --exclude / --keep, glob patterns on the
package's relative paths, e.g. --exclude "figures/**"):
  excluded   instructor-only or junk: deck_source/, figures/, make_figures*.py,
             __pycache__, .ipynb_checkpoints, __MACOSX, .DS_Store
  asset      weights and arrays (.pt .pth .npz .npy .pkl ...), any non-notebook
             file over 1 MiB, and every file in a folder holding over 200 files
             (photo datasets); small text files (README, CREDITS, LICENSE) stay in git
  git        everything else: notebooks, small JSON/CSV, scripts, READMEs

Assets go to dist/<folder>_assets.zip and their paths into .gitignore. Each
notebook gets a banner (Open in Colab badge) and the setup cell at the top.
"""
import argparse
import fnmatch
import hashlib
import pathlib
import shutil
import sys
import tempfile
import zipfile

import nbformat

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import course  # noqa: E402

EXCLUDE = ["deck_source/**", "figures/**", "make_figures*.py", "**/__pycache__/**",
           "**/.ipynb_checkpoints/**", "__MACOSX/**", "**/.DS_Store", ".DS_Store",
           "**/.assets_ok", "*.pptx"]
ASSET_EXT = {".pt", ".pth", ".ckpt", ".safetensors", ".npz", ".npy", ".pkl", ".pickle",
             ".h5", ".hdf5", ".bin", ".joblib", ".gz", ".ubyte", ".tar", ".zip"}
TEXT_KEEP = {".md", ".txt", ".cff"}
SMALL_TEXT = {".csv", ".tsv", ".json", ".yaml", ".yml", ".py", ".md", ".txt"}
BIG = 1 << 20          # 1 MiB
CROWDED = 200          # files in one folder


def match(path, patterns):
    for p in patterns:
        if fnmatch.fnmatch(path, p):
            return True
        if p.startswith("**/") and fnmatch.fnmatch(path, p[3:]):
            return True
    return False


def unpack(package, workdir):
    package = pathlib.Path(package)
    if package.is_dir():
        src = package
    else:
        with zipfile.ZipFile(package) as z:
            z.extractall(workdir)
        src = pathlib.Path(workdir)
    # A zip with a single top folder: use that folder as the package root.
    entries = [p for p in src.iterdir() if p.name not in ("__MACOSX", ".DS_Store")]
    while len(entries) == 1 and entries[0].is_dir():
        src = entries[0]
        entries = [p for p in src.iterdir() if p.name not in ("__MACOSX", ".DS_Store")]
    return src


def classify(src, extra_asset, extra_exclude, extra_keep):
    files = sorted(p.relative_to(src).as_posix() for p in src.rglob("*") if p.is_file())
    counts = {}
    for f in files:
        for parent in pathlib.PurePosixPath(f).parents:
            counts[parent.as_posix()] = counts.get(parent.as_posix(), 0) + 1
    crowded = {d for d, n in counts.items() if n > CROWDED and d != "."}

    plan = {}
    for f in files:
        p = src / f
        suffix = pathlib.PurePosixPath(f).suffix.lower()
        name = pathlib.PurePosixPath(f).name
        if match(f, extra_keep):
            plan[f] = "git"
        elif match(f, extra_exclude) or match(f, EXCLUDE):
            plan[f] = "excluded"
        elif match(f, extra_asset):
            plan[f] = "asset"
        elif suffix == ".ipynb":
            plan[f] = "git"
        elif suffix in ASSET_EXT or p.stat().st_size > BIG:
            plan[f] = "asset"
        elif (suffix in TEXT_KEEP or name.upper().startswith(("LICENSE", "LICENCE", "CREDITS", "README"))):
            plan[f] = "git"
        elif suffix not in SMALL_TEXT and any(parent.as_posix() in crowded
                                              for parent in pathlib.PurePosixPath(f).parents):
            plan[f] = "asset"
        else:
            plan[f] = "git"
    return plan


def ignore_paths(plan):
    """Smallest set of paths (folders where possible) covering every asset file."""
    assets = {f for f, k in plan.items() if k == "asset"}
    out = set()
    for f in sorted(assets):
        best = f
        for parent in pathlib.PurePosixPath(f).parents:
            d = parent.as_posix()
            if d == ".":
                break
            inside = [g for g in plan if g.startswith(d + "/")]
            if all(plan[g] in ("asset", "excluded") for g in inside):
                best = d + "/"
        out.add(best)
    return sorted(p for p in out if not any(p != q and q.endswith("/") and p.startswith(q) for q in out))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def add_cells(nb_path, m, lec):
    nb = nbformat.read(nb_path, as_version=4)
    nb.cells = [c for c in nb.cells
                if not set(c.get("metadata", {}).get("tags", [])) & {course.SETUP_TAG, course.BANNER_TAG}]
    banner = nbformat.v4.new_markdown_cell(course.banner_source(m, lec, nb_path.name),
                                           metadata={"tags": [course.BANNER_TAG]})
    setup = nbformat.v4.new_code_cell(course.setup_cell_source(m, lec),
                                      metadata={"tags": [course.SETUP_TAG]})
    nb.cells = [banner, setup] + nb.cells
    nb.metadata.setdefault("colab", {})["provenance"] = []
    nbformat.write(nb, nb_path)


def update_gitignore(folder, paths):
    gi = course.ROOT / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    begin, end = f"# >>> assets: {folder}", f"# <<< assets: {folder}"
    if begin in text:
        head, rest = text.split(begin, 1)
        text = head + rest.split(end, 1)[1].lstrip("\n")
    block = [begin] + [f"lectures/{folder}/{p}" for p in paths] + [end]
    gi.write_text(text.rstrip("\n") + "\n\n" + "\n".join(block) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("package")
    ap.add_argument("lecture", help="lecture id from course.json, e.g. L11")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--asset", action="append", default=[])
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--keep", action="append", default=[])
    ap.add_argument("--replace", action="store_true", help="clear the lecture folder first")
    a = ap.parse_args()

    m = course.load()
    lec = course.find(m, a.lecture)
    folder = course.folder(lec)
    with tempfile.TemporaryDirectory() as tmp:
        src = unpack(a.package, tmp)
        plan = classify(src, a.asset, a.exclude, a.keep)
        size = {k: sum((src / f).stat().st_size for f, kk in plan.items() if kk == k) for k in ("git", "asset", "excluded")}
        n = {k: sum(1 for kk in plan.values() if kk == k) for k in size}
        print(f"{folder}  (package root: {src.name})")
        for kind in ("git", "asset", "excluded"):
            print(f"\n== {kind}: {n[kind]} files, {size[kind] / 2**20:.1f} MiB")
            groups = {}
            for f, k in plan.items():
                if k == kind:
                    groups.setdefault(str(pathlib.PurePosixPath(f).parent), []).append(f)
            for d, fs in groups.items():
                if len(fs) > 6:
                    kib = sum((src / f).stat().st_size for f in fs) / 1024
                    print(f"   {d}/  {len(fs)} files ({kib:.0f} KiB)")
                else:
                    for f in fs:
                        print(f"   {f}  ({(src / f).stat().st_size / 1024:.0f} KiB)")
        big_git = [f for f, k in plan.items() if k == "git" and (src / f).stat().st_size > 5 * BIG]
        if big_git:
            print("\nWARNING: large files headed for git:", ", ".join(big_git))
        if not a.apply:
            print("\nPlan only. Re-run with --apply to write it.")
            return

        dest = course.ROOT / "lectures" / folder
        if a.replace and dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True, exist_ok=True)
        for f, k in plan.items():
            if k == "git":
                (dest / f).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src / f, dest / f)

        assets = [f for f, k in plan.items() if k == "asset"]
        lec["assets"] = None
        if assets:
            course.DIST.mkdir(exist_ok=True)
            zname = f"{folder}_assets.zip"
            zpath = course.DIST / zname
            with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                for f in assets:
                    info = zipfile.ZipInfo(f, date_time=(2027, 1, 1, 0, 0, 0))   # stable checksum
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o644 << 16
                    z.writestr(info, (src / f).read_bytes())
            lec["assets"] = {"file": zname, "sha256": sha256(zpath), "size": zpath.stat().st_size}
            update_gitignore(folder, ignore_paths(plan))
            print(f"\nAssets: dist/{zname} ({zpath.stat().st_size / 2**20:.1f} MiB)")

        lec["notebooks"] = sorted(f for f, k in plan.items() if k == "git" and f.endswith(".ipynb") and "/" not in f)
        for nb in lec["notebooks"]:
            add_cells(dest / nb, m, lec)
        course.save(m)
        print(f"Wrote lectures/{folder}/ with notebooks: {', '.join(lec['notebooks']) or 'none'}")


if __name__ == "__main__":
    main()
