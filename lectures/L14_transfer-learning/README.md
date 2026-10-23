# L14 · Transfer learning and fine-tuning

Can a network trained on ImageNet spot potato blight? The saved runs behind the lecture slides.

## What is inside

| File | What it is |
|---|---|
| `L14_transfer_learning.ipynb` | The notebook, executed in class mode (the default). |
| `data/` | The potato images: 2,152 PlantVillage lab photos (with leaf IDs) and 222 PlantDoc field photos. Licences in `data/CREDITS.md`. The photos are not stored in git: the notebook's first cell downloads them with the saved runs (about 90 MB). |
| `results/results.json` | Every number on the slides: the training-size runs, the lab-to-field runs and the backbone comparison. |
| `results/*.pt` | The ResNet-18 features of all photos (160×160) and the fine-tuned and from-scratch ResNet-18 trained on 25 leaves per class (stored in float16, 22 MB each; the last cell of the notebook shows how to load them). |

## How to run it

Needs `torch`, `torchvision`, `numpy`, `matplotlib`, `pillow` (all preinstalled in Colab). Run the first code cell first: it downloads the photos and saved runs. The notebook writes its figures to `figures/`.

* **Class mode** (`CLASS_MODE = True`, the default) loads the saved runs and redraws every figure. Only missing runs are trained. With the saved runs it takes under a minute on a laptop CPU (about 25 s on the 2-core machine that made it) and, once the first cell has run, needs no internet.
* **Full mode** (`CLASS_MODE = False`) retrains everything: about 30–40 minutes on a 2-core CPU. Each run is saved when it finishes, so an interrupted run can be completed in class mode.
* Full mode (or a class-mode run with files missing from `results/`) makes torchvision download the ImageNet backbones on first use (ResNet-18 45 MB, ResNet-50 98 MB, MobileNetV3-Large 21 MB, EfficientNet-B0 20 MB).

## The parts

| Part | Slides | What it shows |
|---|---|---|
| Data | 2 | Lab and field photos (`fig_samples`) |
| 1 | 4, 8 | ResNet-18 ImageNet features of every photo, squashed to 2D with PCA: lab classes form groups; field photos of both diseases mix (`fig_pca`) |
| 2 | 7 | Frozen features vs fine-tuning vs from scratch with 1, 5 and 25 leaves per class (`fig_size`) |
| 3 | 9 | From the lab to the field: lab test, field test, adding 40 field photos, field photos only (`fig_shift`) |
| 4 | 11, 22 | Four backbones: parameters, multiply-adds by kind of convolution, CPU time, accuracy (`fig_macs`) |

## Setup of the experiments

* **Classes:** healthy, early blight, late blight (3 classes; chance 33%).
* **Lab split by leaf:** every leaf was photographed 4 times, so whole leaves go to train or test. Test: 13 leaves per class (156 photos). Training: 1, 5 or 25 other leaves per class (4, 20 or 100 photos), drawn with seeds 0–2 (seed 0 only for 25 leaves, except for frozen features).
* **Field test:** 182 PlantDoc photos (early or late blight). The question asked is only "early or late blight?" (chance 50%), because PlantDoc has no healthy potato leaves. 20 field photos per disease are held back for the "add field photos" runs.
* **Three strategies, same ResNet-18:** frozen ImageNet features + a new linear layer; fine-tuning all weights from ImageNet (SGD, learning rate 0.01, 100 steps of 16 photos); from scratch (random weights, learning rate 0.05, 300 steps). Random crops and flips; 160×160 photos to keep the CPU time down.
* **Backbones (Part 4):** frozen features at 224×224, new linear layer on 5 leaves per class (seeds 0–2). CPU time is for one photo at a time on the machine that ran the notebook.
* The networks and runs are deliberately small; one or three seeds per configuration.

## Things to try

The last cell of the notebook lists four exercises (splitting by photo instead of by leaf, fine-tuning only `layer4`, a "frozen" backbone left in `train()` mode, and testing on your own photos).

## Credits

* PlantVillage (CC BY-SA 3.0): Mohanty, Hughes and Salathé (2016). PlantDoc (CC BY 4.0): Singh et al. (2020). Details in `data/CREDITS.md`.
* Pretrained weights: torchvision (ImageNet). ResNet: He et al. (2015); MobileNetV3: Howard et al. (2019); EfficientNet: Tan and Le (2019).
* PEI potato share (20.2% of Canada's 2024 crop): Statistics Canada, "No spud limit in Canada: Another record for potato production in 2024".
