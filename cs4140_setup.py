"""CS 4140 course helper.

Each lecture notebook calls fetch_assets() from its first cell. It downloads the
lecture's saved results, trained weights and data (kept outside git, in a GitHub
Release), checks them, and unpacks them next to the notebook. Run again, it does
nothing. You never need to call it yourself.
"""
import hashlib
import json
import os
import pathlib
import shutil
import sys
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent


def _manifest():
    return json.loads((ROOT / "course.json").read_text(encoding="utf-8"))


def _folder(lec):
    return f'{lec["id"]}_{lec["slug"]}'


def _find(manifest, name):
    for lec in manifest["lectures"]:
        if name in (_folder(lec), lec["id"]):
            return lec
    raise KeyError(f"No lecture called {name!r} in course.json")


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _asset_source(manifest, filename):
    # CS4140_ASSET_BASE lets the instructor test with a local folder before publishing.
    base = os.environ.get("CS4140_ASSET_BASE")
    if base:
        return base.rstrip("/") + "/" + filename
    g = manifest["github"]
    return (f'https://github.com/{g["owner"]}/{g["repo"]}/releases/download/'
            f'{manifest["assets_release"]}/{filename}')


def _download(src, dest, size):
    tmp = dest.with_suffix(dest.suffix + ".part")
    if os.path.isfile(src):
        shutil.copyfile(src, tmp)
    else:
        req = urllib.request.Request(src, headers={"User-Agent": "cs4140-setup"})
        mb = size / 2**20
        print(f"Downloading {dest.name} ({mb:.0f} MB) ...", end="", flush=True)
        done, next_mark = 0, 0.25
        with urllib.request.urlopen(req) as r, open(tmp, "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
                done += len(chunk)
                while size and next_mark <= 1.0 and done / size >= next_mark:
                    print(f" {int(next_mark * 100)}%", end="", flush=True)
                    next_mark += 0.25
        print()
    tmp.replace(dest)


def _extract(zpath, target):
    target = target.resolve()
    with zipfile.ZipFile(zpath) as z:
        for member in z.infolist():
            out = (target / member.filename).resolve()
            if target not in out.parents and out != target:
                raise RuntimeError(f"Unsafe path in {zpath.name}: {member.filename}")
            if member.is_dir():
                out.mkdir(parents=True, exist_ok=True)
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            with z.open(member) as src, open(out, "wb") as dst:
                shutil.copyfileobj(src, dst)


def fetch_assets(lecture):
    """Make sure this lecture's saved results, weights and data are in place."""
    manifest = _manifest()
    lec = _find(manifest, lecture)
    target = ROOT / "lectures" / _folder(lec)
    assets = lec.get("assets")
    if not assets:
        print("Ready. This lecture needs no extra files.")
        return target

    marker = target / ".assets_ok"
    if marker.is_file() and marker.read_text().strip() == assets["sha256"]:
        print("Ready. Saved results and data are already here.")
        return target

    cache = ROOT / ".cache"
    cache.mkdir(exist_ok=True)
    zpath = cache / assets["file"]
    if not (zpath.is_file() and _sha256(zpath) == assets["sha256"]):
        local = target / assets["file"]          # e.g. downloaded by hand from Moodle
        if local.is_file():
            shutil.copyfile(local, zpath)
        else:
            _download(_asset_source(manifest, assets["file"]), zpath, assets["size"])
    if _sha256(zpath) != assets["sha256"]:
        zpath.unlink()
        raise RuntimeError(f"{assets['file']} did not download correctly. Run the cell again.")

    _extract(zpath, target)
    marker.write_text(assets["sha256"])
    print(f"Ready. Saved results and data unpacked into {target.name}/")
    if "google.colab" in sys.modules:
        print("Tip: File → Save a copy in Drive keeps your own changes to this notebook.")
    return target
