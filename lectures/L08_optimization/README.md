# L08 · Optimization

Everything here reproduces the numbers and figures in the lecture slides.

## Contents

| Path | What it is |
|---|---|
| `L08_optimization.ipynb` | The notebook, already executed in class mode (outputs included) |
| `results/*.json` | Saved results of every experiment (class mode reads these) |
| `data/charlottetown_A_daily_2025.csv` | Daily weather for Charlottetown A (ECCC climate ID 8300301, station 50621), 2025 |

Fashion-MNIST (about 30 MB) is downloaded into `data/` on the first run, and the notebook writes its figures to `figures/`.

## How to run

Requirements: `torch`, `torchvision`, `numpy`, `matplotlib` (CPU is enough; all preinstalled in Colab).

* **Class mode** (`CLASS_MODE = True`, the default): loads `results/` and redraws the figures. About 25 seconds.
* **Full mode** (`CLASS_MODE = False`): re-runs every experiment. About 8 minutes on a 2-core laptop CPU.
  The batch-size race measures wall-clock time, so your step counts will differ from the slides; the ranking should not.

## Experiments → slides

| Notebook section | Slide | Result on the slides |
|---|---|---|
| 1. Three learning rates (SGD, 2 epochs) | 2 | lr 0.001: 74.1% · lr 0.1: 85.7% · lr 1: 28.3% |
| 2. Batch-size race (8 s of CPU each, best lr each) | 9 | 50,000: 32 steps, 74% · 1,000: 1,601 steps, 89% · 64: 9,061 steps, 88% · 1: 14,744 steps, 84% |
| 3. Exponentially weighted averages (Charlottetown 2025) | 12–14 | β = 0.9, 0.98, 0.5 and the bias-corrected 0.98 |
| 4. Optimizer race on a ravine (30 steps) | 23 | distance to the goal: GD 3.00 · momentum 0.17 · RMSProp 0.80 · Adam 0.41 |
| 5a. Learning-rate sweep (12 values, 2 epochs) | 25 | best lr: SGD 0.1 · momentum 0.01 · RMSProp 0.001 · Adam 0.001 |
| 5b. Optimizer race (5 epochs, 3 seeds) | 24 | SGD 85.9% · momentum 88.1% · RMSProp 86.8% · Adam 88.2% |
| 6. Learning-rate decay (SGD lr 0.1, 3 seeds) | 29 | constant 83.6–87.8% · step 87.8–87.9% · cosine 88.1–88.3% |
| 7. Saddles vs minima (200,000 random matrices per size) | 33 | minima: N = 3 2.5% · N = 5 20 of 200,000 · none from N = 6 |

All accuracies are on 10,000 validation images held out from the Fashion-MNIST training set (50,000 used for training).
The test set is not used in this lecture.

Network: the MLP from L05, 784 → 128 → 10 with ReLU (101,770 parameters). Minibatches of 64 unless stated.

## Data source and terms

`data/charlottetown_A_daily_2025.csv` comes from Environment and Climate Change Canada (ECCC),
Historical Climate Data, [climate.weather.gc.ca](https://climate.weather.gc.ca): station
Charlottetown A (climate ID 8300301, station ID 50621), daily data for 2025.

Based on Environment and Climate Change Canada data. ECCC provides the data free of charge under its
[terms of use](https://climate.weather.gc.ca/prods_servs/attachment1_e.html); anyone who receives the
data from this repository is bound by the same terms, and it may not be passed on for a fee.
Credit ECCC wherever you use the data or figures made from it.

Fashion-MNIST: Xiao, Rasul & Vollgraf (2017), MIT licence, downloaded by torchvision.
