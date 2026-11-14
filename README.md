# The Gambler Was Right — Paper, Reproduction Code, and Data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21434675.svg)](https://doi.org/10.5281/zenodo.21434675)

> **Notice: superseded (November 2026).** The headline result of this paper
> does not hold. The "equalized differential" comes from how the comparison
> sample was drawn, not from the entry rule. The paper matched the two
> players' bet counts sequence by sequence. That procedure gives extra weight
> to sequences that contain long streaks, which are the sequences where the
> comparison player's catastrophic losses occur. When the comparison sample is
> drawn from all sequences pooled together, the comparison player's rate is
> the same at every threshold, and both players' per-entry rates are
> consistent with the theoretical value of 1/512 (0.1953%).
>
> The code runs and reproduces the paper's tables exactly. What is superseded
> is the interpretation of those tables. The preprint of record is v4.8.1
> (https://doi.org/10.5281/zenodo.21435471). The v4.8.2 PDF in `paper/` is a
> later revision under a different title; it is superseded on the same
> grounds, including its discussion of Table 8b. This repository is kept as
> the record of that work. No further releases are planned.

**Catastrophic-loss rate per entry, by threshold** (5 seeds × 100,000
sequences of 80 flips; the paper's own data, regenerated from the same seeds)

| Threshold T | Selective player | Comparison player, all entries | Comparison player, per-sequence equalized (as published) | Comparison player, pooled equalization |
|---|---|---|---|---|
| 3 | 0.1924% | 0.1942% | 0.2154% | 0.1942% |
| 4 | 0.1920% | 0.1942% | 0.2426% | 0.1942% |
| 5 | 0.1917% | 0.1942% | 0.2977% | 0.1942% |
| 6 | 0.1929% | 0.1942% | 0.4056% | 0.1942% |
| 7 | 0.2017% | 0.1942% | 0.6233% | 0.1942% |

Theoretical per-entry rate: 1/512 = 0.1953%. The fourth column is the
expected value of the paper's equalization procedure given the data; the
fifth is the expected value when the same number of comparison entries is
drawn from the pooled set. Only the fourth column departs from the baseline.

Archive for:

> Teplinsky, M. E. (2026). *The Gambler Was Right: A Reproducible Challenge to
> Strategic Indifference in Fair Coin Sequences.* Preprint, Zenodo.
> https://doi.org/10.5281/zenodo.21435471. Superseded; see the notice above.
> Full text: [`paper/The_Gambler_Was_Right_Teplinsky_2026_v4.8.2.pdf`](paper/The_Gambler_Was_Right_Teplinsky_2026_v4.8.2.pdf)

Two players observe the same computationally generated fair coin flip
sequences and place identical 9-bet anti-continuation wagers; they differ
only in entry criterion (streak-threshold entry vs. entry at every direction
change). The scripts here generate all sequences, run both players, apply the
per-shoe equalization protocol, and print every table reported in the paper.

All results are deterministic given the specified seeds. No external
dependencies beyond the Python 3.6+ standard library.

## Repository layout

```
paper/
  The_Gambler_Was_Right_Teplinsky_2026_v4.8.2.pdf  Full manuscript (PDF)
scripts/
  appendix_b_experiment_v3_br_only.py   Primary experiment (paper Appendix; all paper tables)
  compile_report_v3.py                  Parses the primary output into report + JSON
  robustness/
    run_reversed.py                     Reversed-sequence control run
    scale_shoe40.py … scale_shoe200.py  Shoe-length scaling runs (40/80/120/200 flips)
  concordance_spectrum.py               Supplementary concordance-spectrum variant
seeds.txt                               The five PRNG seeds used everywhere
results/
  v3_main_output.txt                    Original publication run output (2026-05-26)
  v3_parsed.json                        Parsed results (JSON)
  publication_data_report_br_only.md    Compiled publication data report
  appendix_b_output.txt                 Independent re-run (2026-07-18); matches the original
  robustness/
    run_reversed_output.txt             Output of the reversed-sequence control
    scale_shoe*_output.txt              Outputs of the shoe-length scaling runs
  concordance_spectrum/
    concordance_phase2_output.txt       Full console output of the supplementary run
    concordance_spectrum_seed_*.csv     Per-seed raw results (CSV)
LICENSE                                 MIT (code)
CITATION.cff                            Citation metadata
```

## Reproduction

### Primary experiment (all paper tables)

```
python scripts/appendix_b_experiment_v3_br_only.py
```

Runs 5 seeds × 100,000 shoes × 5 thresholds (40,000,000 coin flips) with 100
equalization trials per condition, and prints Tables 1–5 plus verification
checkpoints. Expected runtime: roughly 20–45 minutes depending on hardware.
Every quantity is deterministic given the seeds hard-coded in the script:
the output must match `results/v3_main_output.txt` (original run) and
`results/appendix_b_output.txt` (independent re-run) exactly.

### Robustness checks

```
python scripts/robustness/run_reversed.py
python scripts/robustness/scale_shoe40.py    # likewise shoe80 / shoe120 / shoe200
```

The reversed run replays the identical sequences in reverse order; the
scaling runs repeat the primary experiment at shoe lengths of 40, 120, and
200 flips (shoe80 duplicates the primary configuration). Committed outputs
are in `results/robustness/`.

### Supplementary: concordance spectrum

```
python scripts/concordance_spectrum.py
```

Varies a concordance parameter p ∈ {1.00, 0.90, 0.75, 0.50, 0.25, 0.10, 0.00}
controlling what fraction of the Markov player's entries share the selective
player's streak domain, plus a bidirectional benchmark. The `PHASE` constant
at the top of the script selects a quick check (Phase 1: T4 only, 20,000
shoes/seed, ~1 minute) or the full run (Phase 2: T3–T7, 100,000 shoes/seed,
~45 minutes). The committed results were produced with `PHASE = 2`. The
script prints four tables and writes `concordance_spectrum_seed_<seed>.csv`
per seed into the working directory. This experiment is supplementary and is
not reported in the manuscript.

## Configuration (primary experiment)

| Parameter | Value |
|---|---|
| Shoe length | 80 flips |
| Last enterable position | 65 |
| Bets per entry | 9 |
| Thresholds | 3, 4, 5, 6, 7 |
| Seeds | 42, 123, 456, 789, 1001 |
| Shoes per seed | 100,000 |
| Equalization trials | 100 |

## License

The code in `scripts/` is released under the MIT License (see `LICENSE`).
The manuscript in `paper/` is © 2026 Michael E. Teplinsky, all rights
reserved; it is included for reference and is not covered by the MIT license.
