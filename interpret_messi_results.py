#!/usr/bin/env python3

############################################################
# Imports
############################################################

import argparse
import csv
from pathlib import Path
import matplotlib.pyplot as plt


############################################################
# Helpers
############################################################

def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def pick_column(headers, names):
    for name in names:
        if name in headers:
            return name
    return None


############################################################
# Part 1: Plots
############################################################

def plot_hist(values, title, xlabel, out_path):
    plt.figure(figsize=(7.5, 4.5))
    plt.hist(values, bins=30, color="#2c7fb8", edgecolor="white")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


############################################################
# Input loading
############################################################

def load_first_table(input_dir):
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() != ".tsv":
            continue

        with open(path, "r", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))

        if rows:
            return path, rows

    return None, []


############################################################
# Main
############################################################

def main():
    parser = argparse.ArgumentParser(description="Minimal MESSI interpretation summary")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    table_path, rows = load_first_table(args.input)
    if not rows:
        print("[WARN] No TSV table found for interpretation")
        return

    headers = list(rows[0].keys())
    i_col = pick_column(headers, ["i"])
    j_col = pick_column(headers, ["j"])
    lambda_col = pick_column(headers, ["lambda"])
    pij_col = pick_column(headers, ["p_ij", "pij"])
    bf_col = pick_column(headers, ["bf"])

    if not i_col or not j_col:
        print(f"[WARN] Found {table_path}, but missing i/j columns")
        return

    parsed = []
    for row in rows:
        i_val = to_float(row.get(i_col))
        j_val = to_float(row.get(j_col))
        if i_val is None or j_val is None:
            continue

        parsed.append(
            {
                "i": int(i_val),
                "j": int(j_val),
                "lambda": to_float(row.get(lambda_col)) if lambda_col else None,
                "p_ij": to_float(row.get(pij_col)) if pij_col else None,
                "bf": to_float(row.get(bf_col)) if bf_col else None,
            }
        )

    if not parsed:
        print("[WARN] No valid rows found for interpretation")
        return

    args.output.mkdir(parents=True, exist_ok=True)

    top = sorted(parsed, key=lambda x: x["lambda"] if x["lambda"] is not None else -1.0, reverse=True)[:20]

    top_path = args.output / "top_coevolving_pairs.tsv"
    with open(top_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["i", "j", "lambda", "p_ij", "bf"])
        for row in top:
            writer.writerow([row["i"], row["j"], row["lambda"], row["p_ij"], row["bf"]])

    lambda_vals = [r["lambda"] for r in parsed if r["lambda"] is not None]
    pij_vals = [r["p_ij"] for r in parsed if r["p_ij"] is not None]
    strong_pairs = [r for r in parsed if (r["lambda"] is not None and r["lambda"] > 2.0) or (r["bf"] is not None and r["bf"] > 10.0)]

    if lambda_vals:
        plot_hist(
            lambda_vals,
            "Coevolution Strength (lambda)",
            "lambda",
            args.output / "coevolution_strength_lambda.png",
        )

    if pij_vals:
        plot_hist(
            pij_vals,
            "Posterior Base-Pairing Probability P(i,j)",
            "P(i,j)",
            args.output / "posterior_basepair_probability.png",
        )

    ############################################################
    # Part 2: Report
    ############################################################

    summary_path = args.output / "interpretation_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as handle:
        handle.write("MESSI interpretation summary\n")
        handle.write(f"source_table\t{table_path}\n")
        handle.write(f"total_pairs\t{len(parsed)}\n")
        handle.write(f"pairs_with_lambda\t{len(lambda_vals)}\n")
        handle.write(f"pairs_with_p_ij\t{len(pij_vals)}\n")
        handle.write(f"strong_support_pairs\t{len(strong_pairs)}\n")
        if lambda_vals:
            handle.write(f"lambda_mean\t{sum(lambda_vals) / len(lambda_vals):.4f}\n")
        if pij_vals:
            handle.write(f"p_ij_mean\t{sum(pij_vals) / len(pij_vals):.4f}\n")

    print("[INFO] Output files:", summary_path, top_path)


if __name__ == "__main__":
    main()
