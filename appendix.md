# Appendix

The power calculation (Tables A1 to A3) and the simulation (Table B1) were run in Python; code and results are public (Jensen, 2026). The simulation contains no estimates of the agent's effect. It only checks that the planned estimator behaves as the power calculation promises, under independent accounts.

### A. Power calculation

Two-sided test of two proportions at $\alpha = 0.05$ and power $0.80$, normal approximation with unpooled variance. The regression of Section 5 can only be more precise, so the calculation is conservative. The control rate $p_0 = 2.5$% comes from Finto. With $n_0$ human and $n_1$ agent accounts, the smallest detectable rise $p_1 > p_0$ solves

$$\frac{p_1 - p_0}{\sqrt{p_0(1-p_0)/n_0 + p_1(1-p_1)/n_1}} = z_{0.975} + z_{0.80},$$

and the largest detectable fall is found the same way for $p_1 < p_0$.

**Table A1.** Accounts needed per arm in a 1:1 design.

| $p_0$ | +25% | +50% | +100% |
| :--- | ---: | ---: | ---: |
| 2.0% | 13,806 | 3,822 | 1,138 |
| 2.5% | 10,981 | 3,038 | 903 |
| 3.0% | 9,097 | 2,514 | 746 |

**Table A2.** Detectable rise / fall by number of start-ups (one BDA each, 100 accounts per week, 12 weeks, 1:3 allocation). The main design is the row with four start-ups.

| Start-ups | Human accounts | Agent accounts | $p_0 = 2.0$% | $p_0 = 2.5$% | $p_0 = 3.0$% |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1,200 | 3,600 | +71% / −60% | +63% / −54% | +57% / −50% |
| 2 | 2,400 | 7,200 | +49% / −44% | +43% / −39% | +39% / −36% |
| 3 | 3,600 | 10,800 | +40% / −36% | +35% / −32% | +32% / −30% |
| **4** | **4,800** | **14,400** | **+34% / −31%** | **+30% / −28%** | **+27% / −26%** |
| 6 | 7,200 | 21,600 | +28% / −26% | +25% / −23% | +22% / −21% |
| 8 | 9,600 | 28,800 | +24% / −22% | +21% / −20% | +19% / −18% |

**Table A3.** Detectable rise / fall by the BDAs' pace (four start-ups, 12 weeks, 1:3, $p_0 = 2.5$%). The pace is measured in the pilot and sets the size of the weekly batches; the design plans with 85 to 100 (bold).

| New accounts per BDA and week | Human accounts | Agent accounts | Detectable rise / fall |
| ---: | ---: | ---: | ---: |
| 50 | 2,400 | 7,200 | +43% / −39% |
| 75 | 3,600 | 10,800 | +35% / −32% |
| **85** | **4,080** | **12,240** | **+33% / −30%** |
| **100** | **4,800** | **14,400** | **+30% / −28%** |
| 150 | 7,200 | 21,600 | +25% / −23% |
| 200 | 9,600 | 28,800 | +21% / −20% |

Giving the agent more accounts helps less than it seems, because the variance of the smaller human arm dominates. At $p_0 = 2.5$%, raising the ratio from 1:3 to 1:5 (9,600 more agent accounts) lowers the detectable rise only from +30% to +28%; one more start-up (4,800 accounts) lowers it to +27%.

### B. Monte Carlo check of the design

Each replication draws four start-ups with baselines that differ on the logit scale (standard deviation 0.3, population mean of $p_0$ calibrated to 2.5%) and accounts with three covariates standing in for those of Section 3. Outcomes are independent across accounts given these baselines; week-level shocks, non-compliance and cost are not simulated. Assignment is 1:3 within start-up × week. The agent multiplies each account's baseline probability by $(1 + r_f)$; in the heterogeneous scenarios $r_f$ varies across start-ups with standard deviation 0.10. The true effect is computed from the simulated probabilities, so coverage is measured against the effect the estimator targets.

Two tests are checked. The **main test** is the Lin (2013) regression of Section 5 with stratum fixed effects and robust standard errors; its target is the effect on the participating start-ups. The **start-up test** averages one Lin estimate per start-up and uses a t-test with three degrees of freedom (Ibragimov & Müller, 2010); its target is the average effect across start-ups like these.

**Table B1.** Rejection rates and coverage of 95% intervals, 1,000 replications each.

| Scenario | Main test: rejects | Main test: coverage | Start-up test: rejects | Start-up test: coverage |
| :--- | ---: | ---: | ---: | ---: |
| No effect, same relative effect in every start-up | 6.2% | 93.8% | 4.5% | 95.5% |
| No average effect, varies across start-ups | 8.8% | 94.9% | 5.0% | 95.0% |
| Effect at the detectable size (+30%), same relative effect in every start-up | 77.9% | 93.4% | 41.7% | 95.6% |
| Effect at the detectable size, varies across start-ups | 76.2% | 94.8% | 34.3% | 95.5% |

Under no effect, the main test rejects in 6.2% and the start-up test in 4.5% of replications; with 1,000 replications the Monte Carlo standard error is about 0.7 points, so the main test is slightly liberal. In the second row, the main test rejects more often because the effect on the four participating start-ups is not exactly zero when effects vary across start-ups; its coverage of that effect stays at 95%. At the detectable effect, the main test comes close to the planned power (76 to 78% against 80%), while the start-up test, which answers a broader question with four units, reaches only 34 to 42%. The headline estimand is the effect on the participating start-ups because they are not a random sample (Section 5); the lower power of the start-up test is a second reason, not the first.

### C. Timeline and pre-specification

**Table C1.** Timeline of the experiment.

| Weeks | Phase | Content |
| :--- | :--- | :--- |
| before 1 | Warm-up | Agent and BDA mailboxes are warmed up on separate domains, capped at an assumed 40 cold e-mails a day each; at an assumed four e-mails per account, the agent's 300 new accounts a week need six mailboxes per start-up and the BDA's 100 need two. Authentication (SPF, DKIM, DMARC) is set up. |
| 1–2 | Pilot | Normal BDA pace at 1:3 in each start-up to test logging and deliverability and measure the BDA's pace, which then fixes the batch size, and see how much cost per account varies across weeks. Analysis code registered on the AEA RCT Registry before the main phase. Pilot data are not used in the main analysis. |
| 3–14 | Main experiment | 12 weekly batches per start-up, drawn and randomized by a researcher at the pace measured in the pilot (100 BDA and 300 agent accounts at the planned pace). Agent updates only between batches, logged. If a BDA leaves, that start-up's later weeks are dropped, so τ stays the effect for the BDAs who remain. |
| 15–18 | Outcome closure | 30-day booking windows of the last batch close; meetings held are verified. |
| 19–20 | Analysis | Pre-specified estimators of Section 5 and the start-up test of Appendix B. |
