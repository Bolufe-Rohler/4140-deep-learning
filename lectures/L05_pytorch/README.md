# L05 · PyTorch in four ideas

| File | What it is |
|---|---|
| `L05_pytorch_four_ideas.ipynb` | PyTorch notebook, executed (outputs included). Sections 1–5 match slides 4–19; section 6 has four exercises. |
| `fashion_mlp_sgd.pt`, `fashion_mlp_sgd_losses.npy` | Weights and loss curve of the section-4 network (2 epochs of SGD), used when `RUN_TRAINING = False`. |

**Run it.** Needs `torch`, `torchvision`, `numpy`, `matplotlib` (all preinstalled in Colab). The first run
downloads Fashion-MNIST (about 30 MB) into `./data`, and the notebook writes its figures to `figs/`.
Built with PyTorch 2.14 and torchvision 0.29 (CPU).

* `RUN_TRAINING = True` (the default): under 30 seconds on a CPU after the download (training takes about 8 s).
* `RUN_TRAINING = False`: about 10 seconds, loading the saved network.

The notebook uses one CPU thread (`torch.set_num_threads(1)`) so runs repeat: 82.7% test accuracy after
epoch 1, 82.9% after epoch 2.

Fashion-MNIST: Xiao, Rasul & Vollgraf (2017), MIT licence, downloaded by torchvision.
