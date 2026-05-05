"""
DeepThought Internship — Data Analysis & Visualization
=======================================================
Generates charts and graphs from the 25 Federer-scored companies.
Outputs PNG charts to the analysis/ directory.

Usage:
    pip install matplotlib
    python src/analysis.py
"""

import csv
import os
import sys

# Try importing matplotlib; install hint if missing
try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend for PNG output
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("matplotlib is required. Install with: pip install matplotlib")
    sys.exit(1)

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")
INPUT_CSV = os.path.join(PROJECT_ROOT, "output", "target_companies_25.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "analysis")

# ──────────────────────────────────────────────
# Color palette (premium dark theme)
# ──────────────────────────────────────────────
COLORS = {
    "bg": "#0d1117",
    "card": "#161b22",
    "text": "#e6edf3",
    "subtext": "#8b949e",
    "accent1": "#58a6ff",
    "accent2": "#3fb950",
    "accent3": "#d29922",
    "accent4": "#f85149",
    "accent5": "#bc8cff",
    "accent6": "#39d353",
    "gradient": ["#58a6ff", "#3fb950", "#d29922", "#f85149", "#bc8cff", "#39d353",
                 "#79c0ff", "#56d364", "#e3b341", "#ff7b72", "#d2a8ff", "#2ea043"],
}


def load_data(csv_path):
    """Load company data from CSV."""
    companies = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)
    return companies


def setup_style():
    """Apply dark premium style to matplotlib."""
    plt.rcParams.update({
        "figure.facecolor": COLORS["bg"],
        "axes.facecolor": COLORS["card"],
        "axes.edgecolor": COLORS["subtext"],
        "axes.labelcolor": COLORS["text"],
        "text.color": COLORS["text"],
        "xtick.color": COLORS["subtext"],
        "ytick.color": COLORS["subtext"],
        "grid.color": "#21262d",
        "grid.alpha": 0.6,
        "font.family": "sans-serif",
        "font.size": 11,
    })


def chart_score_distribution(companies, output_dir):
    """Bar chart: Federer Score for each company."""
    fig, ax = plt.subplots(figsize=(16, 9))

    names = [c["Company Name"][:25] for c in companies]
    scores = [int(c["Federer Score"]) for c in companies]

    # Color bars by score tier
    bar_colors = []
    for s in scores:
        if s == 100:
            bar_colors.append(COLORS["accent2"])
        elif s >= 95:
            bar_colors.append(COLORS["accent1"])
        elif s >= 90:
            bar_colors.append(COLORS["accent3"])
        else:
            bar_colors.append(COLORS["accent5"])

    bars = ax.barh(range(len(names)), scores, color=bar_colors, edgecolor="none", height=0.7)

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("Federer Score (0-100)", fontsize=12, fontweight="bold")
    ax.set_title("Federer Score Distribution — 25 Target Companies", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlim(0, 110)
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    # Add score labels on bars
    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                str(score), va="center", fontsize=9, fontweight="bold", color=COLORS["text"])

    # Legend
    legend_patches = [
        mpatches.Patch(color=COLORS["accent2"], label="Score = 100"),
        mpatches.Patch(color=COLORS["accent1"], label="Score = 95"),
        mpatches.Patch(color=COLORS["accent3"], label="Score = 90"),
        mpatches.Patch(color=COLORS["accent5"], label="Score < 90"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=10,
              facecolor=COLORS["card"], edgecolor=COLORS["subtext"])

    plt.tight_layout()
    path = os.path.join(output_dir, "01_score_distribution.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {path}")


def chart_revenue_breakdown(companies, output_dir):
    """Pie chart: Revenue band distribution."""
    fig, ax = plt.subplots(figsize=(10, 10))

    revenue_counts = {}
    for c in companies:
        band = c.get("Revenue Band", "Unknown").strip()
        revenue_counts[band] = revenue_counts.get(band, 0) + 1

    labels = list(revenue_counts.keys())
    sizes = list(revenue_counts.values())
    colors = COLORS["gradient"][:len(labels)]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, autopct="%1.0f%%", startangle=140,
        colors=colors, pctdistance=0.8,
        wedgeprops={"linewidth": 2, "edgecolor": COLORS["bg"]},
    )

    for t in autotexts:
        t.set_fontsize(13)
        t.set_fontweight("bold")
        t.set_color(COLORS["text"])

    ax.legend(labels, loc="lower left", fontsize=11,
              facecolor=COLORS["card"], edgecolor=COLORS["subtext"])
    ax.set_title("Revenue Band Distribution", fontsize=16, fontweight="bold", pad=20)

    plt.tight_layout()
    path = os.path.join(output_dir, "02_revenue_breakdown.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {path}")


def chart_criteria_heatmap(companies, output_dir):
    """Heatmap: Per-company criterion ratings."""
    fig, ax = plt.subplots(figsize=(14, 12))

    criteria = ["C1 Manufacturer", "C2 India-Based", "C3 Differentiated",
                "C4 Technical DM", "C5 Growing Sector", "C6 Growth Signals"]
    names = [c["Company Name"][:25] for c in companies]

    rating_to_num = {"Strong": 3, "Moderate": 2, "Weak": 1}
    color_map = {3: COLORS["accent2"], 2: COLORS["accent3"], 1: COLORS["accent4"]}

    # Build matrix
    matrix = []
    for c in companies:
        row = [rating_to_num.get(c.get(cr, "Weak").strip(), 1) for cr in criteria]
        matrix.append(row)

    # Draw cells
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            rect = plt.Rectangle((j, i), 1, 1, facecolor=color_map[val],
                                 edgecolor=COLORS["bg"], linewidth=2)
            ax.add_patch(rect)
            label = {3: "Strong", 2: "Moderate", 1: "Weak"}[val]
            ax.text(j + 0.5, i + 0.5, label, ha="center", va="center",
                    fontsize=8, fontweight="bold", color=COLORS["text"])

    ax.set_xlim(0, len(criteria))
    ax.set_ylim(0, len(names))
    ax.set_xticks([x + 0.5 for x in range(len(criteria))])
    ax.set_xticklabels([c.replace("C1 ", "C1\n").replace("C2 ", "C2\n").replace("C3 ", "C3\n")
                        .replace("C4 ", "C4\n").replace("C5 ", "C5\n").replace("C6 ", "C6\n")
                        for c in criteria], fontsize=9, ha="center")
    ax.set_yticks([y + 0.5 for y in range(len(names))])
    ax.set_yticklabels(names, fontsize=9)
    ax.invert_yaxis()
    ax.set_title("Criterion Rating Heatmap — All 25 Companies", fontsize=16, fontweight="bold", pad=20)
    ax.tick_params(axis="both", length=0)

    legend_patches = [
        mpatches.Patch(color=COLORS["accent2"], label="Strong"),
        mpatches.Patch(color=COLORS["accent3"], label="Moderate"),
        mpatches.Patch(color=COLORS["accent4"], label="Weak"),
    ]
    ax.legend(handles=legend_patches, loc="upper right", fontsize=10,
              facecolor=COLORS["card"], edgecolor=COLORS["subtext"])

    plt.tight_layout()
    path = os.path.join(output_dir, "03_criteria_heatmap.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {path}")


def chart_segment_distribution(companies, output_dir):
    """Bar chart: Companies by segment."""
    fig, ax = plt.subplots(figsize=(12, 7))

    segments = {}
    for c in companies:
        seg = c.get("Segment", "Unknown").strip()
        segments[seg] = segments.get(seg, 0) + 1

    # Sort by count
    sorted_segs = sorted(segments.items(), key=lambda x: x[1], reverse=True)
    labels = [s[0] for s in sorted_segs]
    counts = [s[1] for s in sorted_segs]
    colors = COLORS["gradient"][:len(labels)]

    bars = ax.bar(range(len(labels)), counts, color=colors, edgecolor="none", width=0.6)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=9, rotation=30, ha="right")
    ax.set_ylabel("Number of Companies", fontsize=12, fontweight="bold")
    ax.set_title("Companies by Industry Segment", fontsize=16, fontweight="bold", pad=20)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                str(count), ha="center", fontsize=11, fontweight="bold", color=COLORS["text"])

    plt.tight_layout()
    path = os.path.join(output_dir, "04_segment_distribution.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {path}")


def chart_score_vs_revenue(companies, output_dir):
    """Scatter plot: Score vs Revenue Band."""
    fig, ax = plt.subplots(figsize=(12, 8))

    revenue_order = {"Rs.10-50Cr": 1, "Rs.50-100Cr": 2, "Rs.100-200Cr": 3,
                     "Rs.200-500Cr": 4, ">Rs.500Cr": 5}

    x_vals, y_vals, labels, colors_list = [], [], [], []
    for c in companies:
        band = c.get("Revenue Band", "Unknown").strip()
        score = int(c.get("Federer Score", 0))
        x = revenue_order.get(band, 0)
        if x > 0:
            x_vals.append(x)
            y_vals.append(score)
            labels.append(c["Company Name"][:20])
            if score == 100:
                colors_list.append(COLORS["accent2"])
            elif score >= 95:
                colors_list.append(COLORS["accent1"])
            else:
                colors_list.append(COLORS["accent3"])

    ax.scatter(x_vals, y_vals, c=colors_list, s=150, edgecolors=COLORS["text"],
               linewidth=0.5, zorder=5, alpha=0.9)

    # Add company name labels
    for x, y, label in zip(x_vals, y_vals, labels):
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(8, 4),
                    fontsize=7, color=COLORS["subtext"])

    ax.set_xticks(list(revenue_order.values()))
    ax.set_xticklabels(list(revenue_order.keys()), fontsize=10)
    ax.set_xlabel("Revenue Band", fontsize=12, fontweight="bold")
    ax.set_ylabel("Federer Score", fontsize=12, fontweight="bold")
    ax.set_title("Federer Score vs. Revenue Band", fontsize=16, fontweight="bold", pad=20)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_ylim(80, 105)

    plt.tight_layout()
    path = os.path.join(output_dir, "05_score_vs_revenue.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {path}")


def chart_criterion_strength(companies, output_dir):
    """Stacked bar: Strong vs Moderate vs Weak counts per criterion."""
    fig, ax = plt.subplots(figsize=(12, 7))

    criteria = ["C1 Manufacturer", "C2 India-Based", "C3 Differentiated",
                "C4 Technical DM", "C5 Growing Sector", "C6 Growth Signals"]

    strong_counts, moderate_counts, weak_counts = [], [], []
    for cr in criteria:
        s = sum(1 for c in companies if c.get(cr, "").strip() == "Strong")
        m = sum(1 for c in companies if c.get(cr, "").strip() == "Moderate")
        w = len(companies) - s - m
        strong_counts.append(s)
        moderate_counts.append(m)
        weak_counts.append(w)

    x = range(len(criteria))
    short_labels = ["C1\nManufacturer", "C2\nIndia-Based", "C3\nDifferentiated",
                    "C4\nTechnical DM", "C5\nGrowing Sector", "C6\nGrowth Signals"]

    bars1 = ax.bar(x, strong_counts, color=COLORS["accent2"], label="Strong", width=0.5)
    bars2 = ax.bar(x, moderate_counts, bottom=strong_counts, color=COLORS["accent3"],
                   label="Moderate", width=0.5)
    bottom2 = [s + m for s, m in zip(strong_counts, moderate_counts)]
    bars3 = ax.bar(x, weak_counts, bottom=bottom2, color=COLORS["accent4"],
                   label="Weak", width=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(short_labels, fontsize=10)
    ax.set_ylabel("Number of Companies", fontsize=12, fontweight="bold")
    ax.set_title("Criterion Strength Analysis — All 25 Companies", fontsize=16, fontweight="bold", pad=20)
    ax.legend(fontsize=11, facecolor=COLORS["card"], edgecolor=COLORS["subtext"])
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout()
    path = os.path.join(output_dir, "06_criterion_strength.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {path}")


def chart_top10_radar(companies, output_dir):
    """Radar/spider chart for top 5 companies."""
    import math

    criteria = ["C1 Manufacturer", "C2 India-Based", "C3 Differentiated",
                "C4 Technical DM", "C5 Growing Sector", "C6 Growth Signals"]
    rating_to_num = {"Strong": 3, "Moderate": 2, "Weak": 1}

    top5 = sorted(companies, key=lambda c: int(c.get("Federer Score", 0)), reverse=True)[:5]
    n_criteria = len(criteria)
    angles = [n / float(n_criteria) * 2 * math.pi for n in range(n_criteria)]
    angles += angles[:1]  # close the polygon

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.set_facecolor(COLORS["card"])
    fig.patch.set_facecolor(COLORS["bg"])

    colors_top = [COLORS["accent1"], COLORS["accent2"], COLORS["accent3"],
                  COLORS["accent5"], COLORS["accent6"]]

    for i, company in enumerate(top5):
        values = [rating_to_num.get(company.get(cr, "Weak").strip(), 1) for cr in criteria]
        values += values[:1]
        ax.plot(angles, values, "o-", linewidth=2, color=colors_top[i],
                label=company["Company Name"][:25], markersize=6)
        ax.fill(angles, values, alpha=0.1, color=colors_top[i])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(["C1", "C2", "C3", "C4", "C5", "C6"], fontsize=12, color=COLORS["text"])
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Weak", "Moderate", "Strong"], fontsize=9, color=COLORS["subtext"])
    ax.set_ylim(0, 3.5)
    ax.set_title("Top 5 Companies — Radar Comparison", fontsize=16, fontweight="bold",
                 pad=30, color=COLORS["text"])
    ax.legend(loc="lower right", bbox_to_anchor=(1.3, 0), fontsize=10,
              facecolor=COLORS["card"], edgecolor=COLORS["subtext"])
    ax.spines["polar"].set_color(COLORS["subtext"])
    ax.tick_params(colors=COLORS["subtext"])
    ax.grid(color=COLORS["subtext"], alpha=0.3)

    plt.tight_layout()
    path = os.path.join(output_dir, "07_top5_radar.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] {path}")


def generate_summary_stats(companies, output_dir):
    """Generate a markdown summary of key statistics."""
    total = len(companies)
    scores = [int(c["Federer Score"]) for c in companies]
    avg_score = sum(scores) / total
    max_score = max(scores)
    min_score = min(scores)
    score_100 = sum(1 for s in scores if s == 100)
    score_95 = sum(1 for s in scores if s == 95)
    score_90 = sum(1 for s in scores if s == 90)
    score_lt90 = sum(1 for s in scores if s < 90)

    # Revenue breakdown
    revenue_counts = {}
    for c in companies:
        band = c.get("Revenue Band", "Unknown").strip()
        revenue_counts[band] = revenue_counts.get(band, 0) + 1

    # Segment breakdown
    segment_counts = {}
    for c in companies:
        seg = c.get("Segment", "Unknown").strip()
        segment_counts[seg] = segment_counts.get(seg, 0) + 1

    md = f"""# Data Analysis Summary — 25 Federer Companies

## Key Statistics
| Metric | Value |
|--------|-------|
| Total Companies | {total} |
| Average Federer Score | {avg_score:.1f} |
| Highest Score | {max_score} |
| Lowest Score | {min_score} |
| Companies scoring 100 | {score_100} |
| Companies scoring 95 | {score_95} |
| Companies scoring 90 | {score_90} |
| Companies scoring <90 | {score_lt90} |

## Revenue Band Distribution
| Revenue Band | Count | Percentage |
|-------------|-------|------------|
"""
    for band, count in sorted(revenue_counts.items(), key=lambda x: x[1], reverse=True):
        md += f"| {band} | {count} | {count/total*100:.0f}% |\n"

    md += f"""
## Segment Distribution
| Segment | Count | Percentage |
|---------|-------|------------|
"""
    for seg, count in sorted(segment_counts.items(), key=lambda x: x[1], reverse=True):
        md += f"| {seg} | {count} | {count/total*100:.0f}% |\n"

    md += """
## Charts Generated
1. `01_score_distribution.png` — Horizontal bar chart of Federer Scores
2. `02_revenue_breakdown.png` — Pie chart of revenue band distribution
3. `03_criteria_heatmap.png` — Heatmap of criterion ratings per company
4. `04_segment_distribution.png` — Bar chart of companies by segment
5. `05_score_vs_revenue.png` — Scatter plot: Score vs Revenue Band
6. `06_criterion_strength.png` — Stacked bar: Strong/Moderate/Weak per criterion
7. `07_top5_radar.png` — Radar chart comparing top 5 companies

## Key Insights
1. **High overall quality**: Average Federer Score of {avg_score:.1f}/100 indicates a strong target list
2. **Hyderabad dominance**: All 25 companies are based in Hyderabad's Genome Valley cluster
3. **Specialty Biotech focus**: The segment shows clear PLI tailwinds and government support
4. **Technical leadership**: Majority of companies have PhD-level founders/MDs
5. **Growth signals**: Most companies show active hiring, plant expansion, or new certifications
"""

    path = os.path.join(output_dir, "analysis_summary.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"  [OK] {path}")


def main():
    setup_style()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Loading data from: {INPUT_CSV}")
    companies = load_data(INPUT_CSV)
    print(f"Loaded {len(companies)} companies\n")

    print("Generating charts...")
    chart_score_distribution(companies, OUTPUT_DIR)
    chart_revenue_breakdown(companies, OUTPUT_DIR)
    chart_criteria_heatmap(companies, OUTPUT_DIR)
    chart_segment_distribution(companies, OUTPUT_DIR)
    chart_score_vs_revenue(companies, OUTPUT_DIR)
    chart_criterion_strength(companies, OUTPUT_DIR)
    chart_top10_radar(companies, OUTPUT_DIR)

    print("\nGenerating summary statistics...")
    generate_summary_stats(companies, OUTPUT_DIR)

    print(f"\n{'='*50}")
    print(f"All charts saved to: {OUTPUT_DIR}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
