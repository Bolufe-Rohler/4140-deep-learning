# L10 · Training deeper networks

The saved runs behind the lecture slides: initialization, batch normalization, plain vs residual networks, and a pretrained ResNet-18.

## What is inside

| File | What it is |
|---|---|
| `L10_training_deeper_networks.ipynb` | The notebook, executed in class mode (the default). |
| `results/results.json` | Every number used on the slides: the per-epoch history of every training run, the gradient profiles, the knock-out accuracies and the ResNet-18 predictions. |
| `results/*.pt` | Weights of the seven trained CNNs (4 for Part 4, 3 more for Part 5, which also reuses `plain-20`). 0.3 to 1 MB each. |

## How to run it

Needs `torch`, `torchvision`, `numpy`, `matplotlib` and `scikit-image` (all preinstalled in Colab). The notebook writes its figures to `figures/`.

* **Class mode** (`CLASS_MODE = True`, the default) loads the saved runs from `results/` and redraws every figure. Parts 1–3 (the probes at initialization) run live. About 20–30 seconds on a laptop CPU.
* **Full mode** (`CLASS_MODE = False`) retrains the seven small CNNs. About 20–25 minutes on a 2-core CPU; a few minutes on a GPU or a recent laptop. Each run is saved as soon as it finishes, so an interrupted full run can be finished in class mode: class mode trains only the runs that are missing from `results/`.
* The first run downloads Fashion-MNIST (about 30 MB) into `data/`, and torchvision downloads the ResNet-18 weights (about 45 MB) into its cache. Without internet, Part 7 shows the architecture and the saved predictions.

## The parts

| Part | Slide | What it shows |
|---|---|---|
| 1 | Why Do Gradients Vanish or Explode? | 0.9, 1.0 and 1.1 multiplied 20, 50 and 100 times |
| 2 | Tool 1: Initialization | 50 ReLU layers before training: PyTorch's default initialization vs He initialization |
| 3 | A Highway for the Gradient | Gradient size at every layer of 56-layer CNNs before training |
| 4 | We Tried It; Plain vs Residual | Plain and residual CNNs with 20 and 56 layers, 10 epochs each |
| 5 | Batch Normalization (in Practice) | A plain 20-layer CNN trained four ways; one batch-norm layer before/after normalization |
| 6 | Remove One Block | Delete one block from the trained 56-layer networks |
| 7 | Inspecting a Pretrained ResNet-18 | Structure, shapes, and predictions on four public-domain photos |

## Setup of the experiments

* Data: Fashion-MNIST, 12,000 training images and 2,000 validation images taken from the official training set with a fixed seed.
* Networks: CIFAR-style CNNs for 28×28 images. A 3×3 convolution, then three stages of n blocks at 8, 16 and 32 channels (28×28, 14×14, 7×7), global average pooling and a linear layer: 6n + 2 layers (n = 3 → 20, n = 9 → 56). A block is two 3×3 convolutions; the residual block adds the shortcut (a 1×1 convolution with stride 2 where the shape changes, as in torchvision).
* Training: SGD with momentum 0.9, one-cycle learning rate (peak 0.1 unless stated), batch 128, weight decay 1e-4, 10 epochs, seed 0. "Training loss" is measured on 4,000 training images at the end of each epoch.
* One seed per configuration. The networks are deliberately small so that everything runs on a CPU.

## Things to try

The last cell of the notebook lists four exercises (wider networks, residual networks without batch norm, `zero_init_residual=True`, and photos outside the 1000 ImageNet classes).

## Credits

* Fashion-MNIST: Zalando Research (MIT licence).
* ResNet-18 weights: torchvision (`ResNet18_Weights.IMAGENET1K_V1`), trained on ImageNet.
* Photos (shipped with scikit-image): Chelsea the cat (Stefan van der Walt, CC0), coffee (Rachel Michetti, CC0), astronaut Eileen Collins (NASA, public domain), Falcon 9 launch of DSCOVR (SpaceX, public domain).
* References for the slides: He et al. 2015 (He initialization; ResNets, "Deep Residual Learning for Image Recognition"); Ioffe & Szegedy 2015 (batch normalization); Veit et al. 2016 ("Residual Networks Behave Like Ensembles of Relatively Shallow Networks"); Yang et al. 2019 ("A Mean Field Theory of Batch Normalization"); Szegedy et al. 2014 ("Going Deeper with Convolutions").
