# Maintaining the repo (instructor notes)

Everything is driven by `course.json`: one entry per lecture, numbered by topic order
(tests and storm days are not numbered, so a moved class never renames a folder).
Folder names are `<id>_<slug>`, e.g. `lectures/L11_debugging/`.

## Add or update a lecture

```bash
python tools/add_lecture.py CS4140_L12_Debugging_Demo.zip L11            # plan only
python tools/add_lecture.py CS4140_L12_Debugging_Demo.zip L11 --apply --replace
python tools/build_readme.py
python tools/verify.py --lecture L11
git add -A && git commit -m "L11: debugging demo"
git push
gh release upload winter-2027-assets dist/L11_debugging_assets.zip --clobber
```

`add_lecture.py` sorts the package's files three ways and shows the plan first:

| Goes to | What |
|---|---|
| git | notebooks, small JSON/CSV, scripts, READMEs and licence files |
| release asset | weights and arrays, anything over 1 MiB, folders of more than 200 files |
| left out | `deck_source/`, `figures/`, `make_figures*.py` (slide material), caches |

Override with `--asset`, `--exclude` or `--keep` and a glob, e.g. `--keep "data/*.csv"`.
It also puts an *Open in Colab* banner and the setup cell at the top of each notebook
(tagged, so re-running replaces them rather than adding more).

## First publication

```bash
gh release create winter-2027-assets dist/*.zip --title "Winter 2027 saved results and data" \
   --notes "Downloaded automatically by the first cell of each notebook."
```

Without `gh`, the release can be made on GitHub in the browser: *Releases → Draft a new
release*, tag `winter-2027-assets`, and drag in the zips from `dist/`.

## Moodle

Per lecture: the lecture PDF, a URL resource *Demo: open in Colab* pointing at the
notebook's Colab link (the README badge has it), and the quiz. The links point at `main`,
so a fix pushed mid-semester reaches every student at once.

## End of term

Tag the final state so this year's version stays available as it was taught:

```bash
git tag winter-2027 && git push --tags
```
