#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path

def run_cmd(cmd, stdout_file=None):
    print("[CMD]", " ".join(str(c) for c in cmd))
    if stdout_file is None:
        subprocess.run(cmd, check=True)
    else:
        with open(stdout_file, "w", encoding="utf-8") as out:
            subprocess.run(cmd, check=True, stdout=out)

def main():
    # Setup paths
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    results_dir = base_dir / "results"
    data_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    # --- Step 1: Preprocess (Placeholder for future implementation) ---
    B_tar_unaligned = data_dir / "B_tar_unaligned.fasta"
    O_tar_unaligned = data_dir / "O_tar_unaligned.fasta"
    B_tar_unaligned_preprocessed = data_dir / "B_tar_unaligned_preprocessed.fasta"
    O_tar_unaligned_preprocessed = data_dir / "O_tar_unaligned_preprocessed.fasta"
    shutil.copy(B_tar_unaligned, B_tar_unaligned_preprocessed)
    shutil.copy(O_tar_unaligned, O_tar_unaligned_preprocessed)
    print("✓ Step 1: Preprocess completed")

    # --- Step 2: MSA (MAFFT) ---
    B_tar_aligned = data_dir / "B_tar_aligned.fasta"
    O_tar_aligned = data_dir / "O_tar_aligned.fasta"
    run_cmd(["mafft", "--auto", "--thread", "-1", str(B_tar_unaligned_preprocessed)], stdout_file=B_tar_aligned)
    run_cmd(["mafft", "--auto", "--thread", "-1", str(O_tar_unaligned_preprocessed)], stdout_file=O_tar_aligned)
    print("✓ Step 2: MSA (MAFFT) completed")

    # --- Step 3: MESSI ---
    docker_runner = base_dir.parent.parent / "MESSI" / "run_messi_docker.sh"
    B_messi = results_dir / "B_messi.csv"
    O_messi = results_dir / "O_messi.csv"
    run_cmd([str(docker_runner), "--alignment", str(B_tar_aligned), "--output", str(B_messi)])
    run_cmd([str(docker_runner), "--alignment", str(O_tar_aligned), "--output", str(O_messi)])
    print("✓ Step 3: MESSI completed")

    # --- Step 4: Interpret (Placeholder for future implementation) ---
    print("✓ Step 4: Interpret (placeholder)")

    print("✓ Pipeline completed. Results saved in:", results_dir)

if __name__ == "__main__":
    main()
