#
# Bamafshe Marziyeh Bamdad + ChatGPT
# Sun Dec 28, 2025 03:27 CET
#

#!/usr/bin/env python3
"""
wilson_ci.py
Compute Wilson score confidence intervals for binomial proportions.

Usage examples:
  python wilson_ci.py --conf 0.95 \
    "Smartphone apps=28/42" "Wearables preferred=26/42" "No tech use=10/42"

  python wilson_ci.py --conf 0.95 --digits 1 --as-percent \
    "Satisfied=18/32" "Dissatisfied=6/32"

python wilson_ci.py --conf 0.95 --digits 1 --as-percent "Q6. Samartphone-based (66.67%)=28/42" "Q6. not use any (23.81%)=10/42" "Q8. satisfied (46.88%)=15/32" "Q8. dissatisfaction (15.63%)=5/32" "Q8. uncertainty (6.25%)=2/32" "Q11. finding routes=29/42" "Q11. locating objects in outdoor=24/42" "Q12. Head-level (76.19)=32/42" "Q12. ground- & chest-level (40.48%)=17/42" "Q7. using for outdoor or for both (93.75%)=30/32" "Q13. wearable (61.9%)=26/42" "Q13. handheld (28.57%)=12/42" "Q13. other (9.52%)=4/42" "Q14. speech (40.48%)=17/42" "Q14. Multimodal (30.95%)=13/42" "Q14. Tactile (19.05%)=8/42" "Q15. Hands & arms (57.14%)=24/42" "Q17. obstcle-free (61.9%)=26/42" "Q17. Route info. (54.76%)=23/42" "Q17. Constant assistance (47.62%)=20/42" "Q17. hortest-distance & rapid re-routing (38.10%)=16/42" "Q16. ease of use (80.95%)=34/42" "Q16. low cost (66.67%)=28/42" "Q16. mental load & device weight (52.38%)=22/42" "Q16. physical effort & avoidance of obstacles (47.62%)=20/42" "Q9. sufficient feedback (18.75%)=6/32" "Q9. insufficient feedback - obstacles (31.25%)=10/32" "Q9. insufficient feedback outdoor (25.00%)=8/32" "Q9. insufficient feedback - intdoor (12.50%)=4/32" "Q10. always or most of the time (40.63%)=13/32" "Q10. sometimes (37.5%)=12/32" "Q10. rarely or never (18.75%)=6/32" "Q10. unsure (3.13%)=1/32" 

Notes:
- Wilson interval is recommended for small samples and proportions near 0/1.
- For 95% CI, z ≈ 1.959963984540054 (normal quantile).

 Note (personal check): Results were spot-checked against
 https://www.statskingdom.com/proportion-confidence-interval-calculator.html
 using the Wilson score method to ensure consistency.

"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Result:
    label: str
    k: int
    n: int


def normal_quantile(p: float) -> float:
    """
    Inverse CDF (quantile) for standard normal distribution.
    Uses math.erfcinv if available; otherwise uses a rational approximation.

    This implementation avoids external dependencies.
    """
    # Use an accurate rational approximation (Peter J. Acklam) for inverse normal CDF.
    # Reference: https://web.archive.org/web/20150910044729/http://home.online.no/~pjacklam/notes/invnorm/
    if not (0.0 < p < 1.0):
        raise ValueError("p must be in (0, 1)")

    # Coefficients in rational approximations
    a = [
        -3.969683028665376e+01,
        2.209460984245205e+02,
        -2.759285104469687e+02,
        1.383577518672690e+02,
        -3.066479806614716e+01,
        2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01,
        1.615858368580409e+02,
        -1.556989798598866e+02,
        6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
        4.374664141464968e+00,
        2.938163982698783e+00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e+00,
        3.754408661907416e+00,
    ]

    # Define break-points
    plow = 0.02425
    phigh = 1 - plow

    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        num = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
        den = ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        return num / den
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        num = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5])
        den = ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
        return num / den

    q = p - 0.5
    r = q * q
    num = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q
    den = (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    return num / den


def wilson_ci(k: int, n: int, conf: float = 0.95) -> Tuple[float, float]:
    """
    Wilson score interval for a binomial proportion.
    Returns (low, high) as proportions in [0,1].
    """
    if n <= 0:
        raise ValueError("n must be > 0")
    if not (0 <= k <= n):
        raise ValueError("k must be between 0 and n")
    if not (0.0 < conf < 1.0):
        raise ValueError("conf must be in (0,1)")

    alpha = 1.0 - conf
    z = normal_quantile(1.0 - alpha / 2.0)

    phat = k / n
    z2 = z * z

    denom = 1.0 + z2 / n
    center = (phat + z2 / (2.0 * n)) / denom
    half_width = (z * math.sqrt((phat * (1.0 - phat) + z2 / (4.0 * n)) / n)) / denom

    low = max(0.0, center - half_width)
    high = min(1.0, center + half_width)
    return low, high


def parse_result(s: str) -> Result:
    """
    Parse 'Label=k/n' with flexible whitespace.
    Examples:
      "Smartphone apps=28/42"
      "Wearables preferred = 26 / 42"
    """
    s = s.strip()
    if "=" not in s:
        raise ValueError(f"Missing '=' in '{s}'. Expected format: Label=k/n")

    label, frac = s.split("=", 1)
    label = label.strip()
    frac = frac.strip()

    m = re.fullmatch(r"(\d+)\s*/\s*(\d+)", frac)
    if not m:
        raise ValueError(f"Bad fraction '{frac}' in '{s}'. Expected k/n like 28/42")

    k = int(m.group(1))
    n = int(m.group(2))
    if n <= 0:
        raise ValueError(f"n must be > 0 in '{s}'")
    if k < 0 or k > n:
        raise ValueError(f"k must be in [0,n] in '{s}'")

    if not label:
        label = f"{k}/{n}"
    return Result(label=label, k=k, n=n)


def fmt_percent(x: float, digits: int) -> str:
    return f"{x * 100:.{digits}f}"


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Compute Wilson score confidence intervals for key proportions (binomial)."
    )
    ap.add_argument(
        "results",
        nargs="+",
        help='Key results as "Label=k/n" (e.g., "Smartphone apps=28/42").',
    )
    ap.add_argument(
        "--conf",
        type=float,
        default=0.95,
        help="Confidence level (default: 0.95).",
    )
    ap.add_argument(
        "--digits",
        type=int,
        default=2,
        help="Decimal digits for percentages and CI bounds (default: 2).",
    )
    ap.add_argument(
        "--as-percent",
        action="store_true",
        help="Print proportion and CI as percentages (default).",
    )
    ap.add_argument(
        "--as-prop",
        action="store_true",
        help="Print proportion and CI as proportions in [0,1] instead of percentages.",
    )

    args = ap.parse_args(argv)

    if args.as_percent and args.as_prop:
        print("Error: Choose only one of --as-percent or --as-prop.", file=sys.stderr)
        return 2

    # Default is percent unless user explicitly chooses prop
    use_prop = args.as_prop

    parsed: List[Result] = []
    for s in args.results:
        parsed.append(parse_result(s))

    # Output header
    if use_prop:
        header = ["Label", "k", "n", "p_hat", f"Wilson {int(args.conf*100)}% CI [low, high]"]
    else:
        header = ["Label", "k", "n", "%", f"Wilson {int(args.conf*100)}% CI [low, high]"]

    rows = []
    for r in parsed:
        low, high = wilson_ci(r.k, r.n, conf=args.conf)
        phat = r.k / r.n

        if use_prop:
            p_str = f"{phat:.{args.digits}f}"
            ci_str = f"[{low:.{args.digits}f}, {high:.{args.digits}f}]"
        else:
            p_str = fmt_percent(phat, args.digits)
            ci_str = f"[{fmt_percent(low, args.digits)}%, {fmt_percent(high, args.digits)}%]"

        rows.append([r.label, str(r.k), str(r.n), p_str, ci_str])

    # Pretty print as fixed-width table
    col_widths = [len(h) for h in header]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    def print_row(cells: List[str]) -> None:
        line = "  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(cells))
        print(line)

    print_row(header)
    print_row(["-" * w for w in col_widths])
    for row in rows:
        print_row(row)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


"""
Label                                                   k   n   %     Wilson 95% CI [low, high]
------------------------------------------------------  --  --  ----  -------------------------
Q6. Samartphone-based (66.67%)                          28  42  66.7  [51.6%, 79.0%]           
Q6. not use any (23.81%)                                10  42  23.8  [13.5%, 38.5%]           
Q8. satisfied (46.88%)                                  15  32  46.9  [30.9%, 63.6%]           
Q8. dissatisfaction (15.63%)                            5   32  15.6  [6.9%, 31.8%]            
Q8. uncertainty (6.25%)                                 2   32  6.2   [1.7%, 20.1%]            
Q11. finding routes                                     29  42  69.0  [54.0%, 80.9%]           
Q11. locating objects in outdoor                        24  42  57.1  [42.2%, 70.9%]           
Q12. Head-level (76.19)                                 32  42  76.2  [61.5%, 86.5%]           
Q12. ground- & chest-level (40.48%)                     17  42  40.5  [27.0%, 55.5%]           
Q7. using for outdoor or for both (93.75%)              30  32  93.8  [79.9%, 98.3%]           
Q13. wearable (61.9%)                                   26  42  61.9  [46.8%, 75.0%]           
Q13. handheld (28.57%)                                  12  42  28.6  [17.2%, 43.6%]           
Q13. other (9.52%)                                      4   42  9.5   [3.8%, 22.1%]            
Q14. speech (40.48%)                                    17  42  40.5  [27.0%, 55.5%]           
Q14. Multimodal (30.95%)                                13  42  31.0  [19.1%, 46.0%]           
Q14. Tactile (19.05%)                                   8   42  19.0  [10.0%, 33.3%]           
Q15. Hands & arms (57.14%)                              24  42  57.1  [42.2%, 70.9%]           
Q17. obstcle-free (61.9%)                               26  42  61.9  [46.8%, 75.0%]           
Q17. Route info. (54.76%)                               23  42  54.8  [39.9%, 68.8%]           
Q17. Constant assistance (47.62%)                       20  42  47.6  [33.4%, 62.3%]           
Q17. hortest-distance & rapid re-routing (38.10%)       16  42  38.1  [25.0%, 53.2%]           
Q16. ease of use (80.95%)                               34  42  81.0  [66.7%, 90.0%]           
Q16. low cost (66.67%)                                  28  42  66.7  [51.6%, 79.0%]           
Q16. mental load & device weight (52.38%)               22  42  52.4  [37.7%, 66.6%]           
Q16. physical effort & avoidance of obstacles (47.62%)  20  42  47.6  [33.4%, 62.3%]           
Q9. sufficient feedback (18.75%)                        6   32  18.8  [8.9%, 35.3%]            
Q9. insufficient feedback - obstacles (31.25%)          10  32  31.2  [18.0%, 48.6%]           
Q9. insufficient feedback outdoor (25.00%)              8   32  25.0  [13.3%, 42.1%]           
Q9. insufficient feedback - intdoor (12.50%)            4   32  12.5  [5.0%, 28.1%]            
Q10. always or most of the time (40.63%)                13  32  40.6  [25.5%, 57.7%]           
Q10. sometimes (37.5%)                                  12  32  37.5  [22.9%, 54.7%]           
Q10. rarely or never (18.75%)                           6   32  18.8  [8.9%, 35.3%]            
Q10. unsure (3.13%)                                     1   32  3.1   [0.6%, 15.7%]   
"""
