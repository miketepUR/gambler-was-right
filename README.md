# The Gambler Was Right — Reproduction Code and Data

<!-- DOI badge will be added here after the Zenodo release -->

Reproduction package for:

> Teplinsky, M. E. (2026). *The Gambler Was Right: A Reproducible Challenge to
> Strategic Indifference in Fair Coin Sequences.* Manuscript in preparation.

Two players observe the same computationally generated fair coin flip
sequences and place identical 9-bet anti-continuation wagers; they differ
only in entry criterion (streak-threshold entry vs. entry at every direction
change). The scripts here generate all sequences, run both players, apply the
per-shoe equalization protocol, and print every table reported in the paper.

All results are deterministic given the specified seeds. No external
dependencies beyond the Python 3.6+ standard library.

## Repository layout

```
scripts/
  appendix_b_experiment_v3_br_only.py   Primary experiment (paper Appendix; all paper tables)
  concordance_spectrum.py               Supplementary concordance-spectrum variant
seeds.txt                               The five PRNG seeds used everywhere
results/
  appendix_b_output.txt                 Full console output of the primary experiment
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
The output should match `results/appendix_b_output.txt` exactly — every
quantity is deterministic given the seeds hard-coded in the script.

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
per seed into the working directory.

## Configuration (both experiments)

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

The code is released under the MIT License (see `LICENSE`). The manuscript
text is not part of this repository.
