# L07 · CNNs II: our images, end to end

**Notebook:** `L07_cnn_cifar10.ipynb`. It needs `torch`, `torchvision`, `matplotlib` and `numpy` (all
preinstalled in Colab). The first run downloads CIFAR-10 (163 MB) into `data/`.

The LeNet-style network from the CNN Example slides, trained on CIFAR-10 with the complete workflow
(45,000 training / 5,000 validation / 10,000 test images, minibatches of 64, Adam, 20 epochs, validation
after every epoch, best checkpoint kept, test set used once), next to a dense network trained the same way.

| Flag | Default | Effect |
|---|---|---|
| `TRAIN` | `False` | Loads the saved runs in `runs/` and replays the training log: under a minute after the download. `True` retrains both networks: about 5 minutes each on a laptop CPU, seconds per epoch on a GPU. With the same seed on a CPU you get the same numbers. |

`runs/` holds the saved results the slides use:

| File | What it is |
| --- | --- |
| `dense_best.pt`, `cnn_best.pt` | best checkpoint of each network (chosen on validation) |
| `dense_history.json`, `cnn_history.json` | training and validation accuracy and loss for every epoch |
| `test_results.json` | parameters, best epoch, validation and test accuracy |
| `predictions.json` | the 16 test predictions shown in the notebook |

The notebook also writes its figures (`curves.png`, `predictions.png`) to `runs/`.

| | dense network | LeNet-style CNN |
| --- | --- | --- |
| parameters | 1,707,274 | 62,958 |
| best epoch | 10 | 12 |
| validation accuracy | 53.7% | 66.4% |
| test accuracy (once) | 52.6% | 66.0% |

CIFAR-10: Krizhevsky (2009), downloaded by torchvision.
