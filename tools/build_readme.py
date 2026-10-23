"""Regenerate README.md from course.json.  Usage: python tools/build_readme.py"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import course  # noqa: E402

INTRO = """# {course} · Demo notebooks

{institution} · {term} · {instructor}

The code shown in class, one folder per lecture. Every notebook runs in Google Colab
with one click, or on your own computer.

## Running a notebook

**In Google Colab (nothing to install).** Click the notebook's *Open in Colab* badge below
or the link on Moodle. Run the first code cell before anything else: it fetches the course
code and the lecture's saved results and data. Colab starts from scratch every time you
reconnect, so run that cell again after a reconnect. Your changes are lost unless you use
*File → Save a copy in Drive*. For the longer training runs, *Runtime → Change runtime type
→ GPU* helps when Colab offers one.

**On your own computer.**

```bash
git clone {repo}.git
cd {repo_name}
pip install -r requirements.txt
jupyter lab
```

Open a notebook inside `lectures/` and run its first cell, which downloads that lecture's
saved results and data the first time.

**Class mode and full mode.** Most notebooks start in *class mode*: they load saved results
and trained weights so they run in seconds, as in the lecture. Switching to full mode
(the flag is near the top of each notebook) retrains everything from scratch; each
notebook says how long that takes.

## Lectures

| | Lecture | Notebook | |
|---|---|---|---|
"""

OUTRO = """
Lecture numbers follow the order of topics (tests and storm days are not numbered), so
they match the Moodle sections even if a class moves.

## Data and credits

Each lecture folder lists the datasets it uses and their licences in its README or
`CREDITS.md`. Trained weights, saved runs and datasets are not stored in git; they are
attached to the [{release}]({repo}/releases/tag/{release}) release and downloaded by the
first cell of each notebook.
"""


def main():
    m = course.load()
    rows = []
    for lec in m["lectures"]:
        for i, nb in enumerate(lec["notebooks"]):
            badge = f'[![Open In Colab]({course.COLAB_BADGE})]({course.colab_url(m, lec, nb)})'
            first = i == 0
            rows.append(f'| {lec["id"] if first else ""} | {lec["title"] if first else ""} '
                        f'| [{nb}](lectures/{course.folder(lec)}/{nb}) | {badge} |')
    if not rows:
        rows.append("| | *Notebooks appear here as lectures are added.* | | |")
    g = m["github"]
    fill = dict(m, repo=course.repo_url(m), repo_name=g["repo"], release=m["assets_release"])
    text = INTRO.format(**fill) + "\n".join(rows) + "\n" + OUTRO.format(**fill)
    (course.ROOT / "README.md").write_text(text, encoding="utf-8")
    print(f"README.md: {len(rows)} notebook row(s)")


if __name__ == "__main__":
    main()
