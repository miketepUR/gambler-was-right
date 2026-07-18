# APPENDIX B: Complete Python Implementation (v3 — BR-only publication run)
#
# This script reproduces the BR-only results that will appear in the paper.
# No external dependencies beyond Python 3.6+ standard library.
# Expected runtime: approximately 20-30 minutes (N=100K, EQ=100, BR only).
#
# v3 changes (from original):
#   - Restricted to the Direct Sequence (BR) view only -- no derived views.
#   - Fix 1 (audit LOW-1): inverted monotonicity check corrected.
#   - Fix 2 (audit LOW-2): hardcoded "YES" check replaced with computation.
#   - Fix 4 (audit LOW-3): MK stop check aligned with TX (start_pos + 1 <= stop).
#   - Fix 5 (audit LOW-4): equalized rate divides by actual subsample total.
#   - DOES NOT apply Fix 3 (the derived-road algorithm change) -- derived
#     roads are irrelevant since this run uses BR only.
#   - Per-seed Z scores are explicitly printed.
#   - Per-side (H/T) equalized comparison at T=4 (Table 5).
#   - Per-side MK tracking added so per-side equalization is possible.
#   - Verification checkpoints emit during execution.
#
# Usage: python appendix_b_experiment_v3_br_only.py
#
# Output: All tables for BR-only publication printed to console.

import random
import math
from collections import defaultdict

# ============================================================
# CONFIGURATION
# ============================================================

SHOE_LENGTH = 120         # v3 Run B (SHOE_LENGTH scaling)
STOP_ENTERING = 97       # proportional (120 * 65/80)
BUST_STEPS = 9            # Number of bets in each entry (both players)
THRESHOLDS = [3, 4, 5, 6, 7]  # Observation depths tested
SEEDS = [42, 123, 456, 789, 1001]  # Independent random seeds
N_PER_SEED = 50000        # v3 Run B: smaller N for scaling-check throughput
EQ_TRIALS = 10            # v3 Run B: lower trials for scaling-check throughput

# ============================================================
# SEQUENCE GENERATION
#
# Each outcome is drawn independently from {H, T} with equal
# probability using Python's Mersenne Twister PRNG.
# No physical medium. No memory. No edge.
# ============================================================

def generate_shoe():
    """Generate one sequence of SHOE_LENGTH fair coin flips."""
    return [random.choice(['H', 'T']) for _ in range(SHOE_LENGTH)]

# ============================================================
# VIEW 1: DIRECT SEQUENCE (BIG ROAD)
#
# Organizes raw outcomes into columns of consecutive identical
# results. Each column is a maximal run of one outcome.
# ============================================================

def build_direct_sequence(outcomes):
    """
    Convert a flat outcome list into columns of consecutive 
    identical outcomes.
    
    Input:  ['H', 'H', 'T', 'T', 'T', 'H']
    Output: [['H', 'H'], ['T', 'T', 'T'], ['H']]
    """
    if not outcomes:
        return []
    columns = [[outcomes[0]]]
    for x in outcomes[1:]:
        if x == columns[-1][0]:
            columns[-1].append(x)
        else:
            columns.append([x])
    return columns

# ============================================================
# VIEWS 2-4: STRUCTURAL COMPARISON VIEWS (DERIVED ROADS)
#
# These algorithms are standardized scoreboard display methods
# used in casinos worldwide. They compare column depths at 
# lookback offsets of 1, 2, and 3 respectively.
#
# Output alphabet: {R, B} (Red, Blue)
# R = structural similarity at this position
# B = structural difference at this position
#
# The R/B encoding has no systematic relationship to the
# original H/T outcomes. It encodes column-depth structure only.
# ============================================================

def build_derived_view(direct_columns, offset):
    """
    Build a derived view from Direct Sequence columns at the
    specified lookback offset.
    
    offset=1: Big Eye Boy (BEB)
    offset=2: Small Road (SR)  
    offset=3: Cockroach Pig (CP)
    
    See Appendix A for full algorithmic specification.
    """
    result = []
    start_col = offset
    
    if len(direct_columns) < start_col + 1:
        return result
    
    for col_idx in range(start_col, len(direct_columns)):
        column = direct_columns[col_idx]
        
        for row_idx in range(len(column)):
            # Skip the very first entry of the starting column
            if col_idx == start_col and row_idx == 0:
                continue
            
            if row_idx == 0:
                # FIRST ROW OF NEW COLUMN
                # Compare depth of preceding column against
                # the column (offset+1) positions back
                prev_depth = len(direct_columns[col_idx - 1])
                
                if (col_idx - offset - 1) >= 0:
                    comp_depth = len(direct_columns[col_idx - offset - 1])
                else:
                    comp_depth = 0
                
                result.append('R' if prev_depth == comp_depth else 'B')
            else:
                # SUBSEQUENT ROWS
                # Check whether current row and previous row
                # both exist (or both don't) in the comparison column
                comp_col = direct_columns[col_idx - offset]
                current_exists = row_idx < len(comp_col)
                previous_exists = (row_idx - 1) < len(comp_col)
                
                result.append('R' if current_exists == previous_exists else 'B')
    
    return result

# ============================================================
# STREAK ANALYSIS
#
# Extract all streaks (maximal runs of identical outcomes) from
# any binary sequence. Used for both Direct Sequence and
# derived views.
# ============================================================

def extract_streaks(sequence):
    """
    Extract all streaks from a binary sequence.
    
    Returns: list of (start_position, side, length) tuples
    
    A streak is a maximal run of consecutive identical values.
    Example: ['R', 'R', 'B', 'B', 'B', 'R'] produces:
        [(0, 'R', 2), (2, 'B', 3), (5, 'R', 1)]
    """
    if len(sequence) < 2:
        return []
    
    streaks = []
    start = 0
    
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[start]:
            streaks.append((start, sequence[start], i - start))
            start = i
    streaks.append((start, sequence[start], len(sequence) - start))
    
    return streaks

# ============================================================
# ENTRY DETECTION
#
# Both player strategies are implemented here. The critical
# design choice: both players make exactly BUST_STEPS (9) bets.
# They differ ONLY in what they observed before placing their
# first bet.
#
# SELECTIVE PLAYER (TX): Enters when a "fresh" streak of
#   exactly T consecutive identical outcomes is detected.
#   "Fresh" means the streak began exactly T positions ago
#   (the preceding outcome was different). This ensures each
#   streak produces exactly one TX entry at its threshold depth.
#
# MARKOV PLAYER (MK): Enters at every direction change — the
#   first position of a new streak. Bets against the new
#   direction continuing.
#
# BUST CONDITION (both players): All BUST_STEPS bets lose.
#   For TX: the streak extends BUST_STEPS beyond the observed T.
#   For MK: the new streak extends BUST_STEPS beyond the
#   observed direction change.
#   Both conditions require streak_length >= threshold + BUST_STEPS.
# ============================================================

def analyze_entries(streaks, stop_position):
    """
    For a list of streaks from any view, identify all TX entries
    (at each threshold) and all MK entries, along with their
    bust status.
    
    stop_position: last position where a new entry can begin.
    
    Returns:
        tx_entries: dict {threshold: [(busted: bool), ...]}
        mk_entries: [(busted: bool), ...]
    """
    tx_entries = {t: [] for t in THRESHOLDS}
    mk_entries = []
    
    for start_pos, side, streak_len in streaks:
        # --- TX entries ---
        # A streak of length L produces one TX entry for each
        # threshold T <= L, at position start_pos + T.
        # The entry is "fresh" by construction because we iterate
        # over maximal streaks — the outcome at start_pos - 1
        # is guaranteed to be different (or start_pos is 0).
        for t in THRESHOLDS:
            if streak_len >= t and start_pos + t <= stop_position:
                # Bust if streak continues BUST_STEPS beyond observed T
                busted = (streak_len - t) >= BUST_STEPS
                tx_entries[t].append(busted)
        
        # --- MK entries ---
        # Enter at the first position of each new streak
        # (every direction change). Skip the very first streak
        # in the sequence (no preceding direction change).
        # v3 Fix 4: stop check aligned with TX. The first MK bet
        # is at start_pos + 1, so gate on (start_pos + 1) <= stop.
        if start_pos > 0 and start_pos + 1 <= stop_position:
            # MK observes 1 outcome (the direction change itself)
            # and bets against continuation for BUST_STEPS bets.
            # Bust if the streak runs for BUST_STEPS + 1 or more
            # (1 observed + BUST_STEPS lost = streak of BUST_STEPS + 1).
            busted = streak_len >= BUST_STEPS + 1
            mk_entries.append(busted)
    
    return tx_entries, mk_entries

# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_experiment():
    """Run the complete experiment across all seeds and thresholds."""
    
    all_results = []  # Collects per-seed, per-threshold results
    
    for seed in SEEDS:
        print(f"  Seed {seed}...")
        random.seed(seed)
        
        # --- Generate all shoes and compute entries ---
        shoe_data = []
        
        for _ in range(N_PER_SEED):
            outcomes = generate_shoe()
            # v3: BR only -- no derived views are built or analyzed.

            tx_all = {t: [] for t in THRESHOLDS}
            mk_all = []

            # Per-side (H / T) tracking for Table 5.
            tx_by_side = {t: {'H': [], 'T': []} for t in THRESHOLDS}
            mk_by_side = {'H': [], 'T': []}

            road_seq = outcomes
            stop = STOP_ENTERING  # BR uses the full shoe-level stop
            streaks = extract_streaks(road_seq)
            tx_entries, mk_entries = analyze_entries(streaks, stop)

            for t in THRESHOLDS:
                tx_all[t].extend(tx_entries[t])
            mk_all.extend(mk_entries)

            # Per-side breakdown (TX and MK)
            for start_pos, side, streak_len in streaks:
                # TX entries by side
                for t in THRESHOLDS:
                    if streak_len >= t and start_pos + t <= stop:
                        busted = (streak_len - t) >= BUST_STEPS
                        tx_by_side[t][side].append(busted)
                # MK entries by side (side = the new streak's side)
                if start_pos > 0 and start_pos + 1 <= stop:
                    busted_mk = streak_len >= BUST_STEPS + 1
                    mk_by_side[side].append(busted_mk)

            shoe_data.append({
                'tx': tx_all,
                'mk': mk_all,
                'tx_side': tx_by_side,
                'mk_side': mk_by_side,
            })
        
        # --- Compute results for each threshold ---
        for t in THRESHOLDS:
            # TX totals
            tx_total = sum(len(s['tx'][t]) for s in shoe_data)
            tx_busts = sum(sum(s['tx'][t]) for s in shoe_data)
            tx_rate = tx_busts / tx_total * 100 if tx_total else 0
            
            # MK full rate (non-equalized)
            mk_full_total = sum(len(s['mk']) for s in shoe_data)
            mk_full_busts = sum(sum(s['mk']) for s in shoe_data)
            mk_full_rate = mk_full_busts / mk_full_total * 100 if mk_full_total else 0
            
            # Equalized comparison: subsample MK to match TX per shoe.
            # v3 Fix 5: track the actual subsample total `et` and use it for
            # the rate denominator instead of tx_total. They differ only on
            # rare shoes where TX > MK; for those, tx_total over-counts.
            eq_busts_list = []
            eq_total_list = []
            for trial in range(EQ_TRIALS):
                random.seed(seed * 1000 + t * 100 + trial + 77777)
                eb = 0
                et = 0
                for s in shoe_data:
                    tc = len(s['tx'][t])
                    ml = s['mk']
                    if tc == 0 or len(ml) == 0:
                        continue
                    ss = min(tc, len(ml))
                    samp = random.sample(ml, ss)
                    et += ss
                    eb += sum(samp)
                eq_busts_list.append(eb)
                eq_total_list.append(et)

            avg_mk_eq_busts = sum(eq_busts_list) / len(eq_busts_list)
            avg_eq_total = sum(eq_total_list) / len(eq_total_list)
            avg_mk_eq_rate = (avg_mk_eq_busts / avg_eq_total * 100) if avg_eq_total > 0 else 0
            eq_std = (sum(((b / e * 100 if e > 0 else 0) - avg_mk_eq_rate) ** 2
                         for b, e in zip(eq_busts_list, eq_total_list))
                         / len(eq_busts_list)) ** 0.5
            eq_busts_min = min(eq_busts_list) if eq_busts_list else 0
            eq_busts_max = max(eq_busts_list) if eq_busts_list else 0

            # Z-score (two-proportion, sample sizes tx_total and avg_eq_total)
            p1 = tx_rate / 100
            p2 = avg_mk_eq_rate / 100
            n1 = tx_total
            n2 = avg_eq_total if avg_eq_total > 0 else tx_total
            if (n1 + n2) > 0:
                pooled = (tx_busts + avg_mk_eq_busts) / (n1 + n2)
                if pooled > 0:
                    se = math.sqrt(pooled * (1 - pooled) * (1.0 / n1 + 1.0 / n2))
                else:
                    se = 1
                z = (p1 - p2) / se if se > 0 else 0
            else:
                z = 0

            # Bayes factor (overflow-safe)
            try:
                bf = math.exp(z * z / 2) if abs(z) > 0.1 else 1.0
            except OverflowError:
                bf = float('inf')

            # Advantage
            adv = (tx_rate / avg_mk_eq_rate - 1) * 100 if avg_mk_eq_rate > 0 else 0

            # Per-side breakdown (TX and MK_eq) -- needed for Table 5 at T=4
            side_results = {}
            for side in ['H', 'T']:
                # TX per side
                tx_side_entries = []
                for s in shoe_data:
                    tx_side_entries.extend(s['tx_side'][t].get(side, []))
                tx_s_total = len(tx_side_entries)
                tx_s_busts = sum(tx_side_entries)
                tx_s_rate = tx_s_busts / tx_s_total * 100 if tx_s_total else 0
                # MK per side, equalized to TX per side count per shoe
                side_eq_busts = []
                side_eq_totals = []
                for trial in range(EQ_TRIALS):
                    random.seed(seed * 10000 + t * 1000 + trial + 99999 + (1 if side == 'H' else 2))
                    seb = 0
                    set_ = 0
                    for s in shoe_data:
                        tc_s = len(s['tx_side'][t].get(side, []))
                        mk_s = s['mk_side'].get(side, [])
                        if tc_s == 0 or len(mk_s) == 0:
                            continue
                        ss_s = min(tc_s, len(mk_s))
                        samp_s = random.sample(mk_s, ss_s)
                        set_ += ss_s
                        seb += sum(samp_s)
                    side_eq_busts.append(seb)
                    side_eq_totals.append(set_)
                avg_s_mk_busts = sum(side_eq_busts) / len(side_eq_busts) if side_eq_busts else 0
                avg_s_eq_total = sum(side_eq_totals) / len(side_eq_totals) if side_eq_totals else 0
                s_mk_rate = (avg_s_mk_busts / avg_s_eq_total * 100) if avg_s_eq_total > 0 else 0
                s_adv = (tx_s_rate / s_mk_rate - 1) * 100 if s_mk_rate > 0 else 0
                side_results[side] = {
                    'tx_entries': tx_s_total,
                    'tx_busts': tx_s_busts,
                    'tx_rate': tx_s_rate,
                    'mk_eq_rate': s_mk_rate,
                    'adv': s_adv,
                }

            all_results.append({
                'seed': seed,
                't': t,
                'tx_total': tx_total,
                'tx_busts': tx_busts,
                'tx_rate': tx_rate,
                'tx_per_shoe': tx_total / N_PER_SEED,
                'mk_full_total': mk_full_total,
                'mk_full_busts': mk_full_busts,
                'mk_full_rate': mk_full_rate,
                'mk_eq_busts': avg_mk_eq_busts,
                'mk_eq_total': avg_eq_total,
                'mk_eq_rate': avg_mk_eq_rate,
                'eq_std': eq_std,
                'eq_busts_min': eq_busts_min,
                'eq_busts_max': eq_busts_max,
                'adv': adv,
                'z': z,
                'bf': bf,
                'side_results': side_results,
                'total_flips': N_PER_SEED * SHOE_LENGTH,
            })

            # CHECKPOINT 2: equalization stability per (seed, T)
            print(f"  EQ_STABILITY: Seed {seed} T{t} -- MK busts range: "
                  f"{eq_busts_min}-{eq_busts_max} across {EQ_TRIALS} trials")

        # CHECKPOINT 1: seed completion summary
        seed_rows = [r for r in all_results if r['seed'] == seed]
        if seed_rows:
            total_tx_entries = sum(r['tx_total'] for r in seed_rows)
            total_mk_entries = seed_rows[0]['mk_full_total']
            total_tx_busts = sum(r['tx_busts'] for r in seed_rows)
            print(f"  CHECKPOINT: Seed {seed} complete. "
                  f"TX entries (all T): {total_tx_entries}, "
                  f"MK entries: {total_mk_entries}, "
                  f"TX busts (all T): {total_tx_busts}")

    # CHECKPOINT 3: per-entry rate verification (after all seeds)
    print()
    markov = 0.5 ** BUST_STEPS
    for t in THRESHOLDS:
        sub = [r for r in all_results if r['t'] == t]
        tx_e = sum(r['tx_total'] for r in sub)
        tx_b = sum(r['tx_busts'] for r in sub)
        tx_r = tx_b / tx_e if tx_e else 0
        dev_pct = abs(tx_r - markov) / markov * 100 if markov > 0 else 0
        ok = "PASS" if dev_pct < 3 else "FAIL"
        print(f"  RATE_CHECK: T{t} -- TX rate: {tx_r * 100:.4f}% vs Markov "
              f"{markov * 100:.4f}% -- deviation: {dev_pct:.2f}% -- {ok} (threshold: 3%)")

    # CHECKPOINT 4: monotonicity verification per seed (after all seeds)
    print()
    for seed in SEEDS:
        rows = sorted([r for r in all_results if r['seed'] == seed], key=lambda r: r['t'])
        advs = [r['adv'] for r in rows]
        # Monotonic if each successive adv is more negative (smaller numerically)
        mono = all(advs[i] > advs[i + 1] for i in range(len(advs) - 1))
        chain = " -> ".join(f"T{r['t']}:{r['adv']:+.1f}%" for r in rows)
        print(f"  MONO_CHECK: Seed {seed} -- {chain} -- Monotonic: {'YES' if mono else 'NO'}")
    print()

    return all_results

# ============================================================
# OUTPUT: Reproduce all paper tables
# ============================================================

def print_results(all_results):
    """Print all tables from the paper."""
    
    markov_pred = (0.5 ** BUST_STEPS) * 100
    
    # ---- TABLE 1: Per-entry rates ----
    print("\n" + "=" * 80)
    print("TABLE 1: Per-entry catastrophic loss rates by threshold")
    print("=" * 80)
    print(f"  {'Threshold':>9} {'TX Entries':>12} {'TX Losses':>10} {'TX Rate':>9} "
          f"{'MK Full':>9} {'Markov':>9}")
    print(f"  {'-' * 62}")
    
    for t in THRESHOLDS:
        sub = [r for r in all_results if r['t'] == t]
        tx_e = sum(r['tx_total'] for r in sub)
        tx_b = sum(r['tx_busts'] for r in sub)
        tx_r = tx_b / tx_e * 100
        mk_r = sum(r['mk_full_rate'] for r in sub) / len(sub)
        print(f"  T{t:<8} {tx_e:>12,} {tx_b:>10} {tx_r:>8.4f}% "
              f"{mk_r:>8.4f}% {markov_pred:>8.4f}%")
    
    # ---- TABLE 2: Equalized comparison ----
    # v3 Fix 5: rates use the equalized count (avg_eq_total) in the
    # denominator for MK; TX rates remain over the full TX count
    # (TX is not subsampled in the standard equalization).
    print("\n" + "=" * 80)
    print("TABLE 2: Equalized comparison by threshold")
    print("=" * 80)
    print(f"  {'T':>3} {'Entries':>12} {'TX Loss':>9} {'MK Loss':>10} "
          f"{'Avoided':>10} {'TX Rate':>9} {'MK Rate':>10} {'Adv':>8}")
    print(f"  {'-' * 76}")

    for t in THRESHOLDS:
        sub = [r for r in all_results if r['t'] == t]
        entries = sum(r['tx_total'] for r in sub)
        mk_eq_total = sum(r['mk_eq_total'] for r in sub)
        tx_b = sum(r['tx_busts'] for r in sub)
        mk_b = sum(r['mk_eq_busts'] for r in sub)
        tx_r = tx_b / entries * 100 if entries else 0
        mk_r = (mk_b / mk_eq_total * 100) if mk_eq_total > 0 else 0
        adv = (tx_r / mk_r - 1) * 100 if mk_r > 0 else 0
        print(f"  T{t:<2} {entries:>12,} {tx_b:>9} {mk_b:>10.1f} "
              f"{mk_b - tx_b:>+10.1f} {tx_r:>8.4f}% {mk_r:>9.4f}% {adv:>+7.1f}%")

    # ---- TABLE 2B: Per-flip comparison ----
    print("\n" + "=" * 80)
    print("TABLE 2B: Equalized catastrophic losses per coin flip")
    print("=" * 80)
    total_flips = N_PER_SEED * SHOE_LENGTH * len(SEEDS)
    print(f"  {'T':>3} {'Flips':>14} {'TX Loss':>9} {'MK Loss':>10} "
          f"{'TX/Flip':>10} {'MK/Flip':>10} {'Gap':>8}")
    print(f"  {'-' * 68}")

    for t in THRESHOLDS:
        sub = [r for r in all_results if r['t'] == t]
        tx_b = sum(r['tx_busts'] for r in sub)
        mk_b = sum(r['mk_eq_busts'] for r in sub)
        tx_pf = tx_b / total_flips * 100 if total_flips else 0
        mk_pf = mk_b / total_flips * 100 if total_flips else 0
        gap = (tx_pf / mk_pf - 1) * 100 if mk_pf > 0 else 0
        print(f"  T{t:<2} {total_flips:>14,} {tx_b:>9} {mk_b:>10.1f} "
              f"{tx_pf:>9.4f}% {mk_pf:>9.4f}% {gap:>+7.1f}%")

    # ---- TABLE 3: Statistical significance ----
    # Per-seed Z scores are individually computed in run_experiment (using each
    # seed's TX/MK_eq totals + busts). Combined Z = Stouffer aggregation.
    # Discounted Z = combined Z / sqrt(2) (conservative within-shoe correction).
    print("\n" + "=" * 80)
    print("TABLE 3: Statistical significance by threshold")
    print("=" * 80)
    seed_hdr = " ".join(f"{'Z_s'+str(s):>9}" for s in SEEDS)
    print(f"  {'T':>3} {seed_hdr} {'Combined Z':>11} {'Bayes Factor':>13} "
          f"{'vs Diaconis':>13} {'5-sig?':>7} {'Disc Z':>9} {'Disc 5-sig?':>11}")
    print(f"  {'-' * (4 + 10 * len(SEEDS) + 60)}")

    for t in THRESHOLDS:
        sub = sorted([r for r in all_results if r['t'] == t], key=lambda r: SEEDS.index(r['seed']))
        per_seed_zs = [r['z'] for r in sub]
        cz = sum(per_seed_zs) / math.sqrt(len(sub))
        try:
            cbf = math.exp(cz * cz / 2)
        except OverflowError:
            cbf = float('inf')
        diac = cbf / 2359 if cbf != float('inf') else float('inf')
        five = "Yes" if abs(cz) > 5 else "No"
        if cbf == float('inf'):
            bf_str = "inf"
        else:
            bf_str = f"{cbf:.1e}" if cbf > 1e6 else f"{cbf:.0f}"
        if diac == float('inf'):
            d_str = "inf"
        else:
            d_str = f"{diac:.0e}" if diac > 1e6 else f"{diac:.0f}x"
        disc_z = cz / math.sqrt(2)
        disc_five = "Yes" if abs(disc_z) > 5 else "No"
        seed_z_str = " ".join(f"{z:>+9.2f}" for z in per_seed_zs)
        print(f"  T{t:<2} {seed_z_str} {cz:>+11.2f} {bf_str:>13} {d_str:>13} "
              f"{five:>7} {disc_z:>+9.2f} {disc_five:>11}")

    # ---- TABLE 4: Per-seed advantage with std dev ----
    print("\n" + "=" * 80)
    print("TABLE 4: Advantage by seed and threshold (with Std Dev)")
    print("=" * 80)
    header = f"  {'T':>3}"
    for s in SEEDS:
        header += f" {'Seed '+str(s):>10}"
    header += f" {'Average':>10} {'StdDev':>8}"
    print(header)
    print(f"  {'-' * (14 + 11 * len(SEEDS) + 10)}")

    for t in THRESHOLDS:
        line = f"  T{t:<2}"
        sub = sorted([r for r in all_results if r['t'] == t], key=lambda r: SEEDS.index(r['seed']))
        advs = [r['adv'] for r in sub]
        for a in advs:
            line += f" {a:>+9.1f}%"
        avg = sum(advs) / len(advs)
        if len(advs) > 1:
            sd = (sum((a - avg) ** 2 for a in advs) / (len(advs) - 1)) ** 0.5
        else:
            sd = 0
        line += f" {avg:>+9.1f}% {sd:>7.2f}%"
        print(line)

    # ---- TABLE 5: Side symmetry (H vs T) at T=4 ----
    print("\n" + "=" * 80)
    print("TABLE 5: Side symmetry (H vs T) at T=4")
    print("=" * 80)
    print(f"  {'Side':>5} {'TX Entries':>12} {'TX Losses':>10} "
          f"{'TX Rate':>9} {'MK Eq Rate':>11} {'Advantage':>10}")
    print(f"  {'-' * 64}")

    sub = [r for r in all_results if r['t'] == 4]
    for side in ['H', 'T']:
        agg_tx_entries = sum(r['side_results'][side]['tx_entries'] for r in sub)
        agg_tx_busts = sum(r['side_results'][side]['tx_busts'] for r in sub)
        # Weighted average of rates by entries
        if agg_tx_entries > 0:
            agg_tx_rate = agg_tx_busts / agg_tx_entries * 100
        else:
            agg_tx_rate = 0
        # MK eq rate / adv: weighted average across seeds (each seed equally weighted)
        if sub:
            agg_mk_rate = sum(r['side_results'][side]['mk_eq_rate'] for r in sub) / len(sub)
            agg_adv = (agg_tx_rate / agg_mk_rate - 1) * 100 if agg_mk_rate > 0 else 0
        else:
            agg_mk_rate = 0
            agg_adv = 0
        print(f"  {side:>5} {agg_tx_entries:>12,} {agg_tx_busts:>10} "
              f"{agg_tx_rate:>8.4f}% {agg_mk_rate:>10.4f}% {agg_adv:>+9.1f}%")

    # ---- SUMMARY ----
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n  Total sequences: {N_PER_SEED * len(SEEDS):,}")
    print(f"  Total coin flips: {total_flips:,}")
    print(f"  Independent seeds: {len(SEEDS)}")
    print(f"  Thresholds tested: {len(THRESHOLDS)}")
    print(f"  Data points: {len(SEEDS) * len(THRESHOLDS)}")

    # v3 Fix 1: monotonicity comparison sense corrected.
    # With both advantages negative, deeper-T should be more negative,
    # i.e. r1.adv > r2.adv numerically. Pass when r1 > r2.
    mono = True
    for t_idx in range(len(THRESHOLDS) - 1):
        for seed in SEEDS:
            r1 = [r for r in all_results if r['t'] == THRESHOLDS[t_idx] and r['seed'] == seed][0]
            r2 = [r for r in all_results if r['t'] == THRESHOLDS[t_idx + 1] and r['seed'] == seed][0]
            if r1['adv'] > r2['adv']:
                pass
            else:
                mono = False

    print(f"  Gradient monotonic across all {len(SEEDS) * len(THRESHOLDS)} points: "
          f"{'YES' if mono else 'NO'}")

    # Equalization stability
    max_std = max(r['eq_std'] for r in all_results)
    print(f"  Max equalization std dev: {max_std:.4f} percentage points")

    # v3 Fix 2: actual check rather than hardcoded "YES".
    markov_fr = 0.5 ** BUST_STEPS
    tx_ok = all(abs(r['tx_rate'] / 100 - markov_fr) / markov_fr < 0.015 for r in all_results)
    tx_ok3 = all(abs(r['tx_rate'] / 100 - markov_fr) / markov_fr < 0.03 for r in all_results)
    mk_ok3 = all(abs(r['mk_full_rate'] / 100 - markov_fr) / markov_fr < 0.03 for r in all_results)
    print(f"\n  Markov prediction (0.5^{BUST_STEPS}): {markov_pred:.4f}%")
    print(f"  All TX per-entry rates within 1.5% of prediction: {'YES' if tx_ok else 'NO'}")
    print(f"  All TX per-entry rates within 3.0% of prediction: {'YES' if tx_ok3 else 'NO'}")
    print(f"  All MK per-entry rates within 3.0% of prediction: {'YES' if mk_ok3 else 'NO'}")

# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 80)
    print("THE GAMBLER WAS RIGHT: Experimental Reproduction Script")
    print("v3 -- BR-only (Direct Sequence only; no derived views)")
    print(f"Configuration: {len(SEEDS)} seeds x {N_PER_SEED:,} shoes x "
          f"{len(THRESHOLDS)} thresholds x 1 view (BR)")
    print(f"Total coin flips: {N_PER_SEED * SHOE_LENGTH * len(SEEDS):,}")
    print(f"EQ_TRIALS = {EQ_TRIALS}; SHOE_LENGTH = {SHOE_LENGTH}; STOP_ENTERING = {STOP_ENTERING}")
    print("=" * 80)

    results = run_experiment()
    print_results(results)

    print("\n" + "=" * 80)
    print("REPRODUCTION COMPLETE")
    print("=" * 80)
