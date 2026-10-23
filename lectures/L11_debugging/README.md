# L11 · Debugging models and checking experiments

The notebook behind the lecture: a student's Fashion-MNIST CNN that runs without errors and is wrong,
a seven-rung debugging ladder that finds each problem, and a seed-paired comparison that checks whether an
"upgrade" is real.

## Run it

* `L11_debugging_and_experiments.ipynb`, first code cell:
  * `CLASS_MODE = True` (default): loads `results.json` and `weights/`; the cheap checks (rungs 1-3) and the
    confusion matrix run live.
    About 30 s on a laptop CPU.
  * `CLASS_MODE = False`: re-runs every experiment and rewrites `results.json`, `weights/` and `runs/`.
    About 45 min on a 2-core CPU.
* Needs Python 3.10+, `torch`, `torchvision` (0.16 or newer, for `transforms.v2`), `numpy`, `matplotlib`.
* The first run downloads Fashion-MNIST (about 30 MB) into `data/`. The notebook writes its figures to `figures/`.

## What is in the package

| Path | What |
|---|---|
| `L11_debugging_and_experiments.ipynb` | The notebook, executed in class mode |
| `results.json` | Every number on the slides: runs, checks, baselines, comparison, test accuracy |
| `weights/` | `A_student.pt` (the buggy model), `A3_fixed.pt` (fixed, small head), `wide_s0.pt` (fixed, wider head) |
| `runs/` | 24 run records, one folder per training run: `config.json` (purpose, settings, seed, code version, commit, data split, environment) and `metrics.json` |
| `data/` | Fashion-MNIST (Xiao, Rasul & Vollgraf, 2017; MIT licence), downloaded on the first run |

## The setup

* Fashion-MNIST, one fixed split of the 60,000 training images: 20,000 for training, 5,000 for validation
  (split seed 1234). The official 10,000-image test set is opened once, at the end.
* Small CNN: two 3×3 convolutions (16 and 32 channels) with ReLU and max-pooling, then a linear head
  (1568 → 10, 20,490 parameters) or a wider head (1568 → 128 → 10, 206,922 parameters).
* Adam, learning rate 0.001, batch 64, 8 epochs, CPU, one data-loader worker on Linux.

## The planted bugs (spoilers)

| # | Line in the student notebook | Found by | Fix | Costs alone |
|---|---|---|---|---|
| 1 | `T.RandomResizedCrop(28)`: ImageNet defaults keep 8-100% of the image | Rung 1: look at the batch after the pipeline | `scale=(0.8, 1.0)` | 4.7 points |
| 2 | `T.Normalize((0.5,), (0.5,))` in the evaluation transform; training uses (0.2860, 0.3530) | Rung 2: compare training and validation inputs | Same constants in both | 5.3 points |
| 3 | `nn.Softmax(dim=1)` at the end of the model, with `nn.CrossEntropyLoss` | Rung 4: tiny batch, loss floor ln(1 + 9/e) = 1.461 (rung 3 passes) | Delete it | 5.2 points |
| 4 | Wider head pasted in a cell after the optimizer was built | Rung 5: the head has gradients but moves 0.00% | Build the optimizer last | 88.0% → 76.5% |

## Main numbers (validation accuracy after 8 epochs)

| Run | Accuracy |
|---|---|
| Chance / linear model on pixels / L05 MLP | 10.0% / 85.2% / 87.3% |
| Student notebook (bugs 1-3) | 75.6% |
| Fix the crop | 80.2% |
| Fix the crop and the normalization | 82.9% |
| Fix all three (small head, seed 0) | 88.0% |
| Wider head pasted after the optimizer (bug 4) | 76.5% |
| Small head, 5 seeds | 88.08% (range 87.66-88.48%) |
| Wider head, 5 seeds | 88.33% (range 87.56-89.02%) |
| Paired difference (wider - small) | +0.24 ± 0.59 points; wider better in 2 of 5 seeds |
| Decision (rule fixed in advance: wins on average and in at least 4 of 5) | keep the small head |
| Test set, opened once (A3_fixed) | 88.1% |

## Notes

* Numbers can differ slightly on another machine, operating system or library version, even with the same
  seeds (the PyTorch reproducibility notes say as much). On Windows and macOS the notebook loads data in the
  main process (`NUM_WORKERS = 0`), which changes the augmentation's random draws.
* The field-guide runs (rung 6) use 10,000 training images and 3-4 epochs; the overfitting panel uses 1,000
  images, no augmentation, 40 epochs.
* Label-error figures on slide 19: Northcutt, Athalye & Mueller, "Pervasive Label Errors in Test Sets
  Destabilize Machine Learning Benchmarks", NeurIPS 2021 Datasets and Benchmarks (arXiv:2103.14749).
* Debugging recipe: Karpathy, "A Recipe for Training Neural Networks", 2019 (karpathy.github.io).
