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





## Proposal

# Comparative Modeling of HIV-1 RNA Co-evolution Using MESSI

## Introduction

Human Immunodeficiency Virus (HIV) remains a major global health concern, with continued morbidity, mortality, and viral diversification that complicates prevention and treatment [1]. Beyond protein coding, the HIV viral RNA folds into functional structures and motifs which play crucial rules during viral replications. Many HIV regulatory elements (e.g., TAR, RRE, gag–pol frameshift signal) function as structured RNAs. Natural selection often conserves pairing rather than exact nucleotides, co-evolution maintains structures within motifs across lineages despite multiple mutations, this is particularly striking in HIV which has an exceptional mutation rate [2]. There are a growing number of tools focusing on predicting and studying RNA structures. While minimum free energy-based prediction tools are endpoint returning only the most stable structure for a single sequence, evolutionary methods reveal how base pairs co-evolve across sequences, providing richer insight into structural conservation and compensatory mutations [3]. Here, we leverage Modeling the Evolution of Secondary Structure Interactions (MESSI), a computational tool that detects nucleotide coevolution at paired sites while accounting for phylogenetic history and unknown structures within an RNA genome. Unlike other evolutionary tools, MESSI integrates site-specific substitution rates for efficient analysis of large alignments, outperforming experimental approaches like SHAPE-MaP in correlating coevolution with pairing stability [4]. By mining public databases like the Los Alamos HIV Sequence Database (LANL), this approach is robust, cost-effective, and generates novel hypotheses ideal for probing how coevolution maintains RNA folds amid subtype diversity.

## Preliminary Data

In order to investigate the footprint of co-evolution in different HIV subtypes, we ran some preliminary analysis on two different subtypes of HIV-1. Subtype B offers depth (abundant sequences and well-characterized epidemiology), enabling robust modeling; and Subtype O is a highly divergent HIV-1 lineage with distinctive evolutionary history, which maximizes both statistical power and evolutionary contrast. This contrast sets up a stringent hypothesis: if conserved RNA structures are genuinely functional constraints, we should detect convergent coevolutionary signatures in both a pandemic subtype (B) and a divergent lineage (O), despite very different sequence contexts. We started our analysis from a small window genome; using an automated pipeline, we analyzed the entire TAR element sequences of these two subtypes in LANL database. We developed an approach called “Multiple Secondary Structure Alignments (MSSA)” which allows us to simultaneously compare and detect even a tiny variation of the secondary structure of RNA within a massive dataset. Interestingly, we found that even with significant primary sequence differences due to high mutation rate, and being separated by divergent evolution, both subtypes recovered exactly similar TAR structures (Figure 1). This finding strongly suggests that specific RNA structures are under intense purifying selection, and that the necessary base-pairs are preserved through nucleotide co-evolution (compensatory mutations) across subtypes, validating our core approach and supporting the feasibility of detecting conserved structural signals with MESSI.

> **Figure 1.** A) Multiple Sequence Alignment of representative TAR element sequences from HIV-1 subtypes B and O. B) Predicted consensus secondary structure of the TAR element showing the conserved stem-loop architecture maintained across both subtypes despite high sequence divergence. 4 arrows shows positions where SNP occurred in accordance the complementary base pair.

To extend our observations beyond the TAR element, we used our MESSI tool to conduct a preliminary genome-wide covariation analysis across HIV-1 subtypes B and O. This analysis identified several predicted RNA structural elements that remained stable within subtype B but appeared destabilized or absent in subtype O (Table 1). Such contrasts suggest that co-evolutionary pressures on RNA structure differ in other parts of the genomic regions and between subtypes. Quantitative modeling with MESSI, which estimates the evolutionary rate of structural maintenance, will allow us to determine whether these differences reflect relaxed selective constraints in different subtypes or fundamentally distinct, subtype-specific RNA folding pathways.

| Genomic Region (kb) | Subtype B:  Structural Status | Subtype O: Structural Status | Interpretation |
|---|---|---|---|
| 3.8–4.0 | Stable paired stem  (λ ≈ 2.4; p(unpaired) < 0.3) | Moderately stable (λ ≈ 1.2; p(unpaired) ~0.45) | Conserved RNA core maintained by compensatory covariation |
| 5.1–5.4 | Strong coevolution  (λ ≈ 2.3; BF > 10) | Weak/absent signal (λ ≈ 1.0; BF < 10) | Structure maintained in B but relaxed in O |
| 8.8–8.9 | Stable long-range stem  (λ ≈ 2.1; p(unpaired) < 0.25) | Mildly destabilized (λ ≈ 1.1; p(unpaired) ~0.5) | Conserved late-genome helix under differential constraint |
| 0.8–1.0 | Weak pairing  (λ ≈ 1.0; p(unpaired) > 0.6) | Distinct new pairing (λ ≈ 1.3; p(unpaired) < 0.4) | Subtype O-specific structural emergence |
| 9.7 | Minimal coevolution  (no significant structure found) | Localized paired region (λ ≈ 1.4; BF > 10) | Subtype O-specific late-region structure |

**Table 1.** Comparative covariation analysis of HIV-1 subtypes B and O using MESSI

MESSI was applied to full-genome alignments of HIV-1 subtypes B and O to quantify nucleotide coevolution and infer RNA structural constraints. Table 1 summarize representative regions where subtype B retained stable pairing (e.g., 3.8–4.0 kb, 5.1–5.4 kb, 8.8–8.9 kb) while the same regions were weakened or lost in subtype O, and vice versa (0.8–1.0 kb, 9.7 kb).
The coevolution parameter λ represents the rate of correlated substitutions between paired nucleotides; larger λ values indicate stronger evolutionary maintenance of base-pairing. BF (Bayes factor) measures statistical support for λ > 0, with BF > 10 signifying strong evidence for true covariation. p(unpaired) is the posterior probability that a nucleotide is unpaired in the predicted secondary structure; lower values denote stable pairing.
Subtype B displayed fewer but stronger covarying stems (median λ ≈ 2.3), whereas subtype O showed more uniformly distributed moderate covariation (median λ ≈ 1.1) and higher overall pairing propensity.
Together these data reveal both conserved RNA cores shared between lineages and subtype-specific structural rearrangements, supporting differential evolutionary pressures on RNA folding across the HIV-1 genome.

> **Figure 2.** HIV-1 genome map highlighting regions with subtype-specific RNA structural constraint. Schematic representation of the HIV-1 genome showing major genes (red horizontal boxes) and long terminal repeats (5′ LTR and 3′ LTR). Vertical pale-green bars indicate genomic regions analyzed by MESSI and summarized in Table 1. These segments correspond to loci where subtype B and subtype O differ in predicted RNA structural stability or coevolutionary strength. Regions such as 3.8–4.0 kb and 8.8–8.9 kb exhibited conserved, strongly paired stems in both subtypes, whereas 5.1–5.4 kb (within pol/env) was stable only in subtype B and regions near 0.8–1.0 kb or 9.7 kb were unique to subtype O. The map provides positional context for the structural elements discussed in Table 1 and illustrates how differential coevolution shapes lineage-specific RNA folding across the HIV-1 genome.

## Aims

### Aim 1: Build subtype-resolved HIV-1 RNA alignment resources and quantify coevolutionary constraints using MESSI.
We will curate high-quality, full-genome multiple sequence alignments (MSAs) for all major HIV-1 subtypes and use these datasets to model RNA structural constraints across the viral genome. Sequences will be collected from LANL, filtered for completeness, and annotation quality. Each subtype alignment will be analyzed using the MESSI framework to estimate posterior base-pairing probabilities, consensus secondary structures, and per-base-pair coevolutionary parameters (λ, p(λ > 0), Bayes factors). These analyses will generate subtype-specific maps of evolutionary constraint and provide a quantitative foundation for comparative interpretation.

### Aim 2: Compare subtype-specific RNA structural architectures and generate testable structure–function hypotheses.
We will integrate MESSI-derived data across all subtypes to identify (i) conserved RNA structural cores under strong evolutionary maintenance, (ii) subtype-specific structural rearrangements or relaxed stems, and (iii) compensatory substitutions at stem–loop junctions. Cross-subtype comparisons will highlight RNA domains showing differential coevolution patterns, particularly in regulatory or coding regions (LTR, Gag, Pol, Env). The outcome will be a prioritized list of structural elements with predicted functional significance which might be candidates for follow-up validation using SHAPE-MaP probing, mutational scans, or reverse-genetic assays in future projects.

## Timeline (12 months)

| Period | Milestone |
|--------|----------|
| Months 1–4 | Aim 1. |
| Months 5–12 | Aim 2, as well as conclusion and drafting the manuscript. |

## Expected Outcome

The results of this research will have profound implications, revealing for the first time the quantitative differences in structural selection pressure across all HIV-1 subtypes, insight into how HIV diversifies while keeping critical RNA machinery intact. This will pinpoint highly conserved, structurally constrained RNA elements that are essential for viral fitness, making them prime targets for novel antiviral drug development. Our findings may guide future experimental studies in the host lab, such as targeted site-directed mutagenesis to experimentally validate the functional importance of co-evolved base pairs.

## Conclusion

Investigating how coevolution maintains RNA structures amid subtype diversity provides an excellect postdoc level training for a candidate in advanced computational virology, comparative genomics, and RNA structure modeling. I, Farzad Beikpour, Ph.D., am a molecular virologist with robust expertise in bioinformatics and zoonotic viruses documented by 12 peer-review papers. My background includes significant computational work, demonstrated by my successful development of the preliminary data using R programming language and computational virology tools. Critically, my forthcoming work from Washington University, involved computational virology analysis of the s2m motif (a highly conserved RNA element in RNA viruses), proving my competence in dissecting evolutionary constraints on viral RNA structures. I am proficient in Large-Data Analysis and Workflow Automation, skills directly applicable to leading this project. Additionally, this project perfectly aligns with goals of the Diako lab at Texas Biomedical Research Instiitute, where Dr. Ebrahimi leads a group of scientists investigating HIV-host interactions. This proposed research, by identifying the structural constraints dictating viral subtype evolution, provides a crucial, quantitative viral-side component to the Diako lab's existing focus on virus-host interaction mechanisms.

## References

1. Arslan, Nurhan, et al. "HIV multidrug class resistance prediction with a time sliding anchor approach." Bioinformatics Advances 5.1 (2025): vbaf099.
2. Levintov, Lev, and Harish Vashisth. "Structural and computational studies of HIV-1 RNA." RNA biology 21.1 (2024): 167-198.
3. Yang, Shu, et al. "Advances in RNA secondary structure prediction and RNA modifications: Methods, data, and applications." arXiv preprint arXiv:2501.04056 (2025).
4. Golden, Michael, et al. "Evolutionary analyses of base-pairing interactions in DNA and RNA secondary structures." Molecular Biology and Evolution 37.2 (2020): 576-592.
