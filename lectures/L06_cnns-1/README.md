# L06 · CNNs I: from hand-made to learned filters

**Notebook:** `L06_cnn_filters.ipynb`. It runs in under a minute and needs `torch`, `torchvision`,
`matplotlib`, `numpy`, `pillow` and `scikit-image` (all preinstalled in Colab).

PyTorch reproduces the edge-detection examples from the slides, then hand-made filters run on a photo,
then the 64 first-layer filters ResNet-18 learned on its own, and their feature maps.

* The first run downloads ResNet-18's ImageNet weights (about 45 MB) through torchvision.
* Put a photo next to the notebook as `campus.jpg` to use it instead of the built-in sample image
  (from scikit-image).

ResNet-18: He et al. (2015); weights from torchvision, trained on ImageNet.
