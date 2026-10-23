# L04 · Why go deep?

**Notebook:** `L04_why_go_deep.ipynb`. Sections 1–5 are the demos from the lecture; section 6 has
four exercises. It needs `torch`, `numpy`, `matplotlib` and `scikit-learn` (all preinstalled in
Colab) and downloads nothing.

## Flags

They are in the first code cell after the setup cell.

| Flag | Default | Effect |
|---|---|---|
| `RUN_TRAINING` | `True` | Trains the two section-3 models. `False` loads `rings_shallow.pt` and `rings_deep.pt` instead. |
| `N_SEEDS_ACT` | `5` | Runs per activation in section 5. `1` is enough for a quick look. |
| `RUN_SWEEP` | `False` | `True` recomputes the section-4 sweeps (5 depths × 5 seeds) from scratch: 25–45 minutes on a laptop CPU. `False` loads `rings_depth_sweep.json`. |

With the defaults the notebook takes about 2 minutes on a CPU; with `RUN_TRAINING = False` and
`N_SEEDS_ACT = 1`, under 20 seconds.

## Files

| File | What it is |
|---|---|
| `rings_depth_sweep.json` | Saved results of the 5-seed sweeps in section 4: depth 1–6 on the narrow rings, and 1 vs 4 hidden layers for k = 2, 4, 6, 8. |
| `rings_shallow.pt`, `rings_deep.pt` | Weights of the two section-3 models (seed 1). |

The notebook writes its figures to `figs/`.

## Numbers to expect

The notebook uses one CPU thread (`torch.set_num_threads(1)`) so runs repeat exactly. The seed-1
models reach 68.4% (1 hidden layer) and 77.6% (4 hidden layers) test accuracy, the same as in the
saved sweep. It was built with PyTorch 2.14 (CPU); another version, such as Colab's, can shift
live-training numbers slightly, but the story holds.
