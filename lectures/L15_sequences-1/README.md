# L15 · Sequences I: order and recurrent state

**Notebook:** `L15_sequences_recurrent_state.ipynb`. It runs on a laptop CPU in about 30 seconds;
no GPU is needed. It reads `data/` and `saved/` and writes its figures to `figures/`. Section 9 has
exercises.

## Flags

`TRAIN` is in the first code cell after the setup cell; `REFRESH` is in section 1.

| Flag | Default | Effect |
|---|---|---|
| `TRAIN` | `True` | Trains the 14-day window network and the RNN live. `False` loads `saved/l15_windownet.pt` and `saved/l15_rnn.pt` instead; the numbers are the same. |
| `REFRESH` | `False` | `True` downloads 2013–2025 again from Environment Canada and overwrites the CSV. This needs internet. |

## Numbers to expect

These match the lecture slides. Test mean absolute error (MAE) on 2024–25:

* climatology: 2.93 °C
* persistence: 2.48 °C
* window network: 2.30 °C, with 513 parameters
* RNN: 2.29 °C, with 1,153 parameters

The `nn.RNN` layer has 1,120 parameters, whatever the sequence length.

The seeds are fixed, so with the same PyTorch version (2.14.1, CPU) you get exactly these numbers.
Another version, such as Colab's, can shift live-training numbers slightly, but the story holds.

## Files

* `data/charlottetown_daily_2013_2025.csv`: daily mean, max and min temperature (°C) and total
  precipitation (mm) from 1 Jan 2013 to 31 Dec 2025, 4,748 days. The 136 days with no mean
  temperature are left blank; the notebook fills them by interpolation.
* `saved/l15_windownet.pt` and `saved/l15_rnn.pt`: the trained models.

## Data source and terms

`data/charlottetown_daily_2013_2025.csv` comes from Environment and Climate Change Canada (ECCC),
Historical Climate Data, [climate.weather.gc.ca](https://climate.weather.gc.ca): station
Charlottetown A (climate ID 8300301, station ID 50621), daily data downloaded 8 October 2026.

Based on Environment and Climate Change Canada data. ECCC provides the data free of charge under its
[terms of use](https://climate.weather.gc.ca/prods_servs/attachment1_e.html); anyone who receives the
data from this repository is bound by the same terms, and it may not be passed on for a fee.
Credit ECCC wherever you use the data or figures made from it.
