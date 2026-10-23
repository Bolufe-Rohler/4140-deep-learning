# L09 · Generalization and regularization

Everything here reproduces the numbers and figures in the lecture slides.

## Contents

| Path | What it is |
|---|---|
| `L09_generalization.ipynb` | The notebook, already executed in class mode (outputs included) |
| `results/*.json` | Saved results of every experiment (class mode reads these) |
| `models/*.pt` | The trained CNNs (3 seeds per setting), used for the test-set check, the weight histograms and the eval-mode check. Not stored in git: the notebook's first cell downloads them (14 MB). |

Fashion-MNIST (about 30 MB) is downloaded into `data/` on the first run, and the notebook writes its figures to `figures/`.

## How to run

Requirements: `torch`, `torchvision`, `numpy`, `matplotlib` (CPU is enough; all preinstalled in Colab).

* **Class mode** (`CLASS_MODE = True`, the default): loads `results/` and `models/` and redraws the figures. About 20 seconds.
* **Full mode** (`CLASS_MODE = False`): re-runs everything, about 45 minutes on a 2-core laptop CPU (most of it is the 21 CNN trainings of section 2).
  If a class-mode run finds section 2 incomplete, it resumes where it stopped.

## Setup

Fashion-MNIST, deliberately small: **2,000 training images**, 5,000 validation images (both from the training file),
and the official 10,000 test images, used exactly once (section 3).
Network: a small CNN (two 3×3 convolutions with 16 and 32 filters, 2×2 max-pooling, a 128-unit dense layer; 206,922 parameters).
Training: Adam, learning rate 0.001, minibatches of 64, 50 epochs, three seeds per setting.

## Results → slides

**Section 1, real vs shuffled labels (slide 2):** both reach 100% training accuracy; validation 83.7% (real) vs 9.5% (shuffled, chance = 10%).

**Section 2, one intervention at a time (slides 5, 12, 23), mean of 3 seeds:**

| Setting | Training acc. | Validation acc. | Gap (points) | Validation loss |
|---|---|---|---|---|
| baseline | 99.8% | 84.1% | 15.7 | 0.78 |
| early stopping | 93.7% | 85.1% | 8.6 | 0.44 |
| weight decay | 97.4% | 83.7% | 13.7 | 0.50 |
| dropout | 96.6% | 85.6% | 11.0 | 0.44 |
| augmentation | 92.4% | 85.0% | 7.4 | 0.44 |
| all three | 83.7% | 81.2% | 2.5 | 0.49 |
| 5× more data | 100.0% | 88.7% | 11.3 | 0.81 |

Early stopping = the baseline's own best-validation epoch. Weight decay: Adam `weight_decay=0.005`. Dropout: p = 0.5 before both dense layers.
Augmentation: random horizontal flip + random shift of up to 2 pixels. More data: 10,000 training images.

**Section 3, the sealed envelope (slide 23):** chosen by validation accuracy: *dropout* (85.6% validation) → 85.4% on the 10,000 test images.

**Section 4, double descent (slide 7):** random-ReLU-feature networks trained on 1,000 images: validation error 24% at p = 200,
88% at p = 1000 (= the number of training images), 21% at p = 20,000.

**Section 5, pictures and checks (slides 12, 18, 19–20):** overall weight norm 18.1 → 8.7 with weight decay;
the dropout CNN scores 85.6% on validation with `model.eval()` and 82.9% if you forget it.

Fashion-MNIST: Xiao, Rasul & Vollgraf (2017), MIT licence, downloaded by torchvision.
