# L03 · Networks as function approximators

**Notebook:** `L03_networks_as_function_approximators.ipynb`. Needs `torch`, `torchvision`, `numpy` and
`matplotlib` (all preinstalled in Colab).

What to look for:

1. **Width:** more hidden units give the network more pieces to bend a function with.
2. **Activation:** without a nonlinearity, any number of layers collapses to a straight line.
3. **Depth:** composing layers multiplies the number of pieces.
4. **Expressive power is not what training finds:** a network that *can* represent XNOR does not always
   *learn* it. From 20 random starts, a 2-2-1 network learns it 18 times and a 2-8-1 network 20 times.
5. **A dense image classifier:** the same recipe on Fashion-MNIST; trace one minibatch through the model.

## Running time and flags

Sections 1–5 take under a minute on a laptop CPU. Section 6 downloads Fashion-MNIST (about 30 MB) into
`./data` and trains for about a minute.

| Flag | Default | Effect |
|---|---|---|
| `TRAIN_IMAGES` | `True` | Trains the Fashion-MNIST network in section 6 and saves it as `fashion_mlp.pt`. `False` loads the saved `fashion_mlp.pt` instead. |
| `SAVE_FIGS` | `False` | `True` saves the figures to `figures/`. |

Fashion-MNIST: Xiao, Rasul & Vollgraf (2017), MIT licence, downloaded by torchvision.
