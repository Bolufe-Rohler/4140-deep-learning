"""Run every lecture notebook from a fresh clone, the way a student would.

    python tools/verify.py                 # both modes, all lectures, assets from dist/
    python tools/verify.py --lecture L11   # one lecture
    python tools/verify.py --github        # assets from the published GitHub release

Modes:
  colab  the notebook alone in an empty folder: its first cell must clone the repo,
         fetch the assets and run (what happens in Colab)
  repo   the notebook inside a fresh clone (what happens on a student's laptop)
Commits only: uncommitted changes are not in the clone.
"""
import argparse
import os
import pathlib
import subprocess
import sys
import tempfile
import time

import nbformat
from nbclient import NotebookClient

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import course  # noqa: E402


def run(nb_path, cwd, env, timeout, repo_override=None):
    nb = nbformat.read(nb_path, as_version=4)
    if repo_override:
        for c in nb.cells:
            if course.SETUP_TAG in c.get("metadata", {}).get("tags", []):
                c.source = "\n".join(f'REPO = "{repo_override}"' if l.startswith("REPO = ") else l
                                     for l in c.source.splitlines())
    old = {k: os.environ.get(k) for k in env}
    os.environ.update(env)
    t0 = time.time()
    try:
        NotebookClient(nb, timeout=timeout, kernel_name="python3",
                       resources={"metadata": {"path": str(cwd)}}).execute()
        return True, time.time() - t0, ""
    except Exception as e:  # noqa: BLE001
        msg = str(e).strip().splitlines()
        return False, time.time() - t0, "\n      ".join(msg[-6:])
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lecture")
    ap.add_argument("--mode", choices=["colab", "repo", "both"], default="both")
    ap.add_argument("--github", action="store_true", help="use published release assets, not dist/")
    ap.add_argument("--timeout", type=int, default=1800, help="seconds per cell")
    a = ap.parse_args()

    m = course.load()
    env = {} if a.github else {"CS4140_ASSET_BASE": str(course.DIST.resolve())}
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        clone = tmp / "clone"
        subprocess.run(["git", "clone", "--quiet", str(course.ROOT), str(clone)], check=True)
        for lec in m["lectures"]:
            if a.lecture and a.lecture not in (lec["id"], course.folder(lec)):
                continue
            for nb in lec["notebooks"]:
                src = clone / "lectures" / course.folder(lec) / nb
                if not src.exists():
                    results.append((lec["id"], nb, "-", False, 0, "not committed"))
                    continue
                if a.mode in ("colab", "both"):
                    sim = tmp / f"colab_{lec['id']}_{src.stem}"
                    sim.mkdir()
                    ok, dt, err = run(src, sim, env, a.timeout, repo_override=str(clone))
                    results.append((lec["id"], nb, "colab", ok, dt, err))
                if a.mode in ("repo", "both"):
                    ok, dt, err = run(src, src.parent, env, a.timeout)
                    results.append((lec["id"], nb, "repo", ok, dt, err))
    print()
    for lid, nb, mode, ok, dt, err in results:
        print(f"{'PASS' if ok else 'FAIL'}  {lid}  {nb}  [{mode}]  {dt:.0f}s")
        if err:
            print(f"      {err}")
    sys.exit(0 if all(r[3] for r in results) else 1)


if __name__ == "__main__":
    main()
