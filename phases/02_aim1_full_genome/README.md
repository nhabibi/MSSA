========================================================
## AIM 1 (FULL GENOME COEVOLUTION MODELING)
========================================================

1) LOAD DATA
- Full-length HIV-1 FASTA sequences

2) PREPROCESS
- Remove:
  - >10% Ns
  - incomplete genomes (HXB2 length-based filter)
  - length outliers (z-score > 3)

3) SPLIT SUBTYPES
- Separate into B and O

4) MSA (MAFFT)
- High accuracy mode:
  mafft --linsi --thread -1 input.fasta > aligned.fasta

5) MESSI
- Run per subtype on full genome alignment
- Same outputs:
  λ, P(λ>0), Bayes factor, pairing probabilities

6) INTERPRETATION
- Genome-wide RNA structural constraint maps
- Conserved RNA structural cores
- Subtype-specific coevolution hotspots
