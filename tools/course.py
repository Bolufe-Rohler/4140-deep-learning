"""Shared helpers for the maintenance tools (instructor side)."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "course.json"
DIST = ROOT / "dist"

SETUP_TAG = "cs4140-setup"
BANNER_TAG = "cs4140-banner"
COLAB_BADGE = "https://colab.research.google.com/assets/colab-badge.svg"


def load():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save(m):
    # One lecture per line keeps diffs readable.
    lines = ["{"]
    keys = [k for k in m if k != "lectures"]
    for k in keys:
        lines.append(f"  {json.dumps(k)}: {json.dumps(m[k], ensure_ascii=False)},")
    lines.append('  "lectures": [')
    lecs = [f"    {json.dumps(l, ensure_ascii=False)}" for l in m["lectures"]]
    lines.append(",\n".join(lecs))
    lines.append("  ]")
    lines.append("}")
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def folder(lec):
    return f'{lec["id"]}_{lec["slug"]}'


def find(m, lecture_id):
    for lec in m["lectures"]:
        if lecture_id in (lec["id"], folder(lec)):
            return lec
    raise SystemExit(f"{lecture_id!r} is not in course.json; add it there first.")


def repo_url(m):
    g = m["github"]
    return f'https://github.com/{g["owner"]}/{g["repo"]}'


def colab_url(m, lec, notebook):
    g = m["github"]
    return (f'https://colab.research.google.com/github/{g["owner"]}/{g["repo"]}/blob/'
            f'{g["branch"]}/lectures/{folder(lec)}/{notebook}')


def github_url(m, lec, notebook):
    g = m["github"]
    return f'{repo_url(m)}/blob/{g["branch"]}/lectures/{folder(lec)}/{notebook}'


def setup_cell_source(m, lec):
    return f'''# ▶ Run this cell first. It gets the course code and this lecture's saved results and data,
#   in Google Colab or on your own computer.
LECTURE = "{folder(lec)}"
REPO = "{repo_url(m)}"
import os, sys, subprocess
root = os.path.abspath(os.path.join("..", ".."))
if not os.path.isfile(os.path.join(root, "cs4140_setup.py")):  # not inside the course repo (e.g. Colab)
    root = "/content/cs4140" if "google.colab" in sys.modules else os.path.abspath("cs4140")
    if not os.path.isdir(root):
        subprocess.run(["git", "clone", "--quiet", "--depth", "1", REPO, root], check=True)
    os.chdir(os.path.join(root, "lectures", LECTURE))
sys.path.insert(0, root)
import cs4140_setup
cs4140_setup.fetch_assets(LECTURE)'''


def banner_source(m, lec, notebook):
    return (f'**{m["course"]} · {lec["id"]} · {lec["title"]}** &nbsp; '
            f'[![Open In Colab]({COLAB_BADGE})]({colab_url(m, lec, notebook)})\n\n'
            f'Run the first code cell before anything else. In Colab, *File → Save a copy in Drive* '
            f'keeps your own changes.')
