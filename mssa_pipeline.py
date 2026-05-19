#!/usr/bin/env python3

# MSSA basic pipeline
# Step 1: Align sequences with MAFFT.
# Step 2: Build phylogenetic tree with FastTree.
# Step 3: Run coevolution analysis with MESSI.
# Step 4: Plot + interpret MESSI outputs.

import subprocess
import sys
from pathlib import Path

############################################################
# Helper functions
############################################################

def run_cmd(cmd, stdout_file=None):
    print("[CMD]", " ".join(cmd))
    if stdout_file is None:
        subprocess.run(cmd, check=True)
    else:
        with open(stdout_file, "w", encoding="utf-8") as out:
            subprocess.run(cmd, check=True, stdout=out)


############################################################
# Basic settings (edit these paths)
############################################################

INPUT_FASTA = Path("input/input.fasta")
OUTPUT_DIR = Path("output")

ALIGNED_FASTA = OUTPUT_DIR / "aligned.fasta"
TREE_FILE = OUTPUT_DIR / "phylogeny.nwk"
COEVOLUTION_DIR = OUTPUT_DIR / "coevolution"
INTERPRET_DIR = OUTPUT_DIR / "interpret"


############################################################
# Pipeline steps
############################################################

def step_1_align():
    run_cmd(["mafft", "--auto", str(INPUT_FASTA)], stdout_file=ALIGNED_FASTA)


def step_2_tree():
    run_cmd(["FastTree", "-nt", str(ALIGNED_FASTA)], stdout_file=TREE_FILE)


def step_3_coevolution():
    run_cmd(["messi", "--msa", str(ALIGNED_FASTA), "--tree", str(TREE_FILE), "--outdir", str(COEVOLUTION_DIR), "--model", "basic"])


def step_4_interpret():
    run_cmd(
        [
            sys.executable,
            "interpret_messi_results.py",
            "--input",
            str(COEVOLUTION_DIR),
            "--output",
            str(INTERPRET_DIR),
        ]
    )


############################################################
# Main
############################################################

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    COEVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    INTERPRET_DIR.mkdir(parents=True, exist_ok=True)

    print("MSSA pipeline start")
    step_1_align()
    step_2_tree()
    step_3_coevolution()
    step_4_interpret()
    print("MSSA pipeline done")
    print("Aligned:", ALIGNED_FASTA)
    print("Tree:", TREE_FILE)
    print("Coevolution:", COEVOLUTION_DIR)
    print("Interpret:", INTERPRET_DIR)


if __name__ == "__main__":
    main()
