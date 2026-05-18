#!/usr/bin/env python3

# MSSA basic pipeline
# Step 1: Align sequences with MAFFT.
# Step 2: Build phylogenetic tree with FastTree.
# Step 3: Run coevolution analysis.
# Note: For pilot datasets, use R-scape.
# Note: For larger/full analyses later, use MESSI.

import subprocess
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

INPUT_FASTA = Path("input.fasta")
OUTPUT_DIR = Path("outputs")
USE_PILOT_RSCAPE = True  # True = R-scape, False = MESSI

ALIGNED_FASTA = OUTPUT_DIR / "aligned.fasta"
TREE_FILE = OUTPUT_DIR / "phylogeny.nwk"
COEVOLUTION_DIR = OUTPUT_DIR / "coevolution"


############################################################
# Pipeline steps
############################################################

def step_1_align():
    run_cmd(["mafft", "--auto", str(INPUT_FASTA)], stdout_file=ALIGNED_FASTA)


def step_2_tree():
    run_cmd(["FastTree", "-nt", str(ALIGNED_FASTA)], stdout_file=TREE_FILE)


def step_3_coevolution():
    if USE_PILOT_RSCAPE:
        run_cmd(["R-scape", "--outdir", str(COEVOLUTION_DIR), str(ALIGNED_FASTA)])
    else:
        run_cmd(
            [
                "messi",
                "--msa",
                str(ALIGNED_FASTA),
                "--tree",
                str(TREE_FILE),
                "--outdir",
                str(COEVOLUTION_DIR),
            ]
        )


############################################################
# Main
############################################################

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    COEVOLUTION_DIR.mkdir(parents=True, exist_ok=True)

    print("MSSA pipeline start")
    step_1_align()
    step_2_tree()
    step_3_coevolution()
    print("MSSA pipeline done")
    print("Aligned:", ALIGNED_FASTA)
    print("Tree:", TREE_FILE)
    print("Coevolution:", COEVOLUTION_DIR)


if __name__ == "__main__":
    main()
