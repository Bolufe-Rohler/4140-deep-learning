# CS 4140 – Deep Learning · Demo notebooks

University of Prince Edward Island · Winter 2027 · Antonio Bolufé-Röhler

The code shown in class, one folder per lecture. Every notebook runs in Google Colab
with one click, or on your own computer.

## Running a notebook

**In Google Colab (nothing to install).** Click the notebook's *Open in Colab* badge below
or the link on Moodle. Run the first code cell before anything else: it fetches the course
code and the lecture's saved results and data. Colab starts from scratch every time you
reconnect, so run that cell again after a reconnect. Your changes are lost unless you use
*File → Save a copy in Drive*.

**On your own computer.**

```bash
git clone https://github.com/OWNER/4140-deep-learning.git
cd 4140-deep-learning
pip install -r requirements.txt
jupyter lab
```

Open a notebook inside `lectures/` and run its first cell, which downloads that lecture's
saved results and data the first time.

**Saved results or live training.** Flags at the top of each notebook choose between loading
saved results and trained weights (seconds) and retraining from scratch (minutes, sometimes
much longer). Each lecture's README lists its flags and how long each option takes.

## Lectures

| | Lecture | Notebook | |
|---|---|---|---|
| L04 | Why go deep? | [L04_why_go_deep.ipynb](lectures/L04_why-go-deep/L04_why_go_deep.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/4140-deep-learning/blob/main/lectures/L04_why-go-deep/L04_why_go_deep.ipynb) |
| L15 | Sequences I: order and recurrent state | [L15_sequences_recurrent_state.ipynb](lectures/L15_sequences-1/L15_sequences_recurrent_state.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/4140-deep-learning/blob/main/lectures/L15_sequences-1/L15_sequences_recurrent_state.ipynb) |
| L16 | Sequences II: memory and learning over time | [L16_memory_lstm.ipynb](lectures/L16_sequences-2/L16_memory_lstm.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OWNER/4140-deep-learning/blob/main/lectures/L16_sequences-2/L16_memory_lstm.ipynb) |

Lecture numbers follow the order of topics (tests and storm days are not numbered), so
they match the Moodle sections even if a class moves.

## Data and credits

Each lecture folder lists the datasets it uses and their licences in its README or
`CREDITS.md`. Trained weights, saved runs and datasets are not stored in git; they are
attached to the [winter-2027-assets](https://github.com/OWNER/4140-deep-learning/releases/tag/winter-2027-assets) release and downloaded by the
first cell of each notebook.
