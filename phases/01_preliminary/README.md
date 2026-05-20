# Preliminary Phase (TAR Validation)

========================================================
## PRELIMINARY (TAR ELEMENT VALIDATION)
========================================================
- Run separately per subtype (B and O)


## 1) PREPROCESS
- Input:
	- data/B_tar_unaligned.fasta
	- data/O_tar_unaligned.fasta

- Output:
    - data/B_tar_unaligned_preprocessed.fasta
	- data/O_tar_unaligned_preprocessed.fasta

- Task: ToAdd

## 2) MSA
- Input:
	- data/B_tar_unaligned_preprocessed.fasta
	- data/O_tar_unaligned_preprocessed.fasta

- Output:
    - data/B_tar_aligned.fasta
	- data/O_tar_aligned.fasta
    
- Task: MAFFT

## 3) MESSI
- Input:
    - data/B_tar_aligned.fasta
	- data/O_tar_aligned.fasta

- Output:
	- results/B_messi.csv
	- results/O_messi.csv

- Task: Run MESSI with Docker wrapper in MESSI/run_messi_docker.sh

## 4) Interpret
- Iutput:
	- results/B_messi.csv
	- results/O_messi.csv

- Output:
	- B_Plots
	- O_Plots

- Task: ToAdd

========================================================
