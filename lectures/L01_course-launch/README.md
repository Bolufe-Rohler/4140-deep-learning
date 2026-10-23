# L01 · Course launch: what does a deep network learn?

| File | What it is |
|---|---|
| `L01_what_machines_learn.ipynb` | PyTorch notebook, executed (outputs included). Sections 1–4 match the demo slides ("Demo: Two Numbers per Image", "Watch the Space Form During Training"); section 5 has four things to try. |
| `mnist_two_numbers.pt` | Weights of the 2-number network after 10 epochs, plus the training snapshots, used when `RUN_TRAINING = False`. |
| `results.json` | The numbers the slides quote. |

**Run it.** Needs `torch`, `torchvision`, `numpy`, `matplotlib` (all preinstalled in Colab). The first run
downloads MNIST (about 10 MB) into `./data`, and the notebook writes its figures to `figs/`.
Built with PyTorch 2.14 and torchvision 0.29 (CPU).

* `RUN_TRAINING = True` (the default): about 1 minute on a laptop CPU after the download (training takes about 40 s).
* `RUN_TRAINING = False`: about 10 seconds, loading `mnist_two_numbers.pt`.

The notebook uses one CPU thread (`torch.set_num_threads(1)`) so runs repeat: 44.6% with 2 PCA numbers, 92.5%
with a linear model on all 784 pixels, 96.4% with the 2 numbers the network learns (snapshots: 10% before
training, 43% after 50 steps, 91% after 1 epoch, 96% after 10).

MNIST: LeCun, Cortes & Burges, downloaded by torchvision.
