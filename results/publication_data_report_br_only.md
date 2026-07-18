# PUBLICATION DATA REPORT — BR-ONLY (v3)

Generated from `appendix_b_experiment_v3_br_only.py` and variants in `v3_runs/`.
Date: 2026-05-26

## Configuration

- View: **Direct Sequence (BR) only — no derived views**
- SHOE_LENGTH = 80
- STOP_ENTERING = 65
- BUST_STEPS = 9
- THRESHOLDS = [3, 4, 5, 6, 7]
- SEEDS = [42, 123, 456, 789, 1001]
- N_PER_SEED = 100,000 (500,000 total shoes, 40,000,000 coin flips)
- EQ_TRIALS = 100 (main + reversed); EQ_TRIALS = 10 (SHOE scaling, N=50,000)

Applied audit fixes (per the rerun prompt):

- **Fix 1** (audit LOW-1): monotonicity comparison sense corrected.
- **Fix 2** (audit LOW-2): hardcoded YES replaced with computed check.
- **Fix 4** (audit LOW-3): MK stop check aligned with TX (`start_pos + 1 <= stop`).
- **Fix 5** (audit LOW-4): equalized MK rate divides by actual subsample total `et`, not `tx_total`.
- Fix 3 (derived-view algorithm) **deliberately not applied** — derived views are excluded.
- Verification checkpoints emit during execution (CHECKPOINT / EQ_STABILITY / RATE_CHECK / MONO_CHECK).

---

## TABLE 1: Per-entry catastrophic loss rates by threshold
*Aggregated across 5 seeds = 500,000 shoes.*

| Threshold | TX Entries | TX Losses | TX Rate % | MK Full Rate % | Markov Prediction % | TX Deviation from Markov |
|-----------|-----------:|----------:|----------:|---------------:|--------------------:|-------------------------:|
| T3 | 4,000,807 | 7,699 | 0.1924 | 0.1942 | 0.1953 | -1.49% |
| T4 | 1,968,274 | 3,780 | 0.1920 | 0.1942 | 0.1953 | -1.70% |
| T5 | 969,443 | 1,858 | 0.1917 | 0.1942 | 0.1953 | -1.85% |
| T6 | 476,866 | 920 | 0.1929 | 0.1942 | 0.1953 | -1.24% |
| T7 | 234,950 | 474 | 0.2017 | 0.1942 | 0.1953 | +3.27% |

## TABLE 2: Equalized comparison by threshold
*EQ_TRIALS = 100; aggregated across 5 seeds.*

| Threshold | Entries (both) | TX Losses | MK Eq Losses | Avoided | TX Rate % | MK Eq Rate % | Advantage % |
|-----------|---------------:|----------:|-------------:|--------:|----------:|-------------:|------------:|
| T3 | 4,000,807 | 7,699 | 8,611.1 | +912.1 | 0.1924 | 0.2152 | -10.6 |
| T4 | 1,968,274 | 3,780 | 4,773.2 | +993.2 | 0.1920 | 0.2425 | -20.8 |
| T5 | 969,443 | 1,858 | 2,884.5 | +1,026.5 | 0.1917 | 0.2975 | -35.6 |
| T6 | 476,866 | 920 | 1,943.3 | +1,023.3 | 0.1929 | 0.4075 | -52.7 |
| T7 | 234,950 | 474 | 1,467.6 | +993.6 | 0.2017 | 0.6246 | -67.7 |

## TABLE 2B: Equalized catastrophic losses per coin flip
*40,000,000 total flips = 5 seeds × 100,000 shoes × 80 flips.*

| Threshold | Total Flips | TX Losses | MK Eq Losses | TX Loss/Flip % | MK Eq Loss/Flip % | Gap % |
|-----------|------------:|----------:|-------------:|---------------:|------------------:|------:|
| T3 | 40,000,000 | 7,699 | 8,611.1 | 0.0192 | 0.0215 | -10.6 |
| T4 | 40,000,000 | 3,780 | 4,773.2 | 0.0095 | 0.0119 | -20.8 |
| T5 | 40,000,000 | 1,858 | 2,884.5 | 0.0046 | 0.0072 | -35.6 |
| T6 | 40,000,000 | 920 | 1,943.3 | 0.0023 | 0.0049 | -52.7 |
| T7 | 40,000,000 | 474 | 1,467.6 | 0.0012 | 0.0037 | -67.7 |

## TABLE 3: Statistical significance by threshold
*Per-seed Z scores are computed individually from each seed's TX/MK-eq totals + busts (not derived from the combined Z). Discounted Z = Combined Z / √2 — conservative correction for within-shoe correlation.*

| Threshold | Per-Seed Z (42 / 123 / 456 / 789 / 1001) | Combined Z | Bayes Factor | vs Diaconis (÷2359) | Exceeds 5σ? | Discounted Z (÷√2) | Discounted exceeds 5σ? |
|-----------|------------------------------------------|-----------:|-------------:|--------------------:|:-----------:|-------------------:|:----------------------:|
| T3 | -2.16 / -3.78 / -3.88 / -2.53 / -3.65 | -7.16 | 1.3e+11 | 6e+07 | Yes | -5.06 | Yes |
| T4 | -4.17 / -4.81 / -5.76 / -4.28 / -5.05 | -10.76 | 1.4e+25 | 6e+21 | Yes | -7.61 | Yes |
| T5 | -6.37 / -6.89 / -7.02 / -6.41 / -6.68 | -14.93 | 2.4e+48 | 1e+45 | Yes | -10.55 | Yes |
| T6 | -8.39 / -8.27 / -8.12 / -8.54 / -9.52 | -19.16 | 4.8e+79 | 2e+76 | Yes | -13.54 | Yes |
| T7 | -10.43 / -10.21 / -9.47 / -9.86 / -10.56 | -22.60 | 8.5e+110 | 4e+107 | Yes | -15.98 | Yes |

## TABLE 4: Advantage by seed and threshold

| Threshold | Seed 42 | Seed 123 | Seed 456 | Seed 789 | Seed 1001 | Average | Std Dev |
|-----------|--------:|---------:|---------:|---------:|----------:|--------:|--------:|
| T3 | -7.2% | -12.5% | -12.9% | -8.4% | -11.9% | -10.6% | 2.57% |
| T4 | -18.2% | -20.8% | -24.8% | -18.7% | -21.5% | -20.8% | 2.63% |
| T5 | -34.2% | -36.8% | -37.3% | -34.2% | -35.4% | -35.6% | 1.44% |
| T6 | -51.9% | -51.5% | -50.4% | -52.3% | -57.1% | -52.6% | 2.59% |
| T7 | -69.2% | -68.8% | -64.5% | -66.0% | -69.9% | -67.7% | 2.29% |

## TABLE 5: Side symmetry (H vs T) at T = 4
*Per-side TX vs MK-eq, equalized within each side per shoe (per Note 6 of the rerun prompt).*

| Side | TX Entries | TX Losses | TX Rate % | MK Eq Rate % | Advantage % |
|------|-----------:|----------:|----------:|-------------:|------------:|
| H | 984,601 | 1,904 | 0.1934 | 0.2879 | -32.8 |
| T | 983,673 | 1,876 | 0.1907 | 0.2884 | -33.9 |

## TABLE 6: SHOE_LENGTH Scaling
*BR-only; N_PER_SEED = 50,000; EQ_TRIALS = 10 for throughput.*

| SHOE_LENGTH | STOP | Threshold | TX Rate % | MK Eq Rate % | Advantage % | Combined Z | 5σ? |
|-------------|-----:|-----------|----------:|-------------:|------------:|-----------:|:---:|
| 40 | 32 | T3 | 0.1832 | 0.2399 | -23.6 | -8.59 | Yes |
| 40 | 32 | T4 | 0.1860 | 0.3021 | -38.5 | -11.40 | Yes |
| 40 | 32 | T5 | 0.1849 | 0.4297 | -57.0 | -14.91 | Yes |
| 40 | 32 | T6 | 0.1988 | 0.6880 | -71.1 | -17.26 | Yes |
| 40 | 32 | T7 | 0.2071 | 1.2041 | -82.8 | -19.42 | Yes |
| 80 | 65 | T3 | 0.1906 | 0.2154 | -11.5 | -5.54 | Yes |
| 80 | 65 | T4 | 0.1908 | 0.2454 | -22.3 | -8.21 | Yes |
| 80 | 65 | T5 | 0.1885 | 0.2992 | -37.0 | -11.06 | Yes |
| 80 | 65 | T6 | 0.1938 | 0.4115 | -52.9 | -13.69 | Yes |
| 80 | 65 | T7 | 0.1980 | 0.6153 | -67.8 | -15.92 | Yes |
| 120 | 97 | T3 | 0.1912 | 0.2083 | -8.2 | -4.69 | No |
| 120 | 97 | T4 | 0.1916 | 0.2265 | -15.4 | -6.58 | Yes |
| 120 | 97 | T5 | 0.1932 | 0.2592 | -25.5 | -8.41 | Yes |
| 120 | 97 | T6 | 0.1971 | 0.3243 | -39.2 | -10.63 | Yes |
| 120 | 97 | T7 | 0.1928 | 0.4686 | -58.9 | -14.43 | Yes |
| 200 | 162 | T3 | 0.1944 | 0.2032 | -4.3 | -3.15 | No |
| 200 | 162 | T4 | 0.1947 | 0.2135 | -8.8 | -4.66 | No |
| 200 | 162 | T5 | 0.1946 | 0.2339 | -16.8 | -6.70 | Yes |
| 200 | 162 | T6 | 0.1984 | 0.2788 | -28.8 | -9.17 | Yes |
| 200 | 162 | T7 | 0.2055 | 0.3551 | -42.1 | -11.09 | Yes |

## TABLE 7: Reversed Polarity Confirmation
*BR-only; EQ_TRIALS = 100; N_PER_SEED = 100,000.*
*TX label now uses the direction-change criterion (was MK). MK label now uses the streak-depth criterion per T (was TX). Equalization subsamples the larger pool down to the smaller per shoe.*

**Aggregate (from the symmetric relationship — reversed TX rate = main MK-eq rate; reversed MK rate = main TX rate):**

| Threshold | TX (breaks) Rate % | MK Eq (streaks) Rate % | Reversed Advantage % | Direction flipped? |
|-----------|-------------------:|-----------------------:|---------------------:|:------------------:|
| T3 | 0.2152 | 0.1924 | +11.9 | YES |
| T4 | 0.2425 | 0.1920 | +26.3 | YES |
| T5 | 0.2975 | 0.1917 | +55.2 | YES |
| T6 | 0.4075 | 0.1929 | +111.2 | YES |
| T7 | 0.6246 | 0.2017 | +209.7 | YES |

**Per-seed reversed advantages (from reversed run's Table 4 — these are the authoritative per-seed numbers):**

| Threshold | Seed 42 | Seed 123 | Seed 456 | Seed 789 | Seed 1001 | Average |
|-----------|--------:|---------:|---------:|---------:|----------:|--------:|
| T3 | +7.8% | +14.3% | +14.8% | +9.2% | +13.5% | +11.9% |
| T4 | +22.2% | +26.3% | +33.0% | +23.1% | +27.5% | +26.4% |
| T5 | +52.0% | +58.2% | +59.6% | +52.1% | +54.7% | +55.3% |
| T6 | +107.7% | +106.2% | +101.6% | +109.8% | +133.0% | +111.7% |
| T7 | +224.8% | +220.2% | +182.1% | +194.5% | +232.4% | +210.8% |

**Direction flipped at every threshold (aggregate):** YES
**Direction flipped at every threshold × seed (5×5 = 25 cells):** YES

**Implementation note.** The v3 reversed script (`v3_runs/run_reversed.py`) stores the *full* direction-change counts in the `tx_total`/`tx_busts` fields rather than the subsampled counts. This is correct for the per-seed Z-score computation (Table 3 in `v3_runs/run_reversed_output.txt`, which shows +Z values flipped from the main run) and for the per-seed advantages (Table 4, all positive). However the reversed run's *aggregate* Table 2 row treats `tx_busts/tx_total` as a rate over the full count, which yields ~0.1942% (the full direction-change rate) instead of the subsampled rate. The aggregate above uses the symmetric relationship to recover the correct reversed comparison.

## VERIFICATION CHECKSUMS

- **Total shoes processed (main):** 500,000
- **Total coin flips (main):** 40,000,000
- **Total TX entries at T4 (main, BR only):** 1,968,274
- **Total MK entries (main, full pool):** 15,998,087 (= TX-entries count in the reversed run, which is the direction-change pool)
- **All per-entry TX rates within 3% of Markov (main):** NO
- **All per-entry MK rates within 3% of Markov (main):** YES
- **Gradient monotonic across all 25 points (main):** YES
- **Equalization stability (max per-trial std dev, main):** 0.0366 percentage points
- **Reversed polarity flips sign at all thresholds (aggregate):** YES
- **Reversed polarity flips sign at all 25 (T × seed) cells:** YES

---

## Appendix A: Raw console output (main run)

```
================================================================================
THE GAMBLER WAS RIGHT: Experimental Reproduction Script
v3 -- BR-only (Direct Sequence only; no derived views)
Configuration: 5 seeds x 100,000 shoes x 5 thresholds x 1 view (BR)
Total coin flips: 40,000,000
EQ_TRIALS = 100; SHOE_LENGTH = 80; STOP_ENTERING = 65
================================================================================
  Seed 42...
  EQ_STABILITY: Seed 42 T3 -- MK busts range: 1630-1810 across 100 trials
  EQ_STABILITY: Seed 42 T4 -- MK busts range: 885-1013 across 100 trials
  EQ_STABILITY: Seed 42 T5 -- MK busts range: 520-634 across 100 trials
  EQ_STABILITY: Seed 42 T6 -- MK busts range: 335-432 across 100 trials
  EQ_STABILITY: Seed 42 T7 -- MK busts range: 257-341 across 100 trials
  CHECKPOINT: Seed 42 complete. TX entries (all T): 1528442, MK entries: 3200829, TX busts (all T): 3031
  Seed 123...
  EQ_STABILITY: Seed 123 T3 -- MK busts range: 1633-1815 across 100 trials
  EQ_STABILITY: Seed 123 T4 -- MK busts range: 897-1032 across 100 trials
  EQ_STABILITY: Seed 123 T5 -- MK busts range: 519-621 across 100 trials
  EQ_STABILITY: Seed 123 T6 -- MK busts range: 344-443 across 100 trials
  EQ_STABILITY: Seed 123 T7 -- MK busts range: 253-326 across 100 trials
  CHECKPOINT: Seed 123 complete. TX entries (all T): 1532342, MK entries: 3198693, TX busts (all T): 2894
  Seed 456...
  EQ_STABILITY: Seed 456 T3 -- MK busts range: 1632-1776 across 100 trials
  EQ_STABILITY: Seed 456 T4 -- MK busts range: 864-1031 across 100 trials
  EQ_STABILITY: Seed 456 T5 -- MK busts range: 510-625 across 100 trials
  EQ_STABILITY: Seed 456 T6 -- MK busts range: 335-432 across 100 trials
  EQ_STABILITY: Seed 456 T7 -- MK busts range: 238-329 across 100 trials
  CHECKPOINT: Seed 456 complete. TX entries (all T): 1532053, MK entries: 3197150, TX busts (all T): 2845
  Seed 789...
  EQ_STABILITY: Seed 789 T3 -- MK busts range: 1636-1770 across 100 trials
  EQ_STABILITY: Seed 789 T4 -- MK busts range: 879-1015 across 100 trials
  EQ_STABILITY: Seed 789 T5 -- MK busts range: 526-633 across 100 trials
  EQ_STABILITY: Seed 789 T6 -- MK busts range: 338-430 across 100 trials
  EQ_STABILITY: Seed 789 T7 -- MK busts range: 261-348 across 100 trials
  CHECKPOINT: Seed 789 complete. TX entries (all T): 1528196, MK entries: 3200377, TX busts (all T): 3004
  Seed 1001...
  EQ_STABILITY: Seed 1001 T3 -- MK busts range: 1691-1873 across 100 trials
  EQ_STABILITY: Seed 1001 T4 -- MK busts range: 906-1034 across 100 trials
  EQ_STABILITY: Seed 1001 T5 -- MK busts range: 535-646 across 100 trials
  EQ_STABILITY: Seed 1001 T6 -- MK busts range: 348-445 across 100 trials
  EQ_STABILITY: Seed 1001 T7 -- MK busts range: 249-340 across 100 trials
  CHECKPOINT: Seed 1001 complete. TX entries (all T): 1529307, MK entries: 3201038, TX busts (all T): 2957

  RATE_CHECK: T3 -- TX rate: 0.1924% vs Markov 0.1953% -- deviation: 1.47% -- PASS (threshold: 3%)
  RATE_CHECK: T4 -- TX rate: 0.1920% vs Markov 0.1953% -- deviation: 1.67% -- PASS (threshold: 3%)
  RATE_CHECK: T5 -- TX rate: 0.1917% vs Markov 0.1953% -- deviation: 1.87% -- PASS (threshold: 3%)
  RATE_CHECK: T6 -- TX rate: 0.1929% vs Markov 0.1953% -- deviation: 1.22% -- PASS (threshold: 3%)
  RATE_CHECK: T7 -- TX rate: 0.2017% vs Markov 0.1953% -- deviation: 3.29% -- FAIL (threshold: 3%)

  MONO_CHECK: Seed 42 -- T3:-7.2% -> T4:-18.2% -> T5:-34.2% -> T6:-51.9% -> T7:-69.2% -- Monotonic: YES
  MONO_CHECK: Seed 123 -- T3:-12.5% -> T4:-20.8% -> T5:-36.8% -> T6:-51.5% -> T7:-68.8% -- Monotonic: YES
  MONO_CHECK: Seed 456 -- T3:-12.9% -> T4:-24.8% -> T5:-37.3% -> T6:-50.4% -> T7:-64.5% -- Monotonic: YES
  MONO_CHECK: Seed 789 -- T3:-8.4% -> T4:-18.7% -> T5:-34.2% -> T6:-52.3% -> T7:-66.0% -- Monotonic: YES
  MONO_CHECK: Seed 1001 -- T3:-11.9% -> T4:-21.5% -> T5:-35.4% -> T6:-57.1% -> T7:-69.9% -- Monotonic: YES


================================================================================
TABLE 1: Per-entry catastrophic loss rates by threshold
================================================================================
  Threshold   TX Entries  TX Losses   TX Rate   MK Full    Markov
  --------------------------------------------------------------
  T3           4,000,807       7699   0.1924%   0.1942%   0.1953%
  T4           1,968,274       3780   0.1920%   0.1942%   0.1953%
  T5             969,443       1858   0.1917%   0.1942%   0.1953%
  T6             476,866        920   0.1929%   0.1942%   0.1953%
  T7             234,950        474   0.2017%   0.1942%   0.1953%

================================================================================
TABLE 2: Equalized comparison by threshold
================================================================================
    T      Entries   TX Loss    MK Loss    Avoided   TX Rate    MK Rate      Adv
  ----------------------------------------------------------------------------
  T3     4,000,807      7699     8611.1     +912.1   0.1924%    0.2152%   -10.6%
  T4     1,968,274      3780     4773.2     +993.2   0.1920%    0.2425%   -20.8%
  T5       969,443      1858     2884.5    +1026.5   0.1917%    0.2975%   -35.6%
  T6       476,866       920     1943.3    +1023.3   0.1929%    0.4075%   -52.7%
  T7       234,950       474     1467.6     +993.6   0.2017%    0.6246%   -67.7%

================================================================================
TABLE 2B: Equalized catastrophic losses per coin flip
================================================================================
    T          Flips   TX Loss    MK Loss    TX/Flip    MK/Flip      Gap
  --------------------------------------------------------------------
  T3      40,000,000      7699     8611.1    0.0192%    0.0215%   -10.6%
  T4      40,000,000      3780     4773.2    0.0095%    0.0119%   -20.8%
  T5      40,000,000      1858     2884.5    0.0046%    0.0072%   -35.6%
  T6      40,000,000       920     1943.3    0.0023%    0.0049%   -52.7%
  T7      40,000,000       474     1467.6    0.0012%    0.0037%   -67.7%

================================================================================
TABLE 3: Statistical significance by threshold
================================================================================
    T     Z_s42    Z_s123    Z_s456    Z_s789   Z_s1001  Combined Z  Bayes Factor   vs Diaconis  5-sig?    Disc Z Disc 5-sig?
  ------------------------------------------------------------------------------------------------------------------
  T3      -2.16     -3.78     -3.88     -2.53     -3.65       -7.16       1.3e+11         6e+07     Yes     -5.06         Yes
  T4      -4.17     -4.81     -5.76     -4.28     -5.05      -10.76       1.4e+25         6e+21     Yes     -7.61         Yes
  T5      -6.37     -6.89     -7.02     -6.41     -6.68      -14.93       2.4e+48         1e+45     Yes    -10.55         Yes
  T6      -8.39     -8.27     -8.12     -8.54     -9.52      -19.16       4.8e+79         2e+76     Yes    -13.54         Yes
  T7     -10.43    -10.21     -9.47     -9.86    -10.56      -22.60      8.5e+110        4e+107     Yes    -15.98         Yes

================================================================================
TABLE 4: Advantage by seed and threshold (with Std Dev)
================================================================================
    T    Seed 42   Seed 123   Seed 456   Seed 789  Seed 1001    Average   StdDev
  -------------------------------------------------------------------------------
  T3       -7.2%     -12.5%     -12.9%      -8.4%     -11.9%     -10.6%    2.57%
  T4      -18.2%     -20.8%     -24.8%     -18.7%     -21.5%     -20.8%    2.63%
  T5      -34.2%     -36.8%     -37.3%     -34.2%     -35.4%     -35.6%    1.44%
  T6      -51.9%     -51.5%     -50.4%     -52.3%     -57.1%     -52.6%    2.59%
  T7      -69.2%     -68.8%     -64.5%     -66.0%     -69.9%     -67.7%    2.29%

================================================================================
TABLE 5: Side symmetry (H vs T) at T=4
================================================================================
   Side   TX Entries  TX Losses   TX Rate  MK Eq Rate  Advantage
  ----------------------------------------------------------------
      H      984,601       1904   0.1934%     0.2879%     -32.8%
      T      983,673       1876   0.1907%     0.2884%     -33.9%

================================================================================
SUMMARY
================================================================================

  Total sequences: 500,000
  Total coin flips: 40,000,000
  Independent seeds: 5
  Thresholds tested: 5
  Data points: 25
  Gradient monotonic across all 25 points: YES
  Max equalization std dev: 0.0366 percentage points

  Markov prediction (0.5^9): 0.1953%
  All TX per-entry rates within 1.5% of prediction: NO
  All TX per-entry rates within 3.0% of prediction: NO
  All MK per-entry rates within 3.0% of prediction: YES

================================================================================
REPRODUCTION COMPLETE
================================================================================
```