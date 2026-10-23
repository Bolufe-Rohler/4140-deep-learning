# L02 · From familiar ML to a first neural network

**Notebook:** `L02_learning_in_two_spaces.ipynb`. It runs on a laptop CPU in a few seconds, needs only
`torch`, `numpy` and `matplotlib`, and downloads nothing.

What to look for:

1. A hypothesis h(x) = θ₀ + θ₁x is a whole function (a line) in the hypothesis space; its weights
   θ = (θ₀, θ₁) are a single point in the weight space, where the cost J(θ) lives.
2. Gradient descent moves the point in weight space while the line moves in hypothesis space.
3. The same PyTorch recipe (model, loss, optimizer) trains logistic regression, which is a single neuron.

`SAVE_FIGS = True` (first code cell after the setup cell) saves the figures to `figures/`.
