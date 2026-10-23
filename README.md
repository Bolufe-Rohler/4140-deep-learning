# CS 4140 – Deep Learning · Demo notebooks

University of Prince Edward Island · Winter 2027 · Antonio Bolufé-Röhler

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
git clone https://github.com/OWNER/4140-deep-learning.git
cd 4140-deep-learning
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
| | *Notebooks appear here as lectures are added.* | | |

Lecture numbers follow the order of topics (tests and storm days are not numbered), so
they match the Moodle sections even if a class moves.

## Data and credits

Each lecture folder lists the datasets it uses and their licences in its README or
`CREDITS.md`. Trained weights, saved runs and datasets are not stored in git; they are
attached to the [winter-2027-assets](https://github.com/OWNER/4140-deep-learning/releases/tag/winter-2027-assets) release and downloaded by the
first cell of each notebook.
