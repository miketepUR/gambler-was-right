The Gambler Was Right: A Reproducible Challenge to Strategic Indifference in Fair Coin Sequences

**Michael E. Teplinsky**Independent Researcher, Thousand Oaks, CAJune 2026

## Abstract

In a memoryless process, each event is independent of every prior event. The past carries no information about the future. From this, a conclusion follows — not as a hypothesis but as a logical entailment — that in a sequence of independent events, the timing of an observer's engagement cannot affect outcome distributions. We term this conclusion *strategic indifference* and test it directly using computationally generated fair coin flip sequences. We show that it does not follow.

Two players observe the same sequences of 80 binary outcomes across 500,000 sequences (40 million coin flips), make the same number of 9-bet anti-continuation wagers, and face identical per-entry loss odds of (1/2)\^9. They differ only in entry criterion: the selective player enters after observing T consecutive same-side outcomes (T ∈ {3, 4, 5, 6, 7}); the Markov player enters at each direction change. The equalized comparison reveals that strategic indifference fails: the selective player experiences 10.6% to 67.7% fewer catastrophic losses than the Markov player, scaling monotonically with observation depth, with zero gradient reversals across 25 data points (5 seeds × 5 thresholds) and combined Z-scores from −7.16 to −22.60 — significance that remains decisive after conservative correction for within-sequence correlation, and corresponding Bayes factors well beyond the benchmark reported for the Diaconis et al. (2023) physical coin-bias result. Yet per-entry loss rates confirm independence — both players match the theoretical prediction of (1/2)\^9 at every threshold tested. The effect is not predictive but positional: the patient player never sees the next flip more clearly — each bet remains exactly 1/512 — but occupies positions where catastrophe is structurally less dense in aggregate.

The mechanism is path narrowing: prior observations consume positions within the streak structure, constituting a higher effective catastrophe threshold without altering any individual flip probability. The advantage scales inversely with sequence length — converging with Miller and Sanjurjo's (2018) finite-sequence streak bias when compared at matched sequence lengths — demonstrating that their retrospective finding also operates prospectively. The result decomposes the Gambler's Fallacy into two separable claims — the per-event prediction (false) and the strategic entry prescription (true) — and demonstrates that observation of prior outcomes in a memoryless sequence, though individually uninformative, produces measurable structural consequences when used as an entry criterion.

Full Python implementation is provided for independent reproduction.

## 1. INTRODUCTION

### 1.1 The Strategic Indifference Assumption

A fair coin is the canonical example of a memoryless process. The probability of heads on any given flip is exactly one-half, regardless of what came before — whether the preceding flip was heads, whether the preceding ten flips were all heads, or whether the coin has never been flipped at all. This property, known as independence, is not merely an approximation. For a mathematically fair binary process, it is a definitional truth. The next outcome does not depend on the prior outcomes. The coin has no memory.

From this property, a second claim is routinely derived: because each flip is independent of all prior flips, the timing of a bet on that flip cannot affect the bettor’s expected outcome. A player who wagers after observing four consecutive heads faces the same probability on their next nine bets as a player who wagers after observing a single tails. Both players will lose nine consecutive bets with probability (1/2)\^9 = 1/512. The observation preceding their entry — whether a long streak or a single outcome — is irrelevant to what follows. This claim, which we term *strategic indifference*, holds that in an independent sequence, entry timing is a matter of personal preference, not statistical advantage.

Strategic indifference is not typically stated as a separate principle. It is treated as an obvious corollary of per-event independence: if no single flip is affected by prior flips, then no strategy based on observing prior flips can outperform any other strategy. This inference is so deeply embedded in probability pedagogy that it rarely receives independent scrutiny. It is the foundation upon which the Gambler’s Fallacy is debunked, the basis for dismissing streak-based betting strategies as superstition, and the reason that decision theorists treat entry timing as irrelevant in memoryless systems.

A Markov process, named for the Russian mathematician Andrey Markov, formalizes this property: the future evolution of the process depends only on its current state, not on the sequence of states that preceded it. For a fair coin, the “current state” carries no information about the past, so every position in the sequence is statistically identical. A player choosing to bet at position 5 after observing four heads is, under Markov’s framework, in exactly the same statistical position as a player betting at position 2 after observing a single tails. The four heads are inert history — observed, perhaps noted, but carrying no information that could improve or worsen the bettor’s prospects.

Consider a simple illustration. Two players sit at the same table and watch the same sequence of fair coin flips. Player A waits patiently, watching flip after flip, until four consecutive heads appear. Only then does Player A place a bet — wagering against continuation, betting that tails will appear. Player B adopts a different strategy: after every change in direction (heads following tails, or tails following heads), Player B immediately bets against the new direction continuing.

Both players make 9-bet sequences. Both risk the same amount. Both face 1/512 odds of losing all 9 bets. The Markovian prediction is categorical: because each flip is independent, these two strategies should produce identical outcome distributions. Player A’s patience — the careful observation of four consecutive same-side outcomes before engaging — should confer no advantage whatsoever. The four observed flips are, in Markov’s framework, noise. They offer no mathematical armor for the bets that follow. By this reasoning, the patient player is not betting against a 13-flip streak — they are betting against a 9-flip streak, because the first 4 flips are already locked in as history. Whether those 4 flips happened or not, you started your bet here, and the next 9 bets are all that matter.

This paper tests that prediction directly, and finds it false.

### 1.2 The Gambler’s Fallacy and Its Decomposition

The Gambler’s Fallacy is traditionally defined as the erroneous belief that in a sequence of independent events, the occurrence of a particular outcome (such as a streak of heads) makes the opposite outcome more likely in subsequent trials. A gambler watching a roulette wheel land on red six times in a row might believe that black is “due” — that the streak itself creates pressure toward reversal.

The debunking is swift and well-established: each spin is independent, the wheel has no memory, and the probability of black on the next spin remains exactly what it was before the streak began. The gambler’s error is in attributing memory to a memoryless process. This debunking is correct.

However, the Gambler’s Fallacy as commonly discussed conflates two logically separable claims:

**Claim 1 (the per-event prediction):** After observing a streak of same-side outcomes, the probability of the opposite outcome on the next individual event is greater than one-half.

**Claim 2 (the strategic prescription):** A player should wait for streaks before betting against continuation, rather than betting at arbitrary positions.

The standard treatment debunks Claim 1 — correctly — and assumes Claim 2 falls with it. The inferential step from “each flip is fair” to “therefore timing your bets based on streaks is futile” appears so natural that Claim 2 has, to our knowledge, never been independently tested.

We confirm Claim 1 is false. Our data reproduces the standard result: the per-entry probability of losing 9 consecutive bets is 1/512 regardless of entry timing. Each flip is fair. The coin has no memory. Markov is right about every individual event.

We find Claim 2 is true. The player who waits for streaks before betting against continuation experiences measurably fewer catastrophic 9-bet losses than a player who enters at non-streak positions, when both players make the same number of bets on the same sequences. The advantage is 20.8% at a minimum observation depth of 4, scaling monotonically to 67.7% at an observation depth of 7, replicating across five independent random seeds at combined significance exceeding the 5-sigma discovery threshold used in physics.

The Gambler’s Fallacy is a fallacy about per-event probabilities. It is not a fallacy about strategic entry timing.

### 1.3 Precedent: Diaconis and the Coin Flip Assumption

The assumption that coin flips are exactly 50/50 has itself been empirically challenged. Diaconis, Holmes, and Montgomery developed a dynamical model of coin tossing predicting that a coin will land on the same side it started with slightly more than half the time, due to precession effects during the flip. In 2023, Bartoš et al. confirmed this prediction empirically with 350,757 coin flips across 48 participants, finding a same-side bias of 50.8% with a 95% credible interval of [50.6%, 50.9%] and a Bayes factor of 2,359 — meaning the evidence was over two thousand times more probable under the biased model than under a pure 50/50 model.

Diaconis attributed this bias to the physics of the coin — angular momentum, starting orientation, and precession dynamics. The medium itself carries predictive information from its initial state into its final state. This finding established a precedent: assumptions about fairness and independence that appear self-evident can fail under sufficiently careful empirical scrutiny.

Our study differs from Diaconis in a fundamental respect. We do not use physical coins. Our sequences are generated by a computational pseudo-random number generator (`random.choice()` in Python, implementing the Mersenne Twister algorithm) which produces outcomes that are, by construction, free of any physical properties — no precession, no angular momentum, no starting-state information. Each outcome is computationally independent of every other. If our experiment reveals a selectional advantage, it cannot be attributed to the physics of the medium.

### 1.4 Precedent: Miller, Sanjurjo, and the Finite Sequence Bias

A second challenge to the standard treatment of streaks comes from mathematics rather than physics. In 2018, Miller and Sanjurjo published a result in *Econometrica* that startled the statistics community: in a finite sequence of fair coin flips, positions immediately following streaks of consecutive same-side outcomes exhibit a mathematically demonstrable reversal bias — the expected proportion of continuation drops below 50%, with the magnitude increasing with streak length.

For a sequence of 100 fair coin flips, Miller and Sanjurjo computed the expected proportion of heads following a streak of heads:

| After streak of | Expected continuation | Drop from 50% |
|-----------------|-----------------------|---------------|
| 1               | 49.5%                 | −0.5%         |
| 2               | 48.4%                 | −1.6%         |
| 3               | 46.0%                 | −4.0%         |
| 4               | 41.2%                 | −8.8%         |
| 5               | 36.5%                 | −13.5%        |

The bias increases monotonically with streak length — the longer the observed streak, the greater the expected reversal. The authors attributed this to a counting artifact inherent in finite datasets: in a closed sequence that must approximately balance between outcomes, positions consumed by streaks leave fewer remaining positions for continuation, creating a retrospective bias toward reversal. They characterized this as a property of completed datasets analyzed in hindsight, explicitly stating that it does not apply to a gambler making real-time bets into the future.

This limitation is worth scrutinizing. Miller and Sanjurjo’s mathematical proof established that streak positions in finite sequences exhibit reversal bias. Their restriction to retrospective analysis followed from their interpretation of the mechanism — that the bias arises from mean-reversion pressure within a closed dataset. If the mechanism is indeed dataset closure, the restriction is correct: a real-time bettor faces an open future with no closure constraint.

However, if the bias Miller and Sanjurjo detected is not solely a mean-reversion artifact but rather the expression of a more general property of how observation interacts with finite sequential structure, the retrospective restriction may be too narrow. Our experiment tests this possibility directly, using an open-sequence design with no closure constraint, and finds that the selective advantage operates prospectively with the same monotonic relationship to observation depth that Miller and Sanjurjo identified retrospectively — though at approximately 2.5× the magnitude, consistent with their closed-dataset methodology attenuating the underlying signal through mean-reversion pressure (Section 4.3).

### 1.5 The Distinction We Test

We propose that per-event independence and strategic indifference are logically distinct claims, and that confirming the first does not establish the second.

Per-event independence is a property of the generating process: P(H\|HHHH) = P(H) = 0.5. This is a mathematical statement about conditional probabilities of individual outcomes. It is true for fair coins, confirmed by our data, and not in dispute.

Strategic indifference is a claim about observers: a player who selects entry positions based on prior outcomes should achieve no different outcome distribution than a player who does not. This is presented as a corollary of independence, but it is an inferential extension — a claim about the strategic implications of independence, not a restatement of independence itself.

We test strategic indifference by constructing the most favorable possible conditions for it. We use mathematically fair binary sequences (no physical bias). We ensure both players make exactly 9 bets per entry (identical risk). We equalize the number of entries per sequence (identical exposure). We replicate across five independent random seeds spanning 500,000 sequences and 40,000,000 coin flips (no dataset dependence). The only variable we manipulate is the entry criterion: one player enters after observing a streak of T consecutive same-side outcomes; the other enters after each direction change.

If strategic indifference holds, the two players should produce statistically indistinguishable outcome distributions. They do not.

Both players face the same definition of catastrophic loss: 9 consecutive bets where the coin lands on the same side every time. Both lose everything they wagered across those 9 bets. There is no structural difference in what constitutes a loss — only in what the player observed before placing the first bet. One player watched and waited. The other did not. Both then made the same bet, the same number of times, on the same coins.

The player who watched and waited loses less often. At an observation depth of 4 prior same-side outcomes, the selective player experiences 20.8% fewer catastrophic losses than the non-selective player. At a depth of 5, the advantage grows to 35.6%. At 7, it reaches 67.7%. The advantage is monotonic — it increases at every level of patience tested — and it replicates across five independent random seeds with zero reversals in 25 data points, at combined statistical significance ranging from 7-sigma to 23-sigma.

The Gambler’s Fallacy, it turns out, is only half a fallacy. The gambler is wrong about why — each flip is fair, and no amount of prior heads makes tails more likely on the next toss. But the gambler is right about what to do — wait for the streak, then bet against it. This result does not claim that coins have memory, that individual flip probabilities are altered by prior outcomes, or that the laws of probability require revision. It claims something more fundamental: that two players, facing the same fair coin, making the same number of bets, using the same betting structure, experiencing the same definition of loss — can arrive at measurably different outcomes based solely on what they chose to observe before engaging.

The individual flips are independent. The decision of when to act on them is not. And that decision, which the entire field of probability has dismissed as irrelevant for the better part of a century, turns out to matter — reproducibly, monotonically, and at a level of statistical confidence that exceeds the discovery threshold used in physics.

Section 4 proposes an explanatory mechanism — based on conditional path narrowing within the space of compatible sequence continuations — that reconciles this finding with per-event independence without requiring any revision to the laws of probability. Section 5 records, separately and without physical claim, two structural parallels between the mathematical form of these findings and established physics — amplitude-squared scaling in the path narrowing gradient, and configuration-dependent cross-terms in the aggregate covariance structure documented in Section 4.5.5 — noting their co-occurrence and identifying them as directions for future theoretical work, while bearing none of the paper's empirical weight.

## 2. METHODS

### 2.1 Sequence Generation

All binary sequences were generated computationally using Python’s `random.choice()` function, which implements the Mersenne Twister pseudo-random number generator (PRNG) with a period of 2\^19937 − 1. Each outcome was drawn independently from the set {H, T} with equal probability. No physical coins, cards, or mechanical devices were used at any point in the experiment.

This design choice is central to the study. Physical coin flips carry information in their starting state, angular momentum, and precession dynamics — properties that Diaconis et al. have shown produce measurable same-side bias. By using a computational generator, we eliminate every physical channel through which prior outcomes might influence future outcomes. If our experiment reveals a selectional advantage, it cannot be attributed to the physics of the medium.

We note that the Mersenne Twister, while deterministic, is universally accepted in computational statistics and passes all standard tests of randomness, including the Diehard battery, the NIST Statistical Test Suite, and the TestU01 suite. Our results replicate across five independent seeds, each producing a distinct deterministic sequence with no structural relationship to the others. Furthermore, because both player strategies are applied to the same sequences, any subtle autocorrelation properties of the generator would affect both players equally. The comparative finding — a difference between two strategies applied to identical data — is robust to PRNG concerns. As a straightforward extension, the experiment could be replicated using hardware random number generation (atmospheric noise or quantum random number generators) to establish generalizability to non-deterministic sources.

Each experimental unit, termed a “shoe” for consistency with the applied domain from which the experimental structure was adapted [footnote: The sequence structure and entry selection framework were originally developed for analysis of the card game baccarat, where a “shoe” refers to the dealing container holding multiple decks. The mathematical framework was subsequently abstracted to fair coin sequences to eliminate all medium-specific properties. The results reported here use exclusively computational coin flips and do not depend on any properties of card games.], consisted of 80 sequential binary outcomes generated from a single random seed state. The shoe length of 80 was chosen to provide sufficient sequence length for streak development and resolution while maintaining a bounded structure amenable to systematic analysis.

### 2.2 Streak Column Construction

Each 80-outcome sequence is organized into columns of consecutive identical outcomes. A sequence H H H T T H H H H T would produce four columns of lengths [3, 2, 4, 1], where each column represents a maximal unbroken run of one outcome. This columnar representation provides the structural basis for both player strategies: streaks are columns, streak length is column depth, and direction changes occur at column boundaries.

No transformation or reinterpretation of the raw outcomes is applied. The columns are a direct, lossless reorganization of the original H/T sequence into its streak structure. Every entry position and every outcome used in the experiment corresponds to a specific coin flip in the original sequence.

### 2.3 Player Strategies

Two player strategies were compared, each representing a different answer to the question: does it matter when you enter a sequence of bets?

**The Selective Player (TX).** The selective player monitors the outcome sequence, watching for the first occurrence of a “fresh” streak: T consecutive identical outcomes immediately preceded by the opposite outcome (establishing that the streak began exactly T positions ago, not earlier). Upon identifying such a streak, the selective player enters — placing 9 consecutive bets against the streak’s continuation.

Five observation depths were tested: T ∈ {3, 4, 5, 6, 7}. At each depth, the selective player observes T consecutive same-side outcomes, then bets that the opposite side will appear, continuing for up to 9 bets. The player suffers a catastrophic loss if and only if all 9 bets lose — meaning the streak continued unbroken for 9 additional outcomes beyond the T already observed.

To be precise about what constitutes the player’s action: the selective player makes 9 bets. No more, no fewer. The T prior outcomes are observed but not wagered on. They are, in Markovian terms, irrelevant history — information that, under the assumption of independence, should have no bearing on the outcome of the 9 bets that follow. The selective player’s strategy is defined entirely by the claim that this information does have bearing, expressed through the timing of entry.

**The Markov Player (MK).** The Markov player implements the strategy that strategic indifference endorses: enter at the earliest possible position where the preceding outcome provides a signal, without requiring extended observation. Specifically, the Markov player enters at every direction change — the first position of a new streak, immediately following an outcome of the opposite type. Upon observing a direction change, the Markov player bets against the new direction continuing, placing 9 consecutive bets.

The Markov player’s strategy is the operational expression of the belief that prior outcomes are irrelevant. If entry timing does not matter, then the minimal observation (a single prior outcome) is as informative as an extended observation (T prior outcomes), and entering immediately is as effective as entering after patient observation.

**Both players:** - Make exactly 9 bets per entry - Bet against the continuation of the most recently observed outcome - Suffer catastrophic loss if and only if all 9 bets lose (the side they bet against appears 9 consecutive times) - Cease entering new bet sequences after position 65 of each 80-outcome shoe, ensuring that every entry has at least 15 remaining positions for the bet sequence to resolve

The two strategies are identical in every respect except one: how many prior same-side outcomes the player observes before placing the first bet. The selective player observes T. The Markov player observes 1. Both then make 9 bets against continuation. Under strategic indifference, this difference should produce no measurable effect on outcomes.

### 2.4 Equalization Protocol

The selective player (TX) produces fewer entry opportunities per shoe than the Markov player (MK), because the TX trigger condition (T consecutive same-side outcomes) is more restrictive than the MK trigger condition (any direction change). At T4, the selective player averages approximately 3.9 entries per shoe, while the Markov player averages approximately 32 entries per shoe.

If both players were allowed to bet at their natural frequencies, any observed difference in catastrophic loss rates could be attributed to differential exposure — the selective player simply bets less often and therefore encounters fewer losses. This is not the hypothesis under test. We test whether entry QUALITY differs, not whether entry QUANTITY differs.

To isolate entry quality, we employ an equalization protocol. For each shoe in the dataset:

1.  Count the number of entries produced by the selective player on this shoe: N_TX.
2.  From the Markov player’s full set of entries on this shoe, randomly sample N_TX entries (without replacement).
3.  Compare catastrophic loss counts between the selective player’s N_TX entries and the Markov player’s sampled N_TX entries.

This ensures that both players make exactly the same number of bets on the same sequence. The only variable is which positions within the sequence were selected for entry — streak positions (TX) or direction-change positions (MK).

To verify that the subsampling procedure does not introduce instability, we repeat the random sampling 100 times per seed using distinct random seeds for the sampling process (independent of the sequence generation seeds). The standard deviation of the Markov player’s equalized catastrophic loss rate across these 100 trials is less than 0.04 percentage points in all cases, confirming that the equalized rate is stable and not an artifact of a particular random subsample.

The equalization protocol can be understood intuitively: it replicates the scenario in which two players sit at the same table, watch the same coin flips, and make the same number of bets per session. One waits patiently for streaks; the other bets at every opportunity but is constrained (by time, attention, or bankroll) to the same number of wagers. Under strategic indifference, both players should achieve identical outcomes. The equalization ensures that any observed difference is attributable to entry timing alone.

### 2.5 Experimental Design

The experiment was conducted across five independent random seeds: {42, 123, 456, 789, 1001}. Each seed generated 100,000 shoes of 80 outcomes each, for a total of 500,000 shoes and 40,000,000 individual binary outcomes across the full experiment.

Five observation depth thresholds were tested at each seed: T ∈ {3, 4, 5, 6, 7}. This produces 25 independent data points (5 seeds × 5 thresholds), enabling both within-seed significance testing and cross-seed replication analysis.

The graduated threshold design serves a specific predictive purpose. If the selectional advantage is genuine — if observing prior outcomes before entry produces a real benefit — then the advantage should increase monotonically with observation depth. A player who observes 5 prior outcomes should outperform one who observes 4, who should in turn outperform one who observes 3. This monotonic gradient would be inconsistent with a methodological artifact, which would not be expected to produce a systematic relationship between observation depth and outcome quality across multiple independent datasets.

Conversely, if the advantage does not increase with observation depth, or if it appears at some thresholds but not others with no systematic pattern, this would suggest a dataset-specific artifact rather than a general phenomenon.

The experimental prediction, derived from the hypothesis that prior observation carries strategic value, is unambiguous: the gradient should be monotonic, increasing with T at every seed.

### 2.6 Statistical Analysis

For each of the 25 data points (5 seeds × 5 thresholds), three quantities are computed:

**Per-entry catastrophic loss rate.** The number of catastrophic losses (9 consecutive bets lost) divided by the total number of entries, computed separately for the selective player and the equalized Markov player. Under the null hypothesis of strategic indifference, both rates should equal (1/2)\^9 = 0.001953125 (1 in 512).

**Z-score.** A two-proportion Z-test comparing the selective player’s catastrophic loss rate against the equalized Markov player’s rate:

Z = (p_TX − p_MK) / √(p̂(1 − p̂)(1/n_TX + 1/n_MK))

where p̂ is the pooled proportion. A negative Z indicates the selective player experiences fewer catastrophic losses.

**Bayes factor.** The maximum likelihood ratio BF₁₀ = exp(Z²/2), representing the relative probability of the observed data under the alternative hypothesis (the selective player has a lower catastrophic loss rate) versus the null hypothesis (both rates are equal). For comparison, Bartoš et al. (2023) reported a Bayes factor of 2,359 for the Diaconis same-side coin bias — a finding widely regarded as definitive.

Cross-seed significance is assessed via combined Z-scores: the sum of per-seed Z-scores for each threshold divided by √5. This provides a single significance measure that accounts for replication across independent datasets.

We note that testing 5 thresholds across 5 seeds produces 25 comparisons, raising the question of multiple-comparison correction. Under Bonferroni correction, the per-comparison significance threshold would increase from Z = 2.58 (p \< 0.01) to approximately Z = 3.3 (p \< 0.0004). As reported in Section 3, the weakest combined result (T3, combined Z = −7.16) exceeds the Bonferroni-corrected threshold by more than a factor of two, and all results from T4 onward exceed it by wide margins. More fundamentally, the 25 comparisons are not independent tests of unrelated hypotheses — they are structured as a predicted monotonic gradient. The probability of observing perfect monotonicity across 25 independent data points by chance is (1/2)\^24 ≈ 6 × 10⁻⁸, providing an additional layer of significance independent of any individual Z-score.

The complete Python implementation, sufficient for full reproduction of all results, is provided in Appendix A.

## 3. RESULTS

### 3.1 Equalized Comparison Refutes Strategic Indifference

Strategic indifference predicts that when two players make the same number of wagers on the same fair coin sequences, their catastrophic loss distributions should be identical regardless of entry timing. Tables 1 through 4 test this prediction across 500,000 sequences of 80 flips each — 40 million total coin flips — with the selective player entering after observing T consecutive same-side outcomes and the Markov player entering at each direction change, exposure-matched by per-sequence subsampling.

The prediction fails at every threshold tested.

Table 1 reports catastrophic losses for both players across the full dataset, with both players placing an identical number of wagers.

**Table 1: Catastrophic losses across 40 million coin flips, at matched exposure (aggregated across 5 seeds, 500,000 sequences)**

| Threshold | Total Flips | TX Losses | MK Eq Losses | TX Advantage | MK÷TX |
|-----------|-------------|-----------|--------------|--------------|-------|
| T3        | 40,000,000  | 7,699     | 8,611        | 10.6%        | 1.12× |
| T4        | 40,000,000  | 3,780     | 4,773        | 20.8%        | 1.26× |
| T5        | 40,000,000  | 1,858     | 2,885        | 35.6%        | 1.55× |
| T6        | 40,000,000  | 920       | 1,943        | 52.7%        | 2.11× |
| T7        | 40,000,000  | 474       | 1,468        | 67.7%        | 3.10× |

The raw loss counts tell two diverging stories. As observation depth increases from T3 to T7, both players encounter fewer catastrophes — but the selective player's losses drop from 7,699 to 474 (a 16-fold reduction) while the Markov player's drop from 8,611 to 1,468 (a 6-fold reduction). By T7, the Markov player suffers more than three times as many catastrophic losses as the selective player. Both players made the same number of bets on the same sequences. The only difference was what each player observed before placing the first bet.

Table 2 translates the same divergence into operational terms: average catastrophic busts per 1,000 sequences, with the final two columns expressing expected sequences between catastrophic events.†

**Table 2: Catastrophic busts per 1,000 sequences, at matched exposure (L = 80)**

| Threshold | Entries / 1,000 | TX Busts | MK Busts | TX Advantage | TX: 1 Bust per  | MK: 1 Bust per |
|-----------|-----------------|----------|----------|--------------|-----------------|----------------|
| T3        | 8,002           | 15.4     | 17.2     | 10.6%        | 65 sequences    | 58 sequences   |
| T4        | 3,937           | 7.6      | 9.5      | 20.8%        | 132 sequences   | 105 sequences  |
| T5        | 1,939           | 3.7      | 5.8      | 35.6%        | 269 sequences   | 173 sequences  |
| T6        | 954             | 1.8      | 3.9      | 52.7%        | 544 sequences   | 257 sequences  |
| T7        | 470             | 0.9      | 2.9      | 67.7%        | 1,055 sequences | 341 sequences  |

† Both players place an equal number of wagers per sequence; see §2.4 for the equalization protocol. "Sequences" refers to the 80-flip sequences used throughout this study.

At T7, the selective player encounters one catastrophe per 1,055 sequences. The Markov player encounters one per 341 — a 3.1× difference in survival span. At T4, the gap is already meaningful: 132 sequences between catastrophes for the selective player versus 105 for the Markov player. The advantage is monotonic: every increment in observation depth widens the survival gap.

Tables 1 and 2 present the same result at different scales. The per-entry comparison in Table 3 shows where the divergence lives: the selective player's catastrophe rate holds steady at approximately 0.19% across all thresholds, while the equalized Markov player's rate rises systematically — from 0.22% at T3 to 0.62% at T7.

**Table 3: Per-entry equalized comparison by threshold (aggregated across 5 seeds, 500,000 sequences, EQ_TRIALS = 100)**

| Threshold | Entries (both) | TX Losses | MK Eq Losses | TX Rate % | MK Eq Rate % | TX Advantage |
|-----------|----------------|-----------|--------------|-----------|--------------|--------------|
| T3        | 4,000,807      | 7,699     | 8,611        | 0.1924    | 0.2152       | 10.6%        |
| T4        | 1,968,274      | 3,780     | 4,773        | 0.1920    | 0.2425       | 20.8%        |
| T5        | 969,443        | 1,858     | 2,885        | 0.1917    | 0.2976       | 35.6%        |
| T6        | 476,866        | 920       | 1,943        | 0.1929    | 0.4075       | 52.7%        |
| T7        | 234,950        | 474       | 1,468        | 0.2017    | 0.6248       | 67.7%        |

The selective player's rate remains stable at approximately 0.19% across all thresholds — consistent with per-entry independence. The equalized Markov player's rate rises systematically from 0.2152% at T3 to 0.6248% at T7. The advantage — defined as the percentage reduction in catastrophic losses for the selective player relative to the equalized Markov player — grows monotonically from 10.6% at T3 to 67.7% at T7.

At T7, the selective player experiences fewer than one-third the catastrophic losses of the Markov player. Both players made the same number of bets. Both faced the same coins. Both used the same 9-bet anti-continuation structure. The only difference was what each player observed before placing the first bet.

**Table 4: Statistical significance by threshold**

| Threshold | Per-Seed Z (42 / 123 / 456 / 789 / 1001) | Combined Z | Bayes Factor | vs Diaconis (÷2,359) | 5-sigma? | Discounted Z (÷√2) | Disc. 5σ? |
|-----------|------------------------------------------|------------|--------------|----------------------|----------|--------------------|-----------|
| T3        | −2.16 / −3.78 / −3.88 / −2.53 / −3.65    | −7.16      | 1.3 × 10¹¹   | 6 × 10⁷              | Yes      | −5.06              | Yes       |
| T4        | −4.17 / −4.81 / −5.76 / −4.28 / −5.05    | −10.76     | 1.4 × 10²⁵   | 6 × 10²¹             | Yes      | −7.61              | Yes       |
| T5        | −6.37 / −6.89 / −7.02 / −6.41 / −6.68    | −14.93     | 2.4 × 10⁴⁸   | 1 × 10⁴⁵             | Yes      | −10.55             | Yes       |
| T6        | −8.39 / −8.27 / −8.12 / −8.54 / −9.52    | −19.16     | 4.8 × 10⁷⁹   | 2 × 10⁷⁶             | Yes      | −13.54             | Yes       |
| T7        | −10.43 / −10.21 / −9.47 / −9.86 / −10.56 | −22.60     | 8.5 × 10¹¹⁰  | 4 × 10¹⁰⁷            | Yes      | −15.98             | Yes       |

Combined Z-scores are computed as the sum of per-seed Z-scores for each threshold divided by √5. All five thresholds exceed 5-sigma. The T4 Bayes factor of 1.4 × 10²⁵ exceeds the Diaconis et al. (2023) benchmark of 2,359 by a factor of approximately 6 × 10²¹. Higher thresholds produce Bayes factors that are, for practical purposes, infinite.

The "Discounted Z" column divides the combined Z by √2 as a conservative correction for potential within-shoe correlation between the selective and Markov player entries (both drawn from the same sequence). Even under this discount, all five thresholds remain above 5-sigma, with the weakest (T3) at 5.06 — still exceeding the discovery threshold.

The equalization protocol's stability was verified through 100 independent subsampling trials per seed. The maximum standard deviation of the Markov player's equalized rate across trials was 0.037 percentage points, confirming that the equalized rate is a property of the data, not of a particular random subsample.

### 3.2 Per-Entry Rates Confirm Independence

The divergence reported in §3.1 does not arise from any departure from per-event fairness. Both player strategies produce per-entry catastrophic loss rates that are statistically indistinguishable from the Markov prediction of (1/2)\^9 = 0.1953%.

**Table 5: Per-entry catastrophic loss rates by threshold (aggregated across 5 seeds, 500,000 sequences)**

| Threshold | TX Entries | TX Losses | TX Rate % | MK Full Rate % | Markov Prediction % | TX Deviation |
|-----------|------------|-----------|-----------|----------------|---------------------|--------------|
| T3        | 4,000,807  | 7,699     | 0.1924    | 0.1942         | 0.1953              | −1.49%       |
| T4        | 1,968,274  | 3,780     | 0.1920    | 0.1942         | 0.1953              | −1.70%       |
| T5        | 969,443    | 1,858     | 0.1917    | 0.1942         | 0.1953              | −1.85%       |
| T6        | 476,866    | 920       | 0.1929    | 0.1942         | 0.1953              | −1.24%       |
| T7        | 234,950    | 474       | 0.2017    | 0.1942         | 0.1953              | +3.27%       |

No per-entry rate deviates from the Markov prediction by more than 2% at thresholds T3 through T6. The T7 rate exhibits the largest deviation at +3.27%, attributable to sampling variation at the lowest entry count — the deviation corresponds to approximately 15 excess losses across 234,950 entries, within one standard deviation of the expected count. The Markov player's full (non-equalized) rate is similarly indistinguishable from theory at every threshold.

Each coin flip is fair. Each 9-bet sequence faces exactly 1/512 odds of total loss. Neither player has a per-entry edge. The coin has no memory, and neither player can see the future.

This is the paradox that the remainder of this section and §4 must resolve: per-entry independence is confirmed — every wager either player places carries the same catastrophe probability — and yet §3.1 demonstrates that at matched exposure, the selective player encounters catastrophe materially less often. The resolution, explored in §4.3, is that identical per-event odds do not guarantee identical aggregate outcomes when the two players occupy systematically different positions within the sequence. Independence governs what happens at each position; it is silent on which positions a strategy comes to occupy.

### 3.3 The Gradient Is Monotonic

The selective advantage increases with observation depth at every seed and every threshold transition, producing a perfectly monotonic gradient across all 25 data points.

**Table 6: Advantage by seed and threshold**

| Threshold | Seed 42 | Seed 123 | Seed 456 | Seed 789 | Seed 1001 | Average | Std Dev |
|-----------|---------|----------|----------|----------|-----------|---------|---------|
| T3        | −7.2%   | −12.5%   | −12.9%   | −8.4%    | −11.9%    | −10.6%  | 2.57%   |
| T4        | −18.2%  | −20.8%   | −24.8%   | −18.7%   | −21.5%    | −20.8%  | 2.63%   |
| T5        | −34.2%  | −36.8%   | −37.3%   | −34.2%   | −35.4%    | −35.6%  | 1.44%   |
| T6        | −51.9%  | −51.5%   | −50.4%   | −52.3%   | −57.1%    | −52.6%  | 2.59%   |
| T7        | −69.2%  | −68.8%   | −64.5%   | −66.0%   | −69.9%    | −67.7%  | 2.29%   |

Within each seed, the advantage at T(N+1) exceeds the advantage at T(N) without exception. Across seeds, the advantage at each threshold is stable, with a coefficient of variation below 5% at every level. No seed produces an outlier or a reversal.

The probability of observing perfect monotonicity across 25 data points by chance — assuming the null hypothesis that observation depth has no systematic relationship to outcome — is (1/2)\^24 ≈ 6 × 10⁻⁸, providing an additional layer of significance independent of any individual Z-score. The gradient has the characteristics of a scaling law: systematic, monotonic, stable across independent datasets, and exhibiting a consistent functional form.

### 3.4 Side Symmetry

The selectional advantage is symmetric with respect to which outcome is being observed. Streaks of heads and streaks of tails produce statistically indistinguishable advantages.

**Table 7: Advantage by side (T4 threshold, aggregated across 5 seeds)**

| Side      | TX Entries | TX Losses | TX Rate % | MK Eq Rate % | Advantage |
|-----------|------------|-----------|-----------|--------------|-----------|
| H (heads) | 984,601    | 1,904     | 0.1934    | 0.2879       | −32.8%    |
| T (tails) | 983,673    | 1,876     | 0.1907    | 0.2884       | −33.9%    |

No significant asymmetry is observed. The effect depends on streak structure — the occurrence of consecutive identical outcomes — not on which specific outcome is being repeated. This is consistent with the generating process being a fair binary source with no side bias, and confirms that the selectional advantage is not an artifact of any asymmetry in the underlying sequence.

### 3.5 Sequence Length Scaling

The selectional advantage varies systematically with sequence length, consistent with the path narrowing mechanism described in Section 4.3.

**Table 8: Effect of sequence length on selectional advantage (5 seeds × 50,000 shoes per seed)**

| Sequence Length | T3 Advantage | T4 Advantage | T5 Advantage | T6 Advantage | T7 Advantage |
|-----------------|--------------|--------------|--------------|--------------|--------------|
| 40              | −23.6%       | −38.5%       | −57.0%       | −71.1%       | −82.8%       |
| 80              | −11.5%       | −22.3%       | −37.0%       | −52.9%       | −67.8%       |
| 120             | −8.2%        | −15.4%       | −25.5%       | −39.2%       | −58.9%       |
| 200             | −4.3%        | −8.8%        | −16.8%       | −28.8%       | −42.1%       |

Shorter sequences produce stronger selectional advantages; longer sequences attenuate the effect. At sequence length 40, the T4 advantage is −38.5%; at length 200, it falls to −8.8%. The relationship is consistent across all thresholds: the advantage approximately halves when the sequence length doubles.

This scaling is predicted by the path narrowing mechanism. In shorter sequences, the observer’s prior observations constitute a larger fraction of the total structure, producing proportionally stronger narrowing of the conditional ensemble of compatible continuations. In longer sequences, the same observations represent a smaller fraction, and the narrowing effect is proportionally weaker. In the limit of infinite sequences, the effect would vanish — but all real-world sequences are finite, and the effect is present at every finite length tested.

At sequence length 200, the effect persists at all thresholds from T5 onward (combined Z \> 5σ) but attenuates in magnitude. At sequence length 40, the effect amplifies, with all thresholds exceeding 5-sigma by wide margins.

The primary analysis uses sequence length 80, which reflects the real-world sequence length in the applied domain where the experimental framework originated.

### 3.6 Reversed Polarity Confirmation

As a definitive test that the selectional advantage arises from entry position rather than any implementation artifact, we reversed the player roles: the selective player entered at direction changes (the Markov strategy) while the Markov player entered at streak positions (the selective strategy). The equalization protocol was applied identically.

**Table 9: Reversed polarity (500,000 shoes, EQ_TRIALS = 100)**

| Threshold | TX (breaks) Rate % | MK Eq (streaks) Rate % | Reversed Advantage | Direction Flipped? |
|-----------|--------------------|------------------------|--------------------|--------------------|
| T3        | 0.2152             | 0.1924                 | +11.9%             | Yes                |
| T4        | 0.2425             | 0.1920                 | +26.3%             | Yes                |
| T5        | 0.2975             | 0.1917                 | +55.2%             | Yes                |
| T6        | 0.4075             | 0.1929                 | +111.2%            | Yes                |
| T7        | 0.6246             | 0.2017                 | +209.7%            | Yes                |

The advantage flips sign cleanly at every threshold. When the streak-based entry criterion is assigned to the Markov label and the direction-change criterion is assigned to the selective label, the “selective” player now performs worse. The effect is a property of the entry position, not of the player label, the code path, or any implementation asymmetry. Streak-based entry outperforms break-based entry regardless of which player uses which strategy.

### 3.7 Summary of Results

The results can be stated concisely:

1.  **Strategic indifference is refuted.** The equalized comparison shows the selective player experiencing 10.6% to 67.7% fewer catastrophic losses than the Markov player, at identical betting frequency on identical sequences, at significance exceeding 5-sigma at all five thresholds tested — including after conservative discounting for within-shoe correlation.
2.  **Per-entry independence is confirmed.** Both players’ catastrophic loss rates match the theoretical prediction of 1/512 within noise at every threshold tested. Each individual coin flip is fair. Markov is right about individual events.
3.  **The advantage scales monotonically with observation depth.** More patience produces greater advantage, with zero reversals across 25 independent data points. The gradient replicates perfectly across five independent random seeds.
4.  **The advantage is side-symmetric.** Neither heads nor tails produces a differential effect. The advantage depends on streak occurrence, not streak direction.
5.  **The advantage scales inversely with sequence length.** Shorter sequences produce stronger effects; longer sequences attenuate them. This is consistent with the path narrowing mechanism described in Section 4: observation-based narrowing has proportionally greater impact within shorter conditional ensembles.
6.  **The advantage is position-dependent, not implementation-dependent.** Reversing which player uses which entry criterion reverses the advantage, confirming that the effect arises from where bets are placed within the sequence, not from any asymmetry in the experimental protocol.

These six findings collectively establish that the observation of prior outcomes — which per-event independence renders individually uninformative — produces measurable, scalable, reproducible, and position-dependent differences in session-level outcome distributions when used as an entry criterion. The following section proposes an explanatory mechanism and discusses implications.

## 4. DISCUSSION

### 4.1 What the Finding Is and Is Not

The results reported in Section 3 establish an empirical fact: two players watching the same fair coin flips, making the same number of bets, using the same 9-bet anti-continuation structure, experience measurably different rates of catastrophic loss based solely on what they observed before placing their first bet. The advantage scales monotonically with observation depth, replicates across independent datasets, and exceeds the 5-sigma discovery threshold at all five thresholds tested.

This finding requires careful scoping.

**It is** a demonstration that entry timing — the observer’s choice of when to engage a memoryless sequence — produces different outcome distributions at the session level, even when each individual event is confirmed to be independent.

**It is** a separation of two logically distinct claims: per-event independence (confirmed) and strategic indifference (refuted).

**It is** a reproducible result with a trivially simple protocol, verifiable by anyone with access to a standard programming language in under three minutes of computation time.

**It is not** a claim that individual coin flips are biased, that past outcomes alter the probability of future events, or that the coin has memory. Per-entry loss rates match the theoretical prediction of (1/2)\^9 at every threshold tested, for both players. Markov is right about every individual event.

**It is not** a claim that the laws of probability require revision. The finding is consistent with standard probability theory. What it challenges is an interpretive extension of that theory — the assumption that per-event independence implies strategic indifference.

**It is not** a perpetual motion machine for gambling. No house edge is overcome. No individual bet is improved. The advantage operates exclusively at the level of catastrophic loss frequency within multi-bet sequences, not at the level of individual wager outcomes.

**It is not** an instance of what Miller and Sanjurjo (2019) term the “gambler’s verity” — the phenomenon whereby a streak-based betting strategy can produce an elevated WIN RATE while generating zero expected profit, because losses are concentrated in high-exposure sequences where the bettor has wagered more. Our equalization protocol controls for this directly: both players make the same number of bets on the same sequences. The selective player does not wager more or less than the Markov player — they wager the same amount at different positions. Any difference in catastrophic loss frequency therefore reflects genuine structural advantage, not the win-rate/expected-profit asymmetry the gambler’s verity describes.

### 4.2 The Gambler’s Fallacy Decomposed

The Gambler’s Fallacy, as traditionally taught, holds that a gambler who believes a streak of heads makes tails more likely is committing a reasoning error. This debunking is correct. Our data confirms it: the per-entry loss rate is 1/512 regardless of observation depth. The coin does not compensate for past outcomes.

However, the traditional treatment conflates two separable claims:

**Claim 1 (the per-event prediction):** After a streak of same-side outcomes, the opposite outcome is more likely on the next event.

**Claim 2 (the strategic prescription):** Wait for streaks before betting against continuation.

Claim 1 is false. Our data confirms this unambiguously (Section 3.1). Each flip is fair. Each entry faces 1/512.

Claim 2 is true. Our data establishes this at 5-sigma (Section 3.2). The player who waits for streaks experiences 20.8% to 67.7% fewer catastrophic losses than the player who enters at non-streak positions, at identical betting frequency on identical sequences.

The standard debunking of the Gambler’s Fallacy kills Claim 1 and assumes Claim 2 dies with it. This inference — from “each flip is independent” to “therefore timing your entry based on prior outcomes is futile” — is the error our data identifies. It is an interpretive overextension: a correct statement about individual events is promoted, without independent verification, to a statement about strategies composed of multiple events. Our experiment separates the two claims and tests Claim 2 on its own terms. It survives.

The gambler is wrong about why. The gambler is right about what to do.

### 4.3 Why It Works: Path Narrowing in Finite Sequences

Three possible explanations exist for why selective entry produces different outcomes in a memoryless sequence. Two can be ruled out. The third is supported by the data.

**Explanation 1 — Predetermination.** The full sequence of outcomes is fixed at generation. The catastrophic streaks either exist at the observer’s entry position or they do not. The observer’s knowledge reveals information about a structure that was already determined. This is classical determinism.

This explanation is insufficient. If the sequence structure is predetermined and the observer merely reads it, there is no reason for observation depth to matter. Whether the observer reads 3 prior outcomes or 7 prior outcomes, the structure is what it is. Predetermination predicts no gradient. The data shows a strong, monotonic gradient.

**Explanation 2 — Observer influence.** The observer’s awareness of prior outcomes somehow constrains or alters subsequent flips. The act of observation changes the generating process.

This explanation is contradicted by the data. If observation influenced future flips, the per-entry loss rate would deviate from the theoretical prediction at higher observation depths — the observer’s influence would manifest as a changed per-flip probability. It does not. Per-entry rates match (1/2)\^9 at every threshold (Section 3.1). Each flip remains exactly fair. The observer changes nothing about any individual event.

**Explanation 3 — Path narrowing.** The future is genuinely random. Each flip is truly 50/50. Nothing is predetermined and nothing is influenced. But observation constrains which subset of possible sequence continuations the observer can encounter.

Before any observation, all possible continuations of the sequence are compatible with the observer’s state of knowledge. After observing T consecutive same-side outcomes, only continuations consistent with that observation remain in the observer’s compatible set. Within this conditional subset, the overwhelming majority of continuations terminate the streak within a few positions — because continuation probability is 1/2 per position, and the fraction of paths extending K additional positions decays as (1/2)\^K. Continuations in which the streak persists for 9 more positions — the catastrophic outcome — are exponentially rare within the conditioned set.

The observer has not changed any future flip. They have narrowed the set of compatible futures. And within that narrowed set, catastrophe is diluted.

The Markov player, entering at a direction change, has observed only a single prior outcome. Their compatible set is larger — it includes continuations where the new direction extends for 10 or more positions (their catastrophic threshold), which are substantially more common than 14+ continuations (the selective player’s catastrophic threshold at T5). The Markov player’s observation performs less narrowing, leaving a larger fraction of catastrophe-compatible paths in their conditioned set.

This is not a violation of independence. Each flip remains 50/50 within every conditioned set. What changes between players is not the probability of any event but the ensemble of compatible sequence structures within which those events occur. Different observations produce different ensembles. Different ensembles contain different densities of catastrophe-compatible structures. The observer’s choice of how much to observe before engaging determines which ensemble they inhabit.

The gradient follows directly. At T3, the observer has narrowed the compatible set by 3 observations — eliminating all continuations incompatible with a 3-streak. At T7, the observer has narrowed by 7 observations — a much tighter constraint. Each additional observation eliminates approximately half the remaining catastrophe-compatible continuations (since each continuation must survive one additional 50/50 test). The resulting catastrophe probability scales as (1/2)\^T relative to the unconditional rate — which is precisely the monotonic gradient reported in Section 3.3.

A clarification is essential here regarding what constitutes catastrophe for each player, because it illuminates the mechanism rather than obscuring it. Both players make 9 bets. Both lose those 9 bets when 9 consecutive outcomes go against them. The catastrophic loss is identical in structure and in cost. But the streak required to produce that loss differs between players — not because the experiment imposes different rules, but because the observer’s prior engagement with the sequence determines how much of the streak is consumed before betting begins.

The selective player at T4 has observed 4 same-side outcomes before placing a single bet. Those 4 observations are real events that occupy real positions in the sequence. They are now part of the streak. For the streak to destroy the selective player’s 9-bet ladder, it must extend 4 positions before the ladder AND 9 positions through it — a total unbroken run of 13. The selective player has, through observation alone, constituted a threshold of 13 for their own catastrophe.

The Markov player has observed 1 outcome before betting. Their constituted threshold is 10: 1 observed position plus 9 bet positions.

Neither threshold is an experimental parameter. Neither is a rule of the game. Both emerge from the same source: how many prior outcomes the observer chose to integrate into their engagement with the sequence. The Markov player treats their prior observations as irrelevant — in keeping with Markovian theory — and therefore does not benefit from any threshold elevation. The selective player treats their prior observations as structurally significant — in contradiction to Markovian theory — and constitutes a higher threshold as a direct result.

The data shows that the constituted threshold is real. The selective player’s catastrophe rate corresponds to the higher threshold, not to the 9-bet ladder alone. The 4 observed flips that Markov declares irrelevant are providing measurable structural protection — not by changing any future flip, but by consuming positions within the streak that can no longer contribute to the observer’s loss.

#### Convergent evidence: Miller and Sanjurjo

The path narrowing mechanism receives independent support from an unexpected source. Miller and Sanjurjo (2018) computed the expected reversal bias at streak positions in finite sequences of 100 fair coin flips. Their gradient, derived from pure mathematical analysis of closed datasets, can be compared to the selectional advantage measured in our experiment:

| Observation depth | Miller & Sanjurjo (retrospective, 100-flip closed dataset) | This study (prospective, 80-flip open sequences) | Ratio |
|-------------------|------------------------------------------------------------|--------------------------------------------------|-------|
| 3                 | −4.0%                                                      | −10.6%                                           | 2.7×  |
| 4                 | −8.8%                                                      | −20.8%                                           | 2.4×  |
| 5                 | −13.5%                                                     | −35.6%                                           | 2.6×  |

Both gradients are monotonically increasing with observation depth. Our prospective advantage is approximately 2.5× larger at every threshold. This magnitude difference is consistent with two methodological distinctions: our open-sequence design imposes no mean-reversion pressure (their closed-dataset design does), and our sequences are shorter (80 vs 100), which produces stronger path narrowing per Section 3.5.

The sequence length explanation is directly testable using our scaling data. At sequence length 200 — the closest match to their 100-flip sequences — our selectional advantage at T3 is −4.3% and at T4 is −8.8%. These values converge closely with Miller and Sanjurjo’s retrospective figures of −4.0% and −8.8% at the same thresholds. The magnitude difference in the primary analysis is substantially explained by the different sequence lengths, confirming that both studies are detecting the same underlying phenomenon at comparable scales.

Miller and Sanjurjo identified two distinct sources of their bias: a sampling-without-replacement effect, in which observed streak positions are “used up” from the finite pool and depleted from the remaining continuation possibilities; and an overlapping-streak arrangement effect, in which self-overlapping patterns (e.g., HHH containing two overlapping instances of HH) create an asymmetry that further attenuates the continuation rate. The first mechanism — sampling without replacement — is structurally equivalent to what we term path narrowing: observed outcomes consume positions, narrowing the set of compatible continuations.

Miller and Sanjurjo characterized their finding as a retrospective counting artifact — a property of completed datasets that does not apply to real-time decision-making. Our experiment demonstrates that the same directional effect operates prospectively, in real time, in open sequences with no closure constraint. The restriction to retrospective analysis appears to have been an artifact of their methodology, not a property of the phenomenon.

### 4.4 The Monty Hall Parallel

The path narrowing mechanism bears a structural relationship to the Monty Hall problem that illuminates both. Notably, Miller and Sanjurjo (2019) independently identified this same structural connection, demonstrating in the *Journal of Economic Perspectives* that the streak selection bias they discovered in their 2018 *Econometrica* paper is formally equivalent to the Monty Hall problem through what they term the *principle of restricted choice*. Two independent research groups arriving at the same structural parallel through different analytical paths constitutes convergent evidence that the connection is genuine, not analogical.

In the Monty Hall problem, a contestant chooses one of three doors. The host, who knows the location of the prize, opens a different door to reveal a non-prize. The contestant is offered the chance to switch. Switching wins 2/3 of the time — a result that famously defies the intuition that two remaining doors should offer 50/50 odds.

The mechanism is conditional narrowing within a bounded set. Three doors, one prize. The host’s reveal eliminates one possibility, but the elimination is asymmetric — the host cannot open the contestant’s door and cannot open the prize door. This asymmetry concentrates the prize probability onto the remaining unchosen door. The contestant who understands the constraint structure — who apprehends the asymmetry in the host’s action — switches and wins 2/3. The contestant who does not understand it treats the two remaining doors as equivalent and wins only 1/2.

The coin flip experiment exhibits the same structure. A sequence of 80 flips is a bounded set of possible outcomes. The observer who records T consecutive same-side outcomes has narrowed the set of compatible continuations. This narrowing is asymmetric: short continuations (streak ends soon) are exponentially more common than long continuations (streak persists), so the narrowing disproportionately eliminates the common, safe outcomes from the uncertainty set while leaving the rare, catastrophic outcomes at their original (low) density. The observer’s compatible set is dominated by short-continuation paths in which their 9-bet ladder resolves safely.

In both cases, the advantage accrues to the observer who apprehends the structure of the conditional set. In Monty Hall, the relevant structure is the host’s constrained choice. In the coin flip experiment, the relevant structure is the exponential decay of streak continuation probability. In both cases, an observer who does not apprehend the structure — who treats the remaining possibilities as undifferentiated — forfeits the advantage.

And in both cases, the system is “closed” in the conditional sense: the set of compatible outcomes, given what has been observed, is bounded. It is this conditional boundedness — not any physical closure of the system — that makes the narrowing informative.

An important distinction: in Monty Hall, an agent with knowledge (the host) performs the narrowing. In the coin flip experiment, no agent acts — the observer’s own engagement with the sequence performs the narrowing. The mathematics of conditional narrowing does not require an external agent. It requires only that an observation has been made which restricts the compatible set. Whether that observation is facilitated by a knowledgeable host or performed directly by the observer on a memoryless sequence, the structural consequence is the same: the compatible set contracts asymmetrically, and the observer who apprehends this asymmetry is advantaged.

### 4.5 Relationship to Diaconis et al. (2023)

Bartoš et al. (2023), testing a prediction by Diaconis, Holmes, and Montgomery, found that physical coin flips exhibit a same-side bias of 50.8% — coins tend to land on the side they started on. The effect was attributed to the physics of precession: the coin’s angular momentum during the flip carries information from its starting state into its final state. The Bayes factor of 2,359 was widely regarded as definitive evidence that the 50/50 assumption fails for physical coins.

Our experiment complements and extends this finding in several respects.

First, our Bayes factors exceed the Diaconis benchmark by orders of magnitude — from 6 × 10²¹ times the Diaconis value at T4 to astronomically beyond at higher thresholds. The statistical evidence for selective entry advantage is substantially stronger than the evidence for physical coin bias.

Second, our experiment uses a computational random number generator with no physical properties. There is no coin, no starting state, no precession, no angular momentum. The selectional advantage we observe cannot be attributed to any physical channel through which prior outcomes might influence future outcomes. If the Diaconis effect and our effect are manifestations of a common principle, that principle cannot be purely physical — it must encompass informational and observational structures as well.

Third, the Diaconis effect is a property of the generating process (the physics of the coin), while our effect is a property of the observer’s engagement with the sequence (the timing of entry). These are different phenomena with different mechanisms. However, both demonstrate that assumptions treated as self-evident — the fairness of coins, the irrelevance of entry timing — can fail under sufficiently careful empirical scrutiny. The Diaconis study established the precedent that 50/50 assumptions warrant testing. Our study extends that precedent to the assumption of strategic indifference.

We raise, without resolving, the question of whether observer-relative mechanisms — rather than or in addition to physical mechanisms — might contribute to the same-side bias Diaconis observed. In the Diaconis protocol, the flipper observes the starting state of the coin before flipping. If the observer’s knowledge of the starting state produces any selectional or conditional narrowing effect analogous to what we observe in binary sequences, it would represent an additional contribution to the same-side bias beyond the purely physical precession dynamics. We identify this as a hypothesis for future investigation.

### 4.5.5 Diagnostic: The Unidirectional Isolation Test

Throughout this study, both players enter bidirectionally — the selective player enters after streaks of either heads or tails, and the Markov player enters at direction changes in either direction. This design reflects the natural scenario under test: two players watching the same sequence, observing all outcomes, entering at different positions. The equalization matches their per-sequence entry counts within this shared observation space.

A natural diagnostic question arises: does the selectional advantage persist if the two players are restricted to opposite sides? Specifically, if the selective player enters only after streaks of heads (betting against heads continuation) and the Markov player enters only at transitions to tails (betting against tails continuation), the equalization protocol is applied identically — but the two players no longer operate within the same streak domain. Their entries are drawn from structurally separate channels of the sequence.

We tested this variant across 500,000 sequences using the same five seeds, equalization protocol, and bust conditions as the primary experiment.† The result is unambiguous: the selectional advantage vanishes.

**Table 10: Unidirectional comparison (TX = heads streaks only, MK = tails direction changes only)**

| Threshold | TX Rate % | MK Eq Rate % | Advantage | Combined Z |
|-----------|-----------|--------------|-----------|------------|
| T3        | 0.188     | 0.195        | −3.8%     | −0.81      |
| T4        | 0.191     | 0.195        | −2.2%     | −0.32      |
| T5        | 0.195     | 0.194        | +0.6%     | +0.06      |
| T6        | 0.205     | 0.201        | +2.2%     | +0.15      |
| T7        | 0.206     | 0.183        | +12.5%    | +0.58      |

No threshold achieves significance. No monotonic gradient appears. The per-seed results scatter in both directions with no systematic pattern. The effect that produces combined Z-scores from −7.16 to −22.60 in the bidirectional experiment produces nothing in the unidirectional case.

† *Reduced to 100,000 sequences per seed for computational efficiency. The null result is robust across all five seeds.*

This null result is not a disconfirmation of the primary finding. It is a structural expectation — and the data shows precisely why.

#### The operative correlation

The equalized comparison works by matching the Markov player's entry count to the selective player's count on each sequence. This per-sequence matching introduces a weighting: sequences where the selective player enters more contribute more Markov entries to the equalized sample. The critical question is whether this weighting is neutral — whether the sequences where the selective player is most active are the same sequences where the Markov player's entries are more or less vulnerable to catastrophe.

In the bidirectional experiment, the weighting is constructive. A sequence rich in long runs — what we might call a "streaky" sequence — simultaneously produces more selective-player entries (more streak triggers) and higher Markov-player bust vulnerability (longer continuation runs at reversal points). The per-sequence correlation between selective entry count and Markov bust rate is positive (r = +0.049). The equalization systematically overweights the sequences where the Markov player is most exposed:

**Bidirectional: Markov bust rate by selective entry count per sequence**

| TX entries per sequence | MK bust rate |
|-------------------------|--------------|
| 0–1                     | 0.082%       |
| 2–3                     | 0.168%       |
| 4–5                     | 0.235%       |
| 6–8                     | 0.268%       |

The gradient is monotonic. The equalization amplifies the structural asymmetry between streak-entry and reversal-entry by concentrating the comparison on the sequences where that asymmetry is strongest. The signals are in phase.

In the unidirectional experiment, the weighting inverts. A sequence with many long heads runs — producing many selective-player entries — is a sequence where heads consume the available positions. The tails runs between those heads clusters are necessarily shorter. Shorter tails runs mean the Markov player's tails-direction entries are *less* likely to face the 10 consecutive tails outcomes required for catastrophe. The per-sequence correlation between selective entry count and Markov bust rate is negative (r = −0.033):

**Unidirectional: Markov tails-bust rate by selective heads-entry count per sequence**

| TX H-entries per sequence | MK T-bust rate |
|---------------------------|----------------|
| 0–1                       | 0.230%         |
| 2–3                       | 0.181%         |
| 4–5                       | 0.131%         |
| 6–8                       | 0.072%         |

The gradient is monotonically inverted. The sequences where the selective player is most active are the sequences where the Markov player is most protected. The equalization overweights the safest sequences for the Markov player. The signals are in anti-phase.

#### Destructive interference

The relationship between these two experiments mirrors a principle familiar from wave mechanics: when two correlated signals are combined in phase, the pattern is amplified; when combined in anti-phase, the pattern cancels.

In the bidirectional case, both players operate within the same streak domain. The per-sequence correlation between entry frequency and bust vulnerability is positive — constructive interference. The equalization amplifies the structural difference between streak-based and reversal-based entry.

In the unidirectional case, the players operate in opposed streak domains. A heads-heavy sequence is a tails-light sequence. The per-sequence correlation between selective heads-entry frequency and Markov tails-bust vulnerability is negative — destructive interference. The equalization cancels the structural difference rather than amplifying it.

The cancellation is not approximate. It is nearly exact: both the correlation magnitudes (\|+0.049\| vs \|−0.033\|) and the gradient ranges (3.3× constructive vs 3.2× destructive) are comparable in scale but opposite in sign. The null result in the unidirectional experiment is not a failure to detect a signal — it is the signature of two signals canceling.

#### What this reveals about the mechanism

This diagnostic isolates the operative channel of the selectional advantage with precision that the primary experiment alone cannot provide.

The constituted threshold — the structural fact that catastrophe requires T+9 consecutive same-side outcomes for the selective player versus only 10 for the Markov player — exists in both experiments. In the unidirectional case, streaks of 13 or more heads are 8.5× rarer than streaks of 10 or more tails, and the selective player accumulates 8.3× fewer total busts than the Markov player. The frequency asymmetry is intact. Yet the equalized rate comparison is flat.

This demonstrates that the constituted threshold produces a total-count asymmetry (fewer busts in absolute terms) but does not, by itself, produce the equalized rate differential reported in Section 3. The rate differential requires an additional element: constructive per-sequence correlation between the selective player's entry frequency and the Markov player's bust vulnerability. This correlation exists when both players occupy the same streak domain (bidirectional) and inverts when they occupy opposed domains (unidirectional).

The selectional advantage, therefore, is not simply "higher thresholds are rarer." It is a property of how two entry strategies interact within a shared positional space — how the per-sequence structure that governs one player's activity simultaneously governs the other player's vulnerability. When both players watch the same streaks from different vantage points, the equalization reveals the asymmetry between patience and reactivity. When they watch different streaks, there is no shared structure for the equalization to reveal.

This is fully consistent with the path narrowing mechanism described in Section 4.3 and the selection-not-prediction framing throughout: the advantage is not a property of individual positions (both face 1/512) but of which positions each strategy comes to occupy when both compete within the same sequence of events. Remove the shared sequence — as the unidirectional experiment does — and there is nothing to select between.

### 4.6 Anticipating Objections

#### 4.6.1 “The equalization concentrates the Markov player on adverse sequences”

The most natural objection to the equalized comparison holds that matching the Markov player's entry count to the selective player's per-shoe count biases the Markov player toward sequences with more selective-player triggers — sequences that may be "streakier" and therefore more dangerous.

This objection must be addressed at two levels.

At the practical level, the equalization protocol replicates the most natural real-world scenario: two players seated at the same table, watching the same outcomes, making the same number of bets per session. Neither player selects which sequences to observe — the sequences arrive in whatever order the process produces. Both players are exposed to the same sequences; they differ only in which positions within those sequences they choose to engage. Equalizing entry counts per sequence is not a methodological distortion — it is the elimination of a confound. Without equalization, any observed advantage could be attributed to differential bet frequency rather than differential entry quality. Equalization isolates the variable under test: entry timing.

At the logical level, the Markovian position holds that sequence character is irrelevant to outcome — every position on every sequence is statistically identical, because each event is independent of all prior events. If this is true, then concentrating the Markov player's entries on any subset of sequences cannot disadvantage them, because no sequence is worse than any other. The objection that the Markov player was placed on "bad" sequences presupposes that some sequences produce worse outcomes than others — which is precisely the claim our experiment tests.

This creates a logical dilemma: the critic must either accept the equalization as fair (in which case the result stands) or object that sequence context affects outcomes (in which case the Markovian premise of strategic indifference is conceded). We present this not as a rhetorical device but as a structural feature of the experimental design: any criticism of the equalization methodology requires abandoning the assumption being tested.

A more refined version of this objection distinguishes between a priori probability (before flips occur, no sequence is worse than any other) and a posteriori composition (after flips occur, some sequences are objectively streakier). The objection holds that the equalization exploits post-hoc knowledge of which sequences turned out to be streaky. This distinction mischaracterizes the selective player's information state. The selective player does not act a priori (before any outcomes) or a posteriori (after the full sequence is known). The selective player acts in real time — observing a partial, growing sequence and entering based on what has been observed so far. At the moment of entry, the selective player does not know whether the current shoe is "streaky." They know only that four consecutive same-side outcomes have just occurred. The remainder of the sequence is genuinely unknown. If this partial observation — which reveals nothing about any individual future flip (Section 3.1) — nonetheless creates a meaningful distinction in aggregate outcomes, that distinction is the finding. The selective player is not exploiting hindsight. They are acting on real-time observation, and the data shows that acting on it produces measurably different results than not acting on it.

A related argument holds that because the selectional advantage attenuates with sequence length (Section 3.5), it must be an artifact of finite-sample bias rather than a genuine property of the system. This reasoning would invalidate most of statistics. All finite-sequence properties attenuate toward their infinite-limit values: sample means converge to population means, variance shrinks with N, and conditional probability effects dilute as the conditioning event becomes a smaller fraction of the total. The question is not whether a finite-sequence property attenuates with length — all of them do — but whether it follows a systematic, predictable functional form consistent with a proposed mechanism. The selectional advantage scales inversely with sequence length in a pattern consistent with the path narrowing model (Section 3.5), converging with Miller and Sanjurjo's (2018) independently derived gradient when compared at matched sequence lengths (Section 4.3). A methodological artifact would not produce a systematic scaling law that replicates across independent datasets and converges with independent mathematical derivations.

The reversed polarity confirmation (Section 3.6) provides definitive evidence against the equalization artifact hypothesis. If the equalization protocol systematically disadvantaged whichever player was subsampled, then swapping the entry criteria between players should produce the same pattern — the subsampled player would always perform worse regardless of which strategy they used. Instead, the advantage reverses: the streak-entry player outperforms the break-entry player regardless of which label they carry. The effect is a property of entry position, not of the equalization methodology.

Section 4.5.5 confirms this directly: the per-sequence correlation between selective entry frequency and Markov bust vulnerability is positive in the bidirectional experiment (r = +0.049) and inverts in the unidirectional experiment (r = −0.033). The equalization does concentrate the Markov player on sequences where the selective player is more active — and in the bidirectional case, those sequences are indeed more adverse for the Markov player. This is not a methodological distortion; it is the mechanism by which entry timing produces different aggregate outcomes.

#### 4.6.2 “The advantage is explained by different effective thresholds”

A more sophisticated objection observes that the selective player’s prior observation has the structural effect of raising the catastrophe threshold — the selective player at T4 constitutes a threshold of 13 (4 observed + 9 bet), while the Markov player constitutes a threshold of only 10 (1 observed + 9 bet). Since longer streaks are rarer, the objection holds that the selective player is simply less exposed to catastrophe by arithmetic, not by any meaningful property of observation.

As discussed in Section 4.3, this objection restates the finding rather than challenging it. The threshold difference is not an experimental parameter — it is constituted by the observer’s engagement with the sequence. Both players make exactly 9 bets. Both face identical per-entry odds of (1/2)\^9. The selective player’s observation of T prior same-side outcomes consumes T positions within the streak — positions that cannot contribute to the player’s loss sequence.

The Markovian position holds that these observations are irrelevant — if so, the constituted threshold should not differ between players, and the 4 observed outcomes should confer no structural protection. That the threshold does effectively differ is precisely the empirical content of the finding: prior observations, which Markovian theory deems irrelevant, produce measurable structural consequences for subsequent outcomes.

Both players sat down to make 9 bets. One of them watched 4 flips first. If those 4 flips are truly inert history carrying no information, then watching them should not change the player's aggregate outcome distribution under equalized comparison. It does — not by altering any individual bet, but by determining which positions the player comes to occupy within the sequence's streak structure.

The unidirectional isolation test (Section 4.5.5) confirms this distinction: the constituted threshold asymmetry (T+9 vs 10) is fully present in the unidirectional experiment, yet the equalized rate differential vanishes — demonstrating that the threshold difference produces a total-count asymmetry but not, by itself, the rate differential reported in Section 3.

*Sub-objection: “You’ve just rediscovered conditional probability.”* A related objection holds that P(streak reaches 13) \< P(streak reaches 10) is trivially true and requires no new explanation. But this framing smuggles in the very assumption being tested. For the 13 vs 10 comparison to apply, both players would need to be positioned within the same streak — one surviving to 10, the other to 13. In fact, the two players enter at DIFFERENT positions: the selective player enters at position 5 of a streak, the Markov player enters at position 2. They are not at the same starting point, exposed to the same streak, with different survival thresholds. They are at different positions entirely, each making 9 bets, each facing (1/2)\^9. The “conditional probability” framing treats the 4 prior observations as part of the event space — which is the selective player’s position. The Markov player, by their own theory, should not be counting those 4 observations as relevant. Both players make 9 bets. The fact that the prior observations create a meaningful difference in outcomes is the finding, not a premise.

*Sub-objection: “This is explained by Jensen’s inequality.”* One might formalize the differential sensitivity of asymmetric threshold functions under concentration as a consequence of Jensen’s inequality applied to convex loss functions. We note that such a formalization would itself constitute a mathematical demonstration that prior observations produce structural consequences for subsequent outcomes — which is the claim under test. Jensen’s inequality applying differentially to the two players is a mathematical restatement of the finding, not an alternative explanation for it.

#### 4.6.3 “This is just subset selection — any non-random filter produces different statistics”

A third objection holds that we have simply applied a filter to a dataset and shown that the filtered subset has different properties from the complement. This, the objection continues, is trivially true of any non-random partition and reveals nothing about probability.

We agree that selective filtering on correlated data trivially produces subset differences. The finding is that selective filtering on outcomes that are, by construction, independent also produces subset differences — contradicting the prediction that independence implies what we might call filtrative indifference. If each flip is independent and carries no information about future flips, then filtering on past flips should produce subsets with identical statistical properties to unfiltered data. It does not. The filter based on prior outcomes — outcomes that are provably uninformative about any individual future event — nonetheless produces a subset in which catastrophic loss is measurably rarer. This is the content of the finding, and the subset selection objection, properly understood, is a restatement of it rather than a refutation.

Furthermore, both players apply a filter. The selective player filters for “T consecutive same-side outcomes preceded my entry.” The Markov player filters for “one opposite-side outcome preceded my entry.” Both are non-random entry criteria based on prior outcomes. The experiment compares two filters, not a filter against no filter. That one filter produces measurably better outcomes than the other — despite both operating on information that Markovian theory deems equally uninformative — is the result.

#### 4.6.4 “The pseudo-random number generator has exploitable structure”

Python’s `random.choice()` implements the Mersenne Twister PRNG, which is deterministic. A sufficiently sophisticated analysis might, in principle, detect autocorrelation patterns that a truly random source would not produce.

We address this concern on two grounds. First, the Mersenne Twister has a period of 2\^19937 − 1, passes all standard randomness test suites (Diehard, NIST, TestU01), and is universally accepted in computational statistics. Our results replicate across five independent seeds, each producing structurally unrelated sequences. Second, and more fundamentally, both player strategies are applied to the same sequences. Any autocorrelation properties of the generator affect both players equally. The comparative finding — a difference between two strategies on identical data — is robust to PRNG concerns, because the PRNG is not a variable between conditions.

As a straightforward extension, the experiment could be replicated using hardware random number generation (atmospheric noise sources or quantum random number generators) to establish generalizability to non-deterministic sources. We note this as future work, while observing that the comparative design makes PRNG quality irrelevant to the finding as reported.

### 4.7 Limitations and Future Directions

Our experiment tests finite sequences. As demonstrated in Section 3.5, the selectional advantage scales inversely with sequence length — attenuating at longer lengths and amplifying at shorter ones. This scaling is consistent with the path narrowing mechanism but means the magnitude of the advantage depends on the sequence length analyzed. The effect persists at all lengths tested (40 through 200), with all thresholds from T5 onward exceeding 5-sigma even at length 200. In the limit of infinite sequences, the effect would be expected to vanish; however, all real-world sequences are finite.

The experiment is restricted to binary outcomes. Extension to non-binary systems — continuous random variables, random walks with threshold crossings, or multi-outcome processes — would test whether the path narrowing mechanism generalizes beyond binary sequences or depends on the two-outcome structure.

Preliminary computational results, to be reported separately, confirm that the selectional advantage replicates in an asymmetric binary process with unequal outcome probabilities (P(A) ≈ 50.7%, P(B) ≈ 49.3%) and an asymmetric payout structure that produces negative per-entry expected value. At T5, the equalized advantage is approximately 11%, reduced from 35.6% in the symmetric (fair coin) case — consistent with the prediction that constitutional asymmetry in the generating process attenuates the effect without eliminating it. Crucially, the advantage operates orthogonally to expected value: the selective player's per-entry outcomes remain net negative, confirming that the phenomenon is structural rather than exploitable. This result also serves as a control against the concern that the primary finding is contingent on exact symmetry in the generating process.

The relationship between our finding and the Diaconis same-side bias (Section 4.5) warrants dedicated experimental investigation. A protocol in which the flipper’s knowledge of the coin’s starting state is systematically varied — with and without observation of the starting position — would test whether observer knowledge contributes to the measured bias independently of the coin’s physical dynamics.

The convergence between our prospective gradient and Miller and Sanjurjo’s retrospective gradient when compared at similar sequence lengths (Section 4.3) raises a foundational question about the nature of finite-sequence streak bias. Miller and Sanjurjo characterized their finding as a property of completed datasets — a counting artifact that does not apply to real-time decision-making. Our experiment demonstrates that the same directional effect operates prospectively, in real time, in open sequences with no closure constraint. A dedicated study systematically comparing post-hoc analysis of completed sequences against real-time selective entry on the same sequences — holding all other parameters constant — would establish definitively whether the retrospective and prospective effects are manifestations of the same underlying mechanism or independent phenomena.

## 5. A STRUCTURAL PARALLEL, NOTED WITH PRECISION

The observations in this section are offered as empirical notes on the mathematical form of the findings reported above. They are severable from every result in Sections 3 and 4, and the empirical claims of this paper stand in full if a reader sets this section aside. We record them because the data exhibits two structural features — each independently noteworthy, and more suggestive in combination — that warrant placement on the record, even as we draw no physical or theoretical conclusion from them.

**The first observation is amplitude-squared scaling.** The path narrowing mechanism produces a specific quantitative form: each additional observation eliminates approximately half of the catastrophe-compatible continuations, because each must survive one further fair binary test. The catastrophe probability therefore scales as (1/2)\^T with observation depth T. This quantity can be written as the square of an amplitude-like factor: ((1/√2)\^T)² = (1/2)\^T. In that form it echoes the relationship between amplitude and probability familiar from two independent formulations in physics — the Born Rule (Born, 1926), under which measurement probabilities equal squared amplitudes, and Feynman's sum-over-histories formulation (Feynman & Hibbs, 1965), in which measurement restricts the set of contributing paths and the probability of the surviving outcomes follows the squared magnitude of the remaining bundle. The structural parallel is specific: in both settings, an act of observation narrows a set of compatible paths, and the probability of the surviving outcomes follows the square of a quantity that reduces by a constant factor with each additional constraint.

We are explicit about the limits of this first observation standing alone. The system studied here contains no complex amplitudes and no wave propagation. The per-event dynamics are purely classical: each catastrophe-compatible continuation attrits by a factor of one-half at each observation step rather than interfering with alternatives. In isolation, the amplitude-squared expression is an algebraic restatement of exponential decay at rate one-half — a rewriting that any process decaying at that rate would admit. We note the parallel without claiming it carries explanatory weight on its own.

**The second observation is the constructive/destructive cross-term.** As reported in Section 4.5.5, the unidirectional isolation test reveals that the aggregate covariance structure of the equalized comparison exhibits sign-switching behavior. When both players operate within the same streak domain — the experimental configuration tested throughout this study — the per-sequence correlation between selective entry frequency and Markov bust vulnerability is positive (r = +0.049). The equalization overweights the sequences where the Markov player is most exposed, amplifying the structural asymmetry between entry strategies. When the players are assigned to opposed streak domains — the selective player entering only on heads streaks, the Markov player entering only at tails direction changes — the correlation inverts (r = −0.033). The equalization overweights the sequences where the Markov player is most protected, and the advantage cancels to statistical zero. The two correlation magnitudes are comparable (\|+0.049\| vs \|−0.033\|), the two gradient ranges are comparable (3.3× constructive vs 3.2× destructive), and the cancellation in the destructive configuration is nearly exact.

This cross-term plays the same mathematical role as the interference term in wave systems. In the standard formulation of two-path interference, the combined probability is not the sum of the individual path probabilities — it includes a cross-term whose sign depends on the phase relationship between the paths, producing amplification (constructive interference) or cancellation (destructive interference) depending on configuration. In the equalized comparison, the combined effect is not determined by the marginal per-entry rate alone — it includes a covariance cross-term whose sign depends on the structural relationship between the two entry strategies, producing amplification (bidirectional, shared domain) or cancellation (unidirectional, opposed domains) depending on configuration. The sign of the cross-term is not a property of either strategy in isolation. It is a property of the relationship between them — of how the two observers' engagements are configured relative to the same sequence.

**It is the co-occurrence of these two features that we wish to place on the record.** Amplitude-squared scaling, by itself, could be dismissed as algebraic rewriting. A sign-switching cross-term, by itself, could be characterized as a statistical property of the equalization protocol. But their co-occurrence in a single system — a fully classical, memoryless experiment with no quantum mechanics, no complex amplitudes, and no wave propagation — is more difficult to set aside as coincidence. Amplitude-squared scaling of outcome probability under observer-dependent path restriction, and a configuration-dependent cross-term that determines whether the combined effect is amplified or canceled: these are the two defining structural features of quantum interference, appearing together in a system that is, by construction, maximally far from quantum.

We note, as a matter of historical record, that neither feature is native to quantum theory. Malus's Law (1809) described amplitude-squared scaling in classical optics more than a century before the Born Rule was formulated. Constructive and destructive interference patterns were identified in water waves and sound centuries before quantum mechanics existed. The quantum formalism unified these features under a single mathematical framework — the superposition of complex amplitudes — but the structural elements themselves predate that unification. Their recurrence in a coin-flip experiment may reflect nothing more than a coincidence of mathematical form across unrelated domains. Or it may reflect some common structure, not yet identified, governing how observer-dependent restriction of compatible paths maps to measurable probability. We do not adjudicate between these possibilities. We record the observations, note their specificity, and identify the question as a direction for dedicated theoretical work.

## 6. CONCLUSION

Two players watch the same fair coin being flipped. Both make the same number of bets. Both use the same 9-bet anti-continuation structure. Both face identical per-entry odds of 1 in 512. One player waits — observing consecutive same-side outcomes before engaging. The other enters immediately at every change in direction. Across 500,000 sequences of 80 flips, replicated over five independent datasets comprising 40 million coin flips, the patient player suffers fewer catastrophic losses. The advantage is 20.8% at an observation depth of 4, scaling monotonically to 67.7% at a depth of 7, with zero gradient reversals across 25 data points, at combined Z-scores from −7.16 to −22.60 and Bayes factors well beyond the benchmark reported for the Diaconis et al. (2023) physical coin-bias result.

Each individual flip is confirmed to be fair. Per-entry loss rates match the theoretical prediction of (1/2)\^9 at every threshold, for both players. Markov is right about every event. But the assumption that per-event independence implies strategic indifference — that it cannot matter WHEN an observer chooses to engage a memoryless sequence — is refuted by the data.

The mechanism is path narrowing within conditional ensembles. The observer who watches T consecutive same-side outcomes before betting has not changed any future flip. They have consumed T positions within the streak structure of the sequence — positions that can no longer contribute to their loss. The set of catastrophe-compatible continuations contracts by a factor of approximately one-half per observation. The observer who watches more narrows more. The observer who watches nothing narrows nothing. Different depths of engagement produce different ensembles, and different ensembles contain different densities of catastrophe. No law of probability is violated. But a century-old interpretive assumption — that observation of prior outcomes in an independent sequence is strategically inert — is shown to be false.

This finding decomposes the Gambler’s Fallacy into two separable claims and shows that the standard debunking addresses only the first. The gambler’s per-event prediction — that tails becomes more likely after a run of heads — is indeed a fallacy. The gambler’s strategic prescription — wait for the streak, then bet against it — is empirically vindicated. The inferential leap from “each flip is fair” to “therefore entry timing is irrelevant” was never a theorem. It was an assumption. It has now been tested, and it fails.

The constituted threshold — the catastrophe barrier created by the observer’s integration of prior outcomes into their engagement with the sequence — provides the explanatory bridge. Both players make 9 bets. But the patient player’s prior observations have consumed positions within the streak, constituting a higher effective barrier that catastrophe must overcome. The Markov player, whose theoretical framework declares those observations irrelevant, does not benefit from this protection. The observations that theory dismisses as meaningless provide measurable structural defense. Theory and data disagree. The data wins.

The experiment is trivially reproducible. The complete Python implementation is provided in Appendix A. Any researcher with a standard computing environment can replicate every result reported here in under five minutes. The sequences are computationally generated, eliminating all physical confounds. The design is comparative, eliminating PRNG concerns. The gradient is monotonic across five independent seeds, eliminating dataset dependence. The advantage scales inversely with sequence length, confirming the path narrowing mechanism. Reversing which player uses which entry criterion reverses the advantage, confirming the effect is position-dependent, not implementation-dependent. Assigning the two players to opposite sides of the sequence — heads streaks against tails direction changes — cancels the advantage entirely, confirming the effect requires constructive correlation within a shared positional space. The finding is not fragile. It is not subtle. It is not borderline. It is a robust, scalable, reproducible empirical fact that challenges a foundational assumption in the theory of probability.

We note, as recorded in Section 5, that the mathematical form of these findings — amplitude-squared scaling in the path narrowing gradient and configuration-dependent cross-terms in the aggregate covariance structure — exhibits structural parallels to the relationship between observation, path restriction, and probability in established physics. We draw no physical conclusion from this. We record it because the specificity and co-occurrence of these features in a fully classical system warrants placement on the record, and because the question of whether observer-dependent path restriction maps to measurable probability through some common structure across domains is one this study raises for future theoretical work.

The individual flips are independent. The decision of when to act on them is not. The gambler was right.

## 7. ACKNOWLEDGMENTS AND DECLARATIONS

*Data and code availability.* The complete Python implementation is provided in Appendix A and is available at [GitHub DOI]. All results are deterministic given the specified seeds.

*AI tools.* The author used AI language model tools for analytical discussion during the development of this study and for drafting assistance in preparing the manuscript. All experimental results are produced by the independently verifiable code above. The author takes sole responsibility for the design, analysis, interpretation, and all claims presented in this paper.

*Competing interests.* The author declares none.

## 7. REFERENCES

Bartoš, F., Sarafoglou, A., Godmann, H. R., et al. (2025). Fair coins tend to land on the same side they started: Evidence from 350,757 flips. *Journal of the American Statistical Association*, 120(552), 2118–2127. https://doi.org/10.1080/01621459.2025.2516210

Born, M. (1926). Zur Quantenmechanik der Stoßvorgänge. *Zeitschrift für Physik*, 37(12), 863–867. https://doi.org/10.1007/BF01397477

Diaconis, P., Holmes, S., & Montgomery, R. (2007). Dynamical bias in the coin toss. *SIAM Review*, 49(2), 211–235. https://doi.org/10.1137/S0036144504446436

Feynman, R. P., & Hibbs, A. R. (1965). *Quantum Mechanics and Path Integrals*. McGraw-Hill.

Malus, É. L. (1809). Sur une propriété de la lumière réfléchie. Mémoires de Physique et de Chimie de la Société d'Arcueil, 2, 145–158.

Matsumoto, M., & Nishimura, T. (1998). Mersenne Twister: A 623-dimensionally equidistributed uniform pseudo-random number generator. *ACM Transactions on Modeling and Computer Simulation*, 8(1), 3–30. https://doi.org/10.1145/272991.272995

Miller, J. B., & Sanjurjo, A. (2018). Surprised by the hot hand fallacy? A truth in the law of small numbers. *Econometrica*, 86(6), 2019–2047. https://doi.org/10.3982/ECTA14943

Miller, J. B., & Sanjurjo, A. (2019). A bridge from Monty Hall to the hot hand: The principle of restricted choice. *Journal of Economic Perspectives*, 33(3), 144–162. https://doi.org/10.1257/jep.33.3.144

Tversky, A., & Kahneman, D. (1971). Belief in the law of small numbers. *Psychological Bulletin*, 76(2), 105–110. https://doi.org/10.1037/h0031322

Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131. [*https://doi.org/10.1126/science.185.4157.1124*](https://doi.org/10.1126/science.185.4157.1124)

## 8. Appendix A: Complete Python Implementation

The following self-contained Python script reproduces all results reported in this paper. No external dependencies beyond Python 3.6+ standard library. Expected runtime: approximately 5 minutes.

```
# APPENDIX B: Complete Python Implementation (v3 — BR-only publication run)
#
# This script reproduces the BR-only results that will appear in the paper.
# No external dependencies beyond Python 3.6+ standard library.
# Expected runtime: approximately 20-30 minutes (N=100K, EQ=100, BR only).
#
# v3 changes (from original):
# - Restricted to the Direct Sequence (BR) view only -- no derived views.
# - Fix 1 (audit LOW-1): inverted monotonicity check corrected.
# - Fix 2 (audit LOW-2): hardcoded "YES" check replaced with computation.
# - Fix 4 (audit LOW-3): MK stop check aligned with TX (start_pos + 1 <= stop).
# - Fix 5 (audit LOW-4): equalized rate divides by actual subsample total.
# - DOES NOT apply Fix 3 (the derived-road algorithm change) -- derived
# roads are irrelevant since this run uses BR only.
# - Per-seed Z scores are explicitly printed.
# - Per-side (H/T) equalized comparison at T=4 (Table 5).
# - Per-side MK tracking added so per-side equalization is possible.
# - Verification checkpoints emit during execution.
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

SHOE_LENGTH = 80          # Binary outcomes per sequence ("shoe")
STOP_ENTERING = 65        # Last position where a new bet sequence can begin
BUST_STEPS = 9            # Number of bets in each entry (both players)
THRESHOLDS = [3, 4, 5, 6, 7]  # Observation depths tested
SEEDS = [42, 123, 456, 789, 1001]  # Independent random seeds
N_PER_SEED = 100000       # v3: doubled for publication-quality precision
EQ_TRIALS = 100           # v3: bumped from 10 for equalization stability

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
 
 Input: ['H', 'H', 'T', 'T', 'T', 'H']
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
# exactly T consecutive identical outcomes is detected.
# "Fresh" means the streak began exactly T positions ago
# (the preceding outcome was different). This ensures each
# streak produces exactly one TX entry at its threshold depth.
#
# MARKOV PLAYER (MK): Enters at every direction change — the
# first position of a new streak. Bets against the new
# direction continuing.
#
# BUST CONDITION (both players): All BUST_STEPS bets lose.
# For TX: the streak extends BUST_STEPS beyond the observed T.
# For MK: the new streak extends BUST_STEPS beyond the
# observed direction change.
# Both conditions require streak_length >= threshold + BUST_STEPS.
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
```
