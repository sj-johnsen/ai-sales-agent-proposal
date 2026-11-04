"""Power calculation for the final report (Table A1, A2).

Two-sided test of two proportions, normal approximation with unpooled variance,
alpha = 0.05, power = 0.80. Control rate p0 from Finto: 2-3 meetings per 100 firms.
Human capacity: about 100 accounts per BDA and week. Each participating firm contributes one BDA,
so the number of firms sets the size of the human arm.
"""
import random
from math import sqrt
from statistics import NormalDist

Z = NormalDist().inv_cdf
ZA, ZB = Z(0.975), Z(0.80)


def n_control(p0, p1, k=1.0):
    """Accounts needed in the control arm when the agent arm has k times as many."""
    return (ZA + ZB) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1) / k) / (p1 - p0) ** 2


def mde(p0, n_c, n_t):
    """Smallest p1 > p0 detectable with n_c control and n_t treated accounts."""
    lo, hi = p0, 0.5
    for _ in range(100):
        mid = (lo + hi) / 2
        se = sqrt(p0 * (1 - p0) / n_c + mid * (1 - mid) / n_t)
        lo, hi = (lo, mid) if (mid - p0) / se > ZA + ZB else (mid, hi)
    return hi


def mde_down(p0, n_c, n_t):
    """Largest p1 < p0 detectable (a drop in the meeting rate)."""
    lo, hi = 0.0, p0
    for _ in range(100):
        mid = (lo + hi) / 2
        se = sqrt(p0 * (1 - p0) / n_c + mid * (1 - mid) / n_t)
        lo, hi = (mid, hi) if (p0 - mid) / se > ZA + ZB else (lo, mid)
    return lo


def simulate(n_c, n_t, p0, p1, draws=4000, seed=1):
    """Share of draws in which a two-sided z-test (unpooled) rejects at 5 %."""
    rng = random.Random(seed)
    hits = 0
    for _ in range(draws):
        a = sum(rng.random() < p0 for _ in range(n_c)) / n_c
        b = sum(rng.random() < p1 for _ in range(n_t)) / n_t
        se = sqrt(a * (1 - a) / n_c + b * (1 - b) / n_t)
        hits += se > 0 and abs(b - a) / se > Z(0.975)
    return hits / draws


PER_WEEK, WEEKS, RATIO = 100, 12, 3      # accounts per BDA and week, weekly batches, agent : BDA
FIRMS = 4                                # main design: Finto plus three start-ups, one BDA each


def design(firms, p0=0.025, weeks=WEEKS, ratio=RATIO, per_week=PER_WEEK):
    """Human and agent accounts, MDE up and down, for `firms` firms with one BDA each."""
    n_c = per_week * weeks * firms
    n_t = ratio * n_c
    return n_c, n_t, mde(p0, n_c, n_t), mde_down(p0, n_c, n_t)


if __name__ == "__main__":
    print("Table A1: accounts per arm for a 1:1 design")
    print("| p0 | +25 % | +50 % | +100 % |")
    for p0 in (0.020, 0.025, 0.030):
        cells = [f"{n_control(p0, p0 * (1 + r)):,.0f}" for r in (0.25, 0.5, 1.0)]
        print(f"| {p0:.1%} | " + " | ".join(cells) + " |")
    print(f"\nTable A2: MDE by number of firms (one BDA each, {WEEKS} weeks, 1:{RATIO})")
    print("| firms | human accounts | agent accounts | p0 = 2.0 % | p0 = 2.5 % | p0 = 3.0 % |")
    for f in (1, 2, 3, 4, 6, 8):
        n_c, n_t, _, _ = design(f)
        cells = []
        for p0 in (0.020, 0.025, 0.030):
            up, down = design(f, p0)[2:]
            cells.append(f"+{up/p0-1:.0%} / {down/p0-1:.0%}")
        print(f"| {f} | {n_c:,} | {n_t:,} | " + " | ".join(cells) + " |")
    print(f"\nTable A3: MDE by BDA pace ({FIRMS} firms, {WEEKS} weeks, 1:{RATIO}, p0 = 2.5 %)")
    print("| new accounts per BDA and week | human accounts | agent accounts | MDE |")
    for pw in (50, 75, 100, 150, 200):
        n_c, n_t, up, down = design(FIRMS, per_week=pw)
        print(f"| {pw} | {n_c:,} | {n_t:,} | +{up/0.025-1:.0%} / {down/0.025-1:.0%} |")
    n_c, n_t, up, down = design(FIRMS)
    print(f"\nMain design ({FIRMS} firms): {n_c:,} human and {n_t:,} agent accounts, "
          f"detects {up:.2%} (+{up/0.025-1:.0%}) or {down:.2%} ({down/0.025-1:.0%})")
    print("Old design (2 BDAs at one firm):", f"{mde(0.025, 2400, 7200):.2%}", f"{mde_down(0.025, 2400, 7200):.2%}")
    print("Check by simulation, main design at the upward MDE:", simulate(n_c, n_t, 0.025, up, draws=2000))
