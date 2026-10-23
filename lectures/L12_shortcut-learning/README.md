# L12 · Shortcut learning and trustworthy evaluation

The notebook behind the lecture. A student's "ten shops" version of Fashion-MNIST gives the CNN from L11
almost 100%, because each shop stamps a 2×2 logo in its own spot and each category came from one shop. The
notebook tests that hypothesis with two baselines, a targeted ablation with a control, a counterfactual and
occlusion maps. It then shows a partial shortcut hiding in a small group, two fixes, leakage from augmented
copies, and the robust model under new photo conditions.

## Run it

* `L12_shortcuts_and_trustworthy_evaluation.ipynb`, first code cell:
  * `CLASS_MODE = True` (default): loads `results.json` and `weights/`; every evaluation, picture and occlusion
    map runs live. Under a minute on a laptop CPU.
  * `CLASS_MODE = False`: retrains all 15 models and rewrites `results.json`, `weights/` and `runs/`.
    About 8-10 min on a 2-core CPU.
* Needs Python 3.10+, `torch`, `torchvision` (0.16 or newer, for `transforms.v2`), `numpy`, `matplotlib`.
* The first run downloads Fashion-MNIST (about 30 MB, MIT licence) into `data/`. The notebook writes its figures to `figures/`.

## What is in the package

| Path | What |
|---|---|
| `L12_shortcuts_and_trustworthy_evaluation.ipynb` | The notebook, executed in class mode |
| `results.json` | Every number on the slides: training runs, the ablation, counterfactual, stress tests, leakage and shift results |
| `weights/` | `shortcut.pt` (the student's model), `erase_tags.pt` (fix 1), `mixed_shops.pt` (fix 2 and the control), `partial.pt` (95% tags), all seed 0 |
| `runs/` | 15 run records, one folder per training run: `config.json` (purpose, settings, seed, code version, environment) and `metrics.json` |
| `data/` | Fashion-MNIST (Xiao, Rasul & Vollgraf, 2017; MIT licence), downloaded on the first run |

## The setup

* Same split as L11: 20,000 training and 5,000 validation images from the 60,000 Fashion-MNIST training
  images (split seed 1234); the 10,000 test images are used for every stress test.
* The tag: a 2×2 square of value 255. Shop k puts it at one of ten spots (top row: columns 1, 7, 13, 19, 25 for
  T-shirt to Coat; bottom row, same columns, for Sandal to Ankle boot).
* Same small CNN as L11 (two 3×3 convolutions with 16 and 32 channels, max-pooling, a linear head),
  Adam 0.001, batch 64, 8 epochs, no augmentation, CPU. Three seeds for the main models.

## Main numbers

| Result | Value |
|---|---|
| Student's model, validation (3 seeds) | 99.99% |
| Cue-only baseline (tag strips only) / garment-only baseline (tag spots blanked) | 100.00% / 88.6% |
| Ablation: student's model with tag → tag removed | 99.99% → 57.5% |
| Same ablation on the control (tags carried no information) | 87.8% → 88.5% |
| Wrong shop's tag: student's model accuracy / follows the tag | 16.7% / 70.2% |
| Wrong shop's tag: control accuracy / follows the tag | 88.3% / 1.2% |
| Stress test, student's model: own shop tag (like the student data) / no tag / random tag / wrong shop tag | 99.99% / 57.5% / 25.0% / 16.7% |
| Stress test, fix 1: blank the tag spots: own shop tag (like the student data) / no tag / random tag / wrong shop tag | 88.7% / 88.7% / 88.7% / 88.7% |
| Stress test, fix 2: mix the shops: own shop tag (like the student data) / no tag / random tag / wrong shop tag | 87.8% / 88.5% / 88.3% / 88.3% |
| Partial shortcut (95%): average / tag disagrees with label (3 seeds) | 98.0% / 71.2% |
| Leakage: copy then random split, validation / new garments | 90.8% / 79.3% |
| Leakage: split by original photo, validation / new garments | 78.5% / 80.5% |
| Shift (fix 1 model): same conditions | 88.7% |
| Shift (fix 1 model): moved 2 px right and down | 58.5% |
| Shift (fix 1 model): garment at 75% size | 66.1% |
| Shift (fix 1 model): half as bright | 82.4% |
| Shift (fix 1 model): inverted (white background) | 17.1% |

## Notes

* "New garments" in the leakage demo are 5,000 validation photos never copied, each with one random crop and
  flip, so they match how the copies were made.
* A second full run on the same machine reproduced every number exactly. On another machine, operating system or
  PyTorch version the last digit can change.
* The shift results use a model trained without augmentation; small moves would be handled better with L11's
  crop augmentation, the inverted background would not.

## Sources for the real cases on the slides

* Geirhos et al., "Shortcut learning in deep neural networks", Nature Machine Intelligence, 2020 (definition).
* Ribeiro, Singh & Guestrin, "Why should I trust you?", KDD 2016 (wolves and snow).
* Zech et al., "Variable generalization performance of a deep learning model to detect pneumonia in chest
  radiographs", PLOS Medicine, 2018.
* DeGrave, Janizek & Lee, "AI for radiographic COVID-19 detection selects shortcuts over signal", Nature Machine
  Intelligence 3, 610-619, 2021.
* Winkler et al., "Association between surgical skin markings in dermoscopic images and diagnostic performance of
  a deep learning convolutional neural network for melanoma recognition", JAMA Dermatology, 2019.
* Lapuschkin et al., "Unmasking Clever Hans predictors and assessing what machines really learn", Nature
  Communications, 2019.
* Mohanty, Hughes & Salathé, "Using deep learning for image-based plant disease detection", 2016; Noyan,
  "Uncovering bias in the PlantVillage dataset", 2022.
* Sagawa et al., "Distributionally robust neural networks for group shifts", ICLR 2020 (Waterbirds).
* Kapoor & Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science", Patterns 4(9), 2023.
* Recht et al., "Do ImageNet classifiers generalize to ImageNet?", ICML 2019.
