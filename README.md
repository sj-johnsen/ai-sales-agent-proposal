# Can an AI agent replace a sales rep who already uses AI?

Final report (research proposal), *Topics in Econometrics B* (Prof. Masayuki Sawada), Hitotsubashi University, Autumn 2026.
Author: Simon Jensen (student ID 2226237U).

This repository holds the code behind the power calculation and the Monte Carlo check of the proposal
[`2226237U_simon_jensen.pdf`](2226237U_simon_jensen.pdf). The proposal plans a field experiment at four B2B start-ups:
prospect accounts are randomized 1:3 between an autonomous, disclosed AI agent (e-mail only) and an AI-assisted
business development associate (BDA) who works as usual. The primary outcome is a booked meeting within 45 days of
the account's batch date.

**No experiment has been run.** The simulation contains no estimates of the agent's effect. It only checks that the
planned estimator keeps its size, covers the true effect and reaches the power the analytical calculation promises.

## Where to find what

| Proposal | File |
| :--- | :--- |
| Accounts needed per arm, 1:1 design (Table A1) | `power.py` |
| Detectable effect by number of start-ups (Table A2) and by BDA pace (Table A3) | `power.py` |
| Monte Carlo check, size, power and coverage (Table B1) | `simulate_and_estimate.py`, results in `validation_results.json` |
| Text of the proposal and the appendix | `text.md`, `appendix.md` |
| PDF layout | `build_pdf.py` |

## Main design numbers

Four start-ups, one BDA each, twelve weekly batches, 100 new accounts per BDA and week, 1:3 allocation, baseline
meeting rate 2.5%: 4,800 human and 14,400 agent accounts. The design detects a rise to 3.26% (+30%) or a fall to
1.80% (−28%) at 5% significance and 80% power. In 1,000 Monte Carlo replications the main estimator (Lin 2013
regression with start-up × week fixed effects and robust standard errors) rejects a true null in 6.2%, its 95%
intervals cover the true effect in 93 to 95%, and it detects +30% in 76 to 78%.

## Running it

```bash
# install uv once: https://docs.astral.sh/uv/
uv sync
uv run python power.py                    # Tables A1 to A3 (seconds)
uv run python simulate_and_estimate.py    # Table B1, writes validation_results.json (about one minute)
uv run --with pypdf python build_pdf.py   # rebuilds the PDF; needs tectonic
```

The simulation is seeded, so a second run gives the same `validation_results.json`.
