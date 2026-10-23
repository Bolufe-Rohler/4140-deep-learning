"""Rewrite every notebook's banner and setup cell from course.json.

Run after changing the GitHub owner/repo/branch or a lecture title:
    python tools/refresh_cells.py && python tools/build_readme.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import course  # noqa: E402
from add_lecture import add_cells  # noqa: E402


def main():
    m = course.load()
    n = 0
    for lec in m["lectures"]:
        for nb in lec["notebooks"]:
            add_cells(course.ROOT / "lectures" / course.folder(lec) / nb, m, lec)
            n += 1
    print(f"Refreshed {n} notebook(s) for {course.repo_url(m)}")


if __name__ == "__main__":
    main()
