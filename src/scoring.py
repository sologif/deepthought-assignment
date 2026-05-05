"""
DeepThought Internship — Federer Scoring Engine
================================================
Deterministic scoring of target companies against
DeepThought's 6-criterion Ideal Customer Profile.

Usage:
    python scoring.py                       # scores the default CSV
    python scoring.py --input my_data.csv   # scores a custom file
"""

import argparse
import csv
import os
import sys

# ──────────────────────────────────────────────
# Criterion weights (must sum to 100)
# ──────────────────────────────────────────────
WEIGHTS = {
    "C1 Manufacturer": 10,
    "C2 India-Based": 5,
    "C3 Differentiated": 25,
    "C4 Technical DM": 20,
    "C5 Growing Sector": 20,
    "C6 Growth Signals": 20,
}

# Rating → numeric multiplier
RATING_MAP = {
    "Strong": 1.0,
    "Moderate": 0.6,
    "Weak": 0.2,
}


def score_company(row: dict) -> int:
    """
    Compute a Federer Score (0-100) for a single company row.

    Parameters
    ----------
    row : dict
        A dictionary with keys matching the criterion column headers.

    Returns
    -------
    int
        Federer Score rounded to the nearest integer.
    """
    total = 0.0
    for criterion, weight in WEIGHTS.items():
        rating = row.get(criterion, "Weak").strip()
        multiplier = RATING_MAP.get(rating, 0.2)
        total += weight * multiplier
    return round(total)


def classify(score: int) -> str:
    """
    Map a numeric Federer Score to a verdict label.

    Parameters
    ----------
    score : int
        Federer Score (0-100).

    Returns
    -------
    str
        One of 'Federer', 'Borderline', or 'Not a fit'.
    """
    if score >= 80:
        return "Federer"
    elif score >= 60:
        return "Borderline"
    else:
        return "Not a fit"


def process_csv(input_path: str, output_path: str = None) -> list:
    """
    Read an input CSV, compute scores, and write the scored output.

    Parameters
    ----------
    input_path : str
        Path to the input CSV file.
    output_path : str, optional
        Path for the scored output CSV. Defaults to input with '_scored' suffix.

    Returns
    -------
    list
        List of scored company dictionaries.
    """
    if not os.path.exists(input_path):
        print(f"Error: File not found — {input_path}")
        sys.exit(1)

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_scored{ext}"

    scored_companies = []

    with open(input_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            score = score_company(row)
            verdict = classify(score)
            row["Federer Score"] = str(score)
            row["Overall Verdict"] = verdict
            scored_companies.append(row)

    # Sort by score descending
    scored_companies.sort(key=lambda r: int(r["Federer Score"]), reverse=True)

    # Write output
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scored_companies)

    return scored_companies


def print_summary(companies: list) -> None:
    """Print a formatted summary table to stdout."""
    print("\n" + "=" * 80)
    print("FEDERER SCORING RESULTS")
    print("=" * 80)
    print(f"\n{'Rank':<6}{'Company':<40}{'Score':<8}{'Verdict':<15}")
    print("-" * 69)

    for i, company in enumerate(companies, 1):
        name = company.get("Company Name", "Unknown")[:38]
        score = company.get("Federer Score", "N/A")
        verdict = company.get("Overall Verdict", "N/A")
        print(f"{i:<6}{name:<40}{score:<8}{verdict:<15}")

    # Summary stats
    total = len(companies)
    federer_count = sum(1 for c in companies if c.get("Overall Verdict") == "Federer")
    borderline_count = sum(1 for c in companies if c.get("Overall Verdict") == "Borderline")
    not_fit_count = total - federer_count - borderline_count

    print("\n" + "-" * 69)
    print(f"Total: {total} companies")
    print(f"  Federer:    {federer_count} ({federer_count/total*100:.0f}%)")
    print(f"  Borderline: {borderline_count} ({borderline_count/total*100:.0f}%)")
    print(f"  Not a fit:  {not_fit_count} ({not_fit_count/total*100:.0f}%)")
    print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="DeepThought Federer Scoring Engine"
    )
    parser.add_argument(
        "--input", "-i",
        default=os.path.join(os.path.dirname(__file__), "..", "output", "target_companies_25.csv"),
        help="Path to input CSV (default: output/target_companies_25.csv)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Path for scored output CSV (default: <input>_scored.csv)",
    )
    args = parser.parse_args()

    print(f"Scoring companies from: {args.input}")
    companies = process_csv(args.input, args.output)
    print_summary(companies)

    out = args.output or os.path.splitext(args.input)[0] + "_scored.csv"
    print(f"Scored CSV written to: {out}")


if __name__ == "__main__":
    main()
