"""Monte Carlo check of the multi-firm design (appendix, Table B1).

The simulation produces no results about agents and BDAs. It checks that the planned estimators
keep their size, reach the power the analytical calculation promises, and cover the true effect.

Design: FIRMS firms, one BDA each, WEEKS weekly batches of 400 accounts per firm, assigned 1:3 to
agent and BDA within firm x week. Meeting probabilities follow a logit with firm-specific baselines
around p0 = 2.5 % and pre-assignment covariates. The agent multiplies each account's baseline
probability by (1 + r_f); r_f varies across firms in the heterogeneous scenarios.

Two estimands, two estimators:
  SATE  the average effect on the accounts of the participating firms.
        Lin (2013): Y on A, centred covariates and their interactions with A, firm x week fixed
        effects, robust (HC1) standard errors.
  PATE  the average effect across the population of firms the participants are drawn from.
        One Lin estimate per firm, averaged; t-test on the F firm estimates with F - 1 degrees of
        freedom (Ibragimov & Mueller, 2010).
The true SATE is computed from the simulated probabilities of each sample, the true PATE from a
large draw of firms, so coverage is measured against the estimand each estimator targets.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

from power import FIRMS, PER_WEEK, RATIO, WEEKS, design

HERE = Path(__file__).parent
P0 = 0.025
SD_FIRM_BASE = 0.30          # sd of firm baselines on the logit scale
REPS = 1000
SEED = 20261102

# account covariates: lead source (inbound / event / scraped), C-level contact, log employees
COV_SHIFT = {"inbound": 0.35, "event": 0.15, "clevel": -0.15, "logemp": -0.08}


def draw_firm_intercepts(rng, n):
    return rng.normal(0.0, SD_FIRM_BASE, n)


def baseline_probs(rng, firm_icpt, n_per_firm, intercept):
    """Covariates and baseline meeting probabilities for every account of every firm."""
    F = len(firm_icpt)
    n = F * n_per_firm
    src = rng.choice(3, n, p=[0.25, 0.25, 0.50])                 # 0 inbound, 1 event, 2 scraped
    clevel = rng.random(n) < 0.30
    logemp = rng.normal(0.0, 1.1, n)
    X = np.column_stack([src == 0, src == 1, clevel, logemp]).astype(float)
    eta = (intercept + np.repeat(firm_icpt, n_per_firm)
           + COV_SHIFT["inbound"] * X[:, 0] + COV_SHIFT["event"] * X[:, 1]
           + COV_SHIFT["clevel"] * X[:, 2] + COV_SHIFT["logemp"] * X[:, 3])
    return X, 1 / (1 + np.exp(-eta))


def calibrate_intercept(rng):
    """Logit intercept that makes the population mean baseline probability equal P0."""
    icpt = draw_firm_intercepts(rng, 2000)
    lo, hi = -6.0, -2.0
    for _ in range(60):
        mid = (lo + hi) / 2
        _, p = baseline_probs(np.random.default_rng(1), icpt, 200, mid)
        lo, hi = (mid, hi) if p.mean() < P0 else (lo, mid)
    return (lo + hi) / 2


def demean(M, groups, n_groups):
    sums = np.zeros((n_groups,) + M.shape[1:])
    np.add.at(sums, groups, M)
    counts = np.bincount(groups, minlength=n_groups).reshape((-1,) + (1,) * (M.ndim - 1))
    return M - (sums / counts)[groups]


def lin(y, A, X, groups, n_groups):
    """Lin (2013) estimate of the effect of A with group fixed effects; returns (tau, HC1 se)."""
    Xc = X - X.mean(0)
    Z = np.column_stack([A, Xc, A[:, None] * Xc])
    Zd, yd = demean(Z, groups, n_groups), demean(y, groups, n_groups)
    ZtZ_inv = np.linalg.inv(Zd.T @ Zd)
    b = ZtZ_inv @ Zd.T @ yd
    e = yd - Zd @ b
    n, k = len(y), Z.shape[1] + n_groups
    meat = (Zd * e[:, None] ** 2).T @ Zd
    V = ZtZ_inv @ meat @ ZtZ_inv * n / (n - k)
    return b[0], np.sqrt(V[0, 0])


def one_sample(rng, intercept, r_mean, r_sd, F=FIRMS):
    n_f = PER_WEEK * (1 + RATIO) * WEEKS                         # accounts per firm
    firm_icpt = draw_firm_intercepts(rng, F)
    X, p0 = baseline_probs(rng, firm_icpt, n_f, intercept)
    r_f = r_mean + r_sd * rng.standard_normal(F)
    p1 = np.clip(p0 * (1 + np.repeat(r_f, n_f)), 0, 1)
    firm = np.repeat(np.arange(F), n_f)
    week = np.tile(np.repeat(np.arange(WEEKS), PER_WEEK * (1 + RATIO)), F)
    cell = firm * WEEKS + week
    A = np.zeros(len(p0))                                        # 1:3 within every firm x week cell
    for c in range(F * WEEKS):
        idx = np.flatnonzero(cell == c)
        A[rng.choice(idx, PER_WEEK * RATIO, replace=False)] = 1
    y = (rng.random(len(p0)) < np.where(A == 1, p1, p0)).astype(float)
    sate = (p1 - p0).mean()

    tau, se = lin(y, A, X, cell, F * WEEKS)
    firm_tau = np.array([lin(y[firm == f], A[firm == f], X[firm == f], week[firm == f], WEEKS)[0]
                         for f in range(F)])
    return sate, tau, se, firm_tau


def scenario(name, r_mean, r_sd, intercept, pate, rng):
    crit_z, crit_t = stats.norm.ppf(0.975), stats.t.ppf(0.975, FIRMS - 1)
    rej_s = rej_p = cov_s = cov_p = 0
    taus, sates = [], []
    for _ in range(REPS):
        sate, tau, se, ft = one_sample(rng, intercept, r_mean, r_sd)
        m, s = ft.mean(), ft.std(ddof=1) / np.sqrt(FIRMS)
        rej_s += abs(tau / se) > crit_z
        rej_p += abs(m / s) > crit_t
        cov_s += abs(tau - sate) <= crit_z * se
        cov_p += abs(m - pate) <= crit_t * s
        taus.append(tau)
        sates.append(sate)
    taus, sates = np.array(taus), np.array(sates)
    return {
        "scenario": name, "r_mean": r_mean, "r_sd": r_sd, "true_pate": pate,
        "mean_true_sate": float(sates.mean()), "mean_tau_hat": float(taus.mean()),
        "bias_vs_sate": float((taus - sates).mean()),
        "reject_sate_test": rej_s / REPS, "reject_pate_test": rej_p / REPS,
        "coverage_sate_ci": cov_s / REPS, "coverage_pate_ci": cov_p / REPS,
    }


def main():
    rng = np.random.default_rng(SEED)
    intercept = calibrate_intercept(rng)
    _, p_pop = baseline_probs(np.random.default_rng(2), draw_firm_intercepts(np.random.default_rng(3), 4000), 200, intercept)
    mean_p0 = float(p_pop.mean())
    n_c, n_t, up, down = design(FIRMS)
    r_mde = up / P0 - 1                                          # relative MDE of the analytical calculation
    rows = []
    for name, r_mean, r_sd in [
        ("no effect, homogeneous", 0.0, 0.0),
        ("no average effect, heterogeneous", 0.0, 0.10),
        ("effect at the MDE, homogeneous", r_mde, 0.0),
        ("effect at the MDE, heterogeneous", r_mde, 0.10),
    ]:
        rows.append(scenario(name, r_mean, r_sd, intercept, r_mean * mean_p0, rng))
        print(rows[-1])
    out = {
        "design": {"firms": FIRMS, "weeks": WEEKS, "per_bda_week": PER_WEEK, "ratio": RATIO,
                   "human_accounts": n_c, "agent_accounts": n_t, "p0": P0,
                   "mde_up": up, "mde_down": down, "mde_up_rel": r_mde, "mde_down_rel": down / P0 - 1},
        "monte_carlo": {"replications": REPS, "seed": SEED, "sd_firm_baseline_logit": SD_FIRM_BASE,
                        "population_mean_p0": mean_p0, "scenarios": rows},
    }
    (HERE / "validation_results.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
