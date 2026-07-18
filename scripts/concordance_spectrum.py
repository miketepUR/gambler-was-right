#!/usr/bin/env python3
"""
CONCORDANCE SPECTRUM EXPERIMENT

Varies the concordance parameter p to control what fraction of MK's entries
share TX's streak domain (heads) vs. the opposite domain (tails).

TX is fixed: heads-only, unidirectional across all C1-C7 configurations.
MK varies: entries filtered by concordance parameter p.
C_BI: standard bidirectional benchmark (both players enter on both sides).

Based on appendix_b_experiment_v3_br_only.py
"""

import random
import math
import csv
import time

# ============================================================
# CONFIGURATION
# ============================================================

PHASE = 2  # 1 = quick check (T4, 20K shoes, 30 eq trials)
           # 2 = full run (T3-T7, 100K shoes, 100 eq trials)

SHOE_LENGTH = 80
BUST_STEPS = 9
STOP_ENTERING = 65
SEEDS = [42, 123, 456, 789, 1001]

if PHASE == 1:
    THRESHOLDS = [4]
    N_PER_SEED = 20000
    EQ_TRIALS = 30
else:
    THRESHOLDS = [3, 4, 5, 6, 7]
    N_PER_SEED = 100000
    EQ_TRIALS = 100

CONFIGS = [
    ('C1',  1.00),
    ('C2',  0.90),
    ('C3',  0.75),
    ('C4',  0.50),
    ('C5',  0.25),
    ('C6',  0.10),
    ('C7',  0.00),
    ('C_BI', None),   # bidirectional benchmark
]

MARKOV_PRED = (0.5 ** BUST_STEPS) * 100  # 0.1953125%

# ============================================================
# CORE FUNCTIONS (from base script, unchanged)
# ============================================================

def generate_shoe():
    """Generate one shoe of SHOE_LENGTH fair coin flips as a string."""
    return ''.join(random.choice('HT') for _ in range(SHOE_LENGTH))


def extract_streaks(seq):
    """Extract maximal runs from a sequence. Returns [(start, side, length), ...]."""
    if len(seq) < 2:
        return []
    streaks = []
    start = 0
    for i in range(1, len(seq)):
        if seq[i] != seq[start]:
            streaks.append((start, seq[start], i - start))
            start = i
    streaks.append((start, seq[start], len(seq) - start))
    return streaks

# ============================================================
# ENTRY DETECTION
# ============================================================

def get_tx_entries(streaks, threshold, heads_only):
    """
    TX entries for a given threshold.
    heads_only=True: enter only on H-side streaks (C1-C7).
    heads_only=False: enter on both sides (C_BI).
    Returns list of bools (True = busted).
    """
    entries = []
    for start_pos, side, slen in streaks:
        if heads_only and side != 'H':
            continue
        if slen >= threshold and start_pos + threshold <= STOP_ENTERING:
            entries.append((slen - threshold) >= BUST_STEPS)
    return entries


def get_mk_entries(streaks, concordance_p, rng):
    """
    MK entries with concordance filtering.
    concordance_p=None: include all direction changes (C_BI).
    concordance_p=float: include H-side with prob p, T-side with prob (1-p).
    rng: random.Random instance for stochastic filtering.
    Returns list of (busted: bool, side: str).
    """
    entries = []
    for start_pos, side, slen in streaks:
        if start_pos == 0:
            continue
        if start_pos + 1 > STOP_ENTERING:
            continue

        if concordance_p is not None:
            if side == 'H':
                if concordance_p < 1.0 and rng.random() >= concordance_p:
                    continue
            else:
                opp = 1.0 - concordance_p
                if opp < 1.0 and rng.random() >= opp:
                    continue

        busted = slen >= BUST_STEPS + 1
        entries.append((busted, side))
    return entries

# ============================================================
# PEARSON CORRELATION (online single-pass accumulator)
# ============================================================

class PearsonAccum:
    """Accumulates (x, y) pairs and computes Pearson r without storing them."""
    def __init__(self):
        self.n = 0
        self.sx = self.sy = self.sxy = self.sx2 = self.sy2 = 0.0

    def add(self, x, y):
        self.n += 1
        self.sx += x
        self.sy += y
        self.sxy += x * y
        self.sx2 += x * x
        self.sy2 += y * y

    def compute(self):
        """Returns (r, p_value) or (None, None) if insufficient data."""
        if self.n < 3:
            return None, None
        dx = self.n * self.sx2 - self.sx ** 2
        dy = self.n * self.sy2 - self.sy ** 2
        if dx <= 0 or dy <= 0:
            return None, None
        r = (self.n * self.sxy - self.sx * self.sy) / math.sqrt(dx * dy)
        r = max(-1.0, min(1.0, r))
        if abs(r) >= 1.0:
            return r, 0.0
        t_stat = r * math.sqrt(self.n - 2) / math.sqrt(1 - r * r)
        p_val = 2 * (1 - 0.5 * (1 + math.erf(abs(t_stat) / math.sqrt(2))))
        return r, p_val

# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_experiment():
    all_results = []
    corr_accum = {cfg: PearsonAccum() for cfg, _ in CONFIGS}
    t_start = time.time()

    for seed in SEEDS:
        seed_t0 = time.time()
        print(f"\n  Seed {seed}: generating {N_PER_SEED:,} shoes...")
        random.seed(seed)
        shoes = [generate_shoe() for _ in range(N_PER_SEED)]
        print(f"    Generated in {time.time() - seed_t0:.1f}s")

        for cfg_idx, (cfg_name, p_val) in enumerate(CONFIGS):
            cfg_t0 = time.time()
            heads_only_tx = (cfg_name != 'C_BI')
            conc_p = p_val if cfg_name != 'C_BI' else None
            conc_rng = random.Random(seed * 100 + cfg_idx + 12345)

            # --------------------------------------------------
            # Combined pass: MK (threshold-independent) + TX (all thresholds)
            # Computes streaks once per shoe, reuses for both.
            # --------------------------------------------------
            shoe_mk_busts = []       # list of lists of bool
            mk_full_total = 0
            mk_full_busts = 0
            mk_h_count = 0
            mk_t_count = 0

            tx_data = {t: {'counts': [], 'total': 0, 'busts': 0}
                       for t in THRESHOLDS}

            for si in range(N_PER_SEED):
                streaks = extract_streaks(shoes[si])

                # MK entries with concordance filtering
                mk_ents = get_mk_entries(streaks, conc_p, conc_rng)
                bust_flags = [b for b, _ in mk_ents]
                shoe_mk_busts.append(bust_flags)
                mk_full_total += len(mk_ents)
                mk_full_busts += sum(bust_flags)
                for _, side in mk_ents:
                    if side == 'H':
                        mk_h_count += 1
                    else:
                        mk_t_count += 1

                # TX entries for every threshold
                for t in THRESHOLDS:
                    tx_ents = get_tx_entries(streaks, t, heads_only_tx)
                    tx_data[t]['counts'].append(len(tx_ents))
                    tx_data[t]['total'] += len(tx_ents)
                    tx_data[t]['busts'] += sum(tx_ents)

            mk_full_rate = (mk_full_busts / mk_full_total * 100
                            if mk_full_total > 0 else 0)

            # --------------------------------------------------
            # Equalization + stats per threshold
            # --------------------------------------------------
            for t in THRESHOLDS:
                shoe_tx_counts = tx_data[t]['counts']
                tx_total = tx_data[t]['total']
                tx_busts = tx_data[t]['busts']
                tx_rate = tx_busts / tx_total * 100 if tx_total > 0 else 0

                # Pre-filter qualifying shoes (tc > 0 and MK pool >= tc)
                qual_shoes = []
                total_eq_tc = 0
                for si in range(N_PER_SEED):
                    tc = shoe_tx_counts[si]
                    ml = shoe_mk_busts[si]
                    if tc > 0 and len(ml) >= tc:
                        qual_shoes.append((si, tc, ml))
                        total_eq_tc += tc

                eq_busts_list = []
                do_corr = (t == 4)
                if do_corr:
                    shoe_eq_bust_sum = [0.0] * N_PER_SEED
                    shoe_eq_trial_n = [0] * N_PER_SEED

                for trial in range(EQ_TRIALS):
                    random.seed(seed * 1000 + t * 100 + trial + 77777)
                    eb = 0
                    for si, tc, ml in qual_shoes:
                        samp_busts = sum(random.sample(ml, tc))
                        eb += samp_busts
                        if do_corr:
                            shoe_eq_bust_sum[si] += samp_busts
                            shoe_eq_trial_n[si] += 1
                    eq_busts_list.append(eb)

                avg_eq_busts = (sum(eq_busts_list) / len(eq_busts_list)
                                if eq_busts_list else 0)
                avg_eq_total = float(total_eq_tc)
                mk_eq_rate = (avg_eq_busts / avg_eq_total * 100
                              if avg_eq_total > 0 else 0)

                adv = ((tx_rate / mk_eq_rate - 1) * 100
                       if mk_eq_rate > 0 else 0)

                # Per-seed Z score (two-proportion test)
                z = 0.0
                n1 = tx_total
                n2 = avg_eq_total if avg_eq_total > 0 else 1
                if n1 > 0 and n2 > 0:
                    pooled = (tx_busts + avg_eq_busts) / (n1 + n2)
                    if 0 < pooled < 1:
                        se = math.sqrt(
                            pooled * (1 - pooled) * (1/n1 + 1/n2))
                        if se > 0:
                            z = (tx_rate/100 - mk_eq_rate/100) / se

                # Per-shoe correlation at T4
                if do_corr:
                    for si in range(N_PER_SEED):
                        tc = shoe_tx_counts[si]
                        trials_n = shoe_eq_trial_n[si]
                        if tc > 0 and trials_n > 0:
                            avg_bust_rate = (
                                shoe_eq_bust_sum[si] / trials_n) / tc
                            corr_accum[cfg_name].add(tc, avg_bust_rate)

                all_results.append({
                    'config': cfg_name,
                    'p': p_val,
                    'threshold': t,
                    'seed': seed,
                    'tx_total': tx_total,
                    'tx_busts': tx_busts,
                    'tx_rate': tx_rate,
                    'mk_full_total': mk_full_total,
                    'mk_full_busts': mk_full_busts,
                    'mk_full_rate': mk_full_rate,
                    'mk_eq_busts': avg_eq_busts,
                    'mk_eq_total': avg_eq_total,
                    'mk_eq_rate': mk_eq_rate,
                    'advantage': adv,
                    'z': z,
                    'mk_h': mk_h_count,
                    'mk_t': mk_t_count,
                })

            elapsed = time.time() - cfg_t0
            r = all_results[-1]
            p_str = f"{p_val:.2f}" if p_val is not None else "bi"
            print(f"    {cfg_name:>4} p={p_str:>4}: "
                  f"TX={r['tx_rate']:.4f}% MK_eq={r['mk_eq_rate']:.4f}% "
                  f"adv={r['advantage']:+.1f}% z={r['z']:+.2f} ({elapsed:.1f}s)")

        print(f"  Seed {seed} done: {time.time() - seed_t0:.1f}s")

    runtime = time.time() - t_start
    print(f"\n  Total runtime: {runtime:.1f}s ({runtime/60:.1f} min)")
    return all_results, corr_accum, runtime

# ============================================================
# VERIFICATION CHECKS
# ============================================================

def run_verification(results):
    print("\n" + "=" * 80)
    print("VERIFICATION CHECKS")
    print("=" * 80)
    markov = 0.5 ** BUST_STEPS
    all_pass = True

    # CHECK 1: TX per-entry bust rate ~ 0.1953% across all configs
    print("\n  CHECK 1: TX per-entry bust rate ~ 0.1953% (1/512)")
    for cfg, _ in CONFIGS:
        for t in THRESHOLDS:
            sub = [r for r in results
                   if r['config'] == cfg and r['threshold'] == t]
            tx_e = sum(r['tx_total'] for r in sub)
            tx_b = sum(r['tx_busts'] for r in sub)
            rate = tx_b / tx_e * 100 if tx_e > 0 else 0
            dev = abs(rate/100 - markov) / markov * 100
            ok = "PASS" if dev < 5 else "FAIL"
            if ok == "FAIL":
                all_pass = False
            print(f"    {cfg:>4} T{t}: {rate:.4f}% (dev {dev:.2f}%) {ok}")

    # CHECK 2: TX entry counts identical across C1-C7 per seed+threshold
    print("\n  CHECK 2: TX counts identical across C1-C7 per seed")
    for seed in SEEDS:
        for t in THRESHOLDS:
            counts = {}
            for cfg, _ in CONFIGS:
                if cfg == 'C_BI':
                    continue
                row = [r for r in results
                       if r['config'] == cfg and r['seed'] == seed
                       and r['threshold'] == t][0]
                counts[cfg] = row['tx_total']
            vals = list(counts.values())
            ok = "PASS" if len(set(vals)) == 1 else "FAIL"
            if ok == "FAIL":
                all_pass = False
            print(f"    Seed {seed} T{t}: {vals[0]:,} (all same: {ok})")

    # CHECK 3: C1 and C7 produce different MK equalized rates
    print("\n  CHECK 3: C1 vs C7 MK equalized rates differ")
    for t in THRESHOLDS:
        c1 = [r for r in results
              if r['config'] == 'C1' and r['threshold'] == t]
        c7 = [r for r in results
              if r['config'] == 'C7' and r['threshold'] == t]
        c1_rate = sum(r['mk_eq_rate'] for r in c1) / len(c1)
        c7_rate = sum(r['mk_eq_rate'] for r in c7) / len(c7)
        diff = abs(c1_rate - c7_rate)
        ok = "PASS" if diff > 0.001 else "FAIL"
        if ok == "FAIL":
            all_pass = False
        print(f"    T{t}: C1={c1_rate:.4f}% C7={c7_rate:.4f}% "
              f"diff={diff:.4f}pp {ok}")

    # CHECK 5: MK full per-entry rate ~ 0.1953% across all configs
    print("\n  CHECK 5: MK full (non-equalized) rate ~ 0.1953%")
    for cfg, _ in CONFIGS:
        seen = set()
        mk_e = mk_b = 0
        for r in results:
            if r['config'] != cfg:
                continue
            key = (r['config'], r['seed'])
            if key in seen:
                continue
            seen.add(key)
            mk_e += r['mk_full_total']
            mk_b += r['mk_full_busts']
        rate = mk_b / mk_e * 100 if mk_e > 0 else 0
        dev = abs(rate/100 - markov) / markov * 100
        ok = "PASS" if dev < 5 else "FAIL"
        if ok == "FAIL":
            all_pass = False
        print(f"    {cfg:>4}: {rate:.4f}% (dev {dev:.2f}%) {ok}")

    print(f"\n  Overall: {'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED'}")
    return all_pass

# ============================================================
# OUTPUT TABLES
# ============================================================

def print_tables(results, corr_accum):
    # ---- TABLE 1: Full Results Grid ----
    print("\n" + "=" * 80)
    print("TABLE 1: Full Results Grid")
    print("=" * 80)
    print(f"  {'Config':>6} {'p':>5} {'T':>2} {'TX_Entries':>11} "
          f"{'TX_Busts':>9} {'TX_Rate%':>9} {'MK_Eq_Busts':>12} "
          f"{'MK_Eq_Rate%':>12} {'Advantage%':>11} {'Comb_Z':>9}")
    print(f"  {'-' * 93}")

    for cfg, pv in CONFIGS:
        for t in THRESHOLDS:
            sub = [r for r in results
                   if r['config'] == cfg and r['threshold'] == t]
            tx_e = sum(r['tx_total'] for r in sub)
            tx_b = sum(r['tx_busts'] for r in sub)
            tx_rate = tx_b / tx_e * 100 if tx_e > 0 else 0
            mk_eq_b = sum(r['mk_eq_busts'] for r in sub)
            mk_eq_t = sum(r['mk_eq_total'] for r in sub)
            mk_eq_rate = (mk_eq_b / mk_eq_t * 100
                          if mk_eq_t > 0 else 0)
            adv = ((tx_rate / mk_eq_rate - 1) * 100
                   if mk_eq_rate > 0 else 0)
            per_seed_zs = [r['z'] for r in sub]
            comb_z = (sum(per_seed_zs) / math.sqrt(len(per_seed_zs))
                      if per_seed_zs else 0)
            ps = f"{pv:.2f}" if pv is not None else "bidir"
            print(f"  {cfg:>6} {ps:>5} {t:>2} {tx_e:>11,} "
                  f"{tx_b:>9,} {tx_rate:>8.4f}% {mk_eq_b:>12.1f} "
                  f"{mk_eq_rate:>11.4f}% {adv:>+10.1f}% {comb_z:>+9.2f}")

    # ---- TABLE 2: Advantage vs Concordance ----
    print("\n" + "=" * 80)
    print("TABLE 2: Advantage vs. Concordance (Key Table)")
    print("=" * 80)
    hdr = f"  {'Config':>6} {'p':>5}"
    for t in THRESHOLDS:
        hdr += f"  {'T'+str(t)+'_Adv%':>9}"
    print(hdr)
    print(f"  {'-' * (12 + 11 * len(THRESHOLDS))}")

    for cfg, pv in CONFIGS:
        ps = f"{pv:.2f}" if pv is not None else "bidir"
        line = f"  {cfg:>6} {ps:>5}"
        for t in THRESHOLDS:
            sub = [r for r in results
                   if r['config'] == cfg and r['threshold'] == t]
            tx_e = sum(r['tx_total'] for r in sub)
            tx_b = sum(r['tx_busts'] for r in sub)
            tx_rate = tx_b / tx_e * 100 if tx_e > 0 else 0
            mk_eq_b = sum(r['mk_eq_busts'] for r in sub)
            mk_eq_t = sum(r['mk_eq_total'] for r in sub)
            mk_eq_rate = (mk_eq_b / mk_eq_t * 100
                          if mk_eq_t > 0 else 0)
            adv = ((tx_rate / mk_eq_rate - 1) * 100
                   if mk_eq_rate > 0 else 0)
            line += f"  {adv:>+8.2f}%"
        print(line)

    # ---- TABLE 3: Per-Sequence Correlation (T4) ----
    print("\n" + "=" * 80)
    print("TABLE 3: Per-Sequence Correlation (T4)")
    print("=" * 80)
    print(f"  {'Config':>6} {'p':>5} {'Corr_r':>10} {'p_value':>14} "
          f"{'n_shoes':>10}")
    print(f"  {'-' * 50}")

    for cfg, pv in CONFIGS:
        acc = corr_accum[cfg]
        r_val, p_cor = acc.compute()
        ps = f"{pv:.2f}" if pv is not None else "bidir"
        if r_val is not None:
            if p_cor < 1e-15:
                pcs = "<1e-15"
            elif p_cor < 0.001:
                pcs = f"{p_cor:.2e}"
            else:
                pcs = f"{p_cor:.6f}"
            print(f"  {cfg:>6} {ps:>5} {r_val:>+10.6f} {pcs:>14} "
                  f"{acc.n:>10,}")
        else:
            print(f"  {cfg:>6} {ps:>5} {'N/A':>10} {'N/A':>14} "
                  f"{acc.n:>10,}")

    # ---- TABLE 4: MK Entry Composition ----
    print("\n" + "=" * 80)
    print("TABLE 4: MK Entry Composition (before equalization)")
    print("=" * 80)
    print(f"  {'Config':>6} {'p':>5} {'Avg_MK_H':>10} {'Avg_MK_T':>10} "
          f"{'Avg_MK_Tot':>11} {'Avg_TX':>8} {'H_frac%':>8}")
    print(f"  {'-' * 63}")

    total_shoes = N_PER_SEED * len(SEEDS)
    for cfg, pv in CONFIGS:
        seen = set()
        mk_h = mk_t = 0
        for r in results:
            if r['config'] != cfg:
                continue
            key = (r['config'], r['seed'])
            if key in seen:
                continue
            seen.add(key)
            mk_h += r['mk_h']
            mk_t += r['mk_t']

        # TX entries at T4 for comparison
        tx_e = sum(r['tx_total'] for r in results
                   if r['config'] == cfg and r['threshold'] == 4)

        avg_h = mk_h / total_shoes
        avg_t = mk_t / total_shoes
        avg_tot = (mk_h + mk_t) / total_shoes
        avg_tx = tx_e / total_shoes
        h_frac = mk_h / (mk_h + mk_t) * 100 if (mk_h + mk_t) > 0 else 0
        ps = f"{pv:.2f}" if pv is not None else "bidir"
        print(f"  {cfg:>6} {ps:>5} {avg_h:>10.2f} {avg_t:>10.2f} "
              f"{avg_tot:>11.2f} {avg_tx:>8.2f} {h_frac:>7.1f}%")

# ============================================================
# CSV EXPORT
# ============================================================

def export_csv(results):
    print("\n" + "=" * 80)
    print("CSV EXPORT")
    print("=" * 80)
    for seed in SEEDS:
        fname = f"concordance_spectrum_seed_{seed}.csv"
        seed_rows = [r for r in results if r['seed'] == seed]
        with open(fname, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['config', 'p', 'threshold', 'seed',
                        'tx_entries', 'tx_busts',
                        'mk_eq_busts', 'mk_eq_rate',
                        'advantage', 'z_score'])
            for r in seed_rows:
                ps = f"{r['p']:.2f}" if r['p'] is not None else "bidir"
                w.writerow([
                    r['config'], ps, r['threshold'], r['seed'],
                    r['tx_total'], r['tx_busts'],
                    f"{r['mk_eq_busts']:.1f}",
                    f"{r['mk_eq_rate']:.4f}",
                    f"{r['advantage']:.2f}",
                    f"{r['z']:.4f}",
                ])
        print(f"  Saved {fname}")

# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 80)
    print("CONCORDANCE SPECTRUM EXPERIMENT")
    print(f"Phase {PHASE}: {'Quick check (T4 only)' if PHASE == 1 else 'Full run (T3-T7)'}")
    print(f"  {len(CONFIGS)} configs x {len(SEEDS)} seeds x "
          f"{N_PER_SEED:,} shoes x {len(THRESHOLDS)} threshold(s)")
    print(f"  Total shoes per config: {N_PER_SEED * len(SEEDS):,}")
    print(f"  EQ_TRIALS = {EQ_TRIALS}")
    print(f"  SHOE_LENGTH = {SHOE_LENGTH}, BUST_STEPS = {BUST_STEPS}, "
          f"STOP_ENTERING = {STOP_ENTERING}")
    print("=" * 80)

    results, corr, runtime = run_experiment()
    run_verification(results)
    print_tables(results, corr)
    export_csv(results)

    print("\n" + "=" * 80)
    print("IMPLEMENTATION NOTES")
    print("=" * 80)
    print("  - TX is heads-only for C1-C7; bidirectional for C_BI.")
    print("  - MK concordance filtering uses a separate RNG per config+seed")
    print("    (random.Random(seed*100 + cfg_idx + 12345)).")
    print("  - Equalization skips shoes where MK pool < TX count.")
    print("  - Correlation computed at T4, aggregated across all seeds.")
    print("  - Shoes stored as strings for memory efficiency;")
    print("    streaks recomputed per config (once per shoe).")

    print(f"\n  Phase {PHASE} runtime: {runtime:.1f}s ({runtime/60:.1f} min)")
    print("=" * 80)
