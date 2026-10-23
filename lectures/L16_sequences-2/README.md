# L16 · Sequences II: memory and learning over time

**Notebook:** `L16_memory_lstm.ipynb`. It runs on a laptop CPU in about 30 seconds; no GPU is
needed. It reads `data/` and `saved/` and writes its figures to `figures/`. Section 9 has
exercises.

## Flags

They are in the first code cell after the setup cell.

| Flag | Default | Effect |
|---|---|---|
| `LIVE_RACE` | `True` | Section 2 trains an RNN and an LSTM side by side (about 10 s per network). `False` skips the race. |
| `RUN_GRID` | `False` | `True` recomputes all 54 memory-test runs in section 3 and overwrites `saved/l16_grid.json`. This takes about 30 minutes on one CPU core. |
| `TRAIN_FORECAST` | `False` | `True` retrains the Charlottetown LSTM and GRU for section 8 (about 1 minute). |

## Numbers to expect

These match the lecture slides.

* Race after 1,500 steps: the RNN reaches 49.2% and the LSTM 100%.
* Grid: the RNN is at chance from length 30 on. The LSTM and the GRU reach 100% at every length up to 200.
* Clipping: the gradient norm is 12.6 million before clipping and 1.00 after.
* The hand-built LSTM unit scores 100% at 100 steps and at 1,000 steps.
* Forecast MAE: RNN 2.29 °C, LSTM 2.27 °C, GRU 2.27 °C.

The seeds are fixed, so with the same PyTorch version (2.14.1, CPU) you get exactly these numbers.
Another version, such as Colab's, can shift live-training numbers slightly, but the story holds.

## Files

* `saved/l16_grid.json`: the 54 memory-test runs (3 cells × 6 lengths × 3 seeds), with accuracy,
  steps-to-solve and loss curves.
* `saved/l16_rnn_L100_seed0.pt`, `saved/l16_lstm_L100_seed0.pt`, `saved/l16_gru_L100_seed0.pt`:
  the trained 100-step networks used in sections 4, 6b and 7.
* `saved/l16_forecast_lstm.pt`, `saved/l16_forecast_gru.pt`, and the L15 RNN `saved/l15_rnn.pt`:
  the forecasters compared in section 8.
* `data/charlottetown_daily_2013_2025.csv`: the Charlottetown daily data from L15.

## Data source and terms

`data/charlottetown_daily_2013_2025.csv` comes from Environment and Climate Change Canada (ECCC),
Historical Climate Data, [climate.weather.gc.ca](https://climate.weather.gc.ca): station
Charlottetown A (climate ID 8300301, station ID 50621), daily data downloaded 8 October 2026.

Based on Environment and Climate Change Canada data. ECCC provides the data free of charge under its
[terms of use](https://climate.weather.gc.ca/prods_servs/attachment1_e.html); anyone who receives the
data from this repository is bound by the same terms, and it may not be passed on for a fee.
Credit ECCC wherever you use the data or figures made from it.
