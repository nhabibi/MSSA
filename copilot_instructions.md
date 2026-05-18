# Multiple Secondary Structure Alignment (MSSA)

## Phases

| Phase | Scope |
|-------|-------|
| Phase I | Pilot Study (TAR region) |
| Phase II | Aim 1 — Full genome processing |
| Phase III | Aim 2 — Large-scale coevolution modeling |
| Phase IV | AI Role — Post-processing and interpretation |

## Model

**Input**
- MSA: Aligned HIV-1 sequences
- Phylogenetic Tree

**Output**

| Output | Description |
|--------|-------------|
| Coevolution Strength (λ) | Strength of compensatory evolution between paired sites |
| Posterior Base-Pairing Probability P(i,j) | Probability that positions i and j form a real base pair |
| Predicted RNA Secondary Structure (SS) | Consensus stem–loop architecture conserved across sequences |
| Subtype Structural Difference (ΔSS) | Structural differences between subtypes B and O |

## Pipeline

### 1. RNA Sequences
- Source: https://www.hiv.lanl.gov/
- Phase I: TAR sequences (~60 nt)
- Later phases: Full HIV-1 genomes

### 2. MSA
- Tool: MAFFT

### 3. Dataset Cleaning

### 4. Phylogenetic Tree
- Phase I: FastTree
- Later phases: IQ-TREE
> Note: The phylogenetic tree is a direct input to MESSI alongside the MSA.

### 5. Coevolution Analysis
- Phase I: R-scape _(TAR is too short for reliable MESSI parameter estimation)_
- Later phases: MESSI

### 6. Result Analysis
- Compare coevolution pairs (λ)
- Check structure consistency (SS, P(i,j))
- Identify conserved structural elements

### 7. AI-Based Analysis
Using Bio LLMs to jointly analyze all MESSI outputs (predicted secondary structure, posterior base-pairing probabilities, coevolution strength, and subtype structural difference) to reduce false positives and false negatives.
