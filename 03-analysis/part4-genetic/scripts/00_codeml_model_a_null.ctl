* =============================================================================
* PAML codeml control file - Branch-site Model A (NULL)
* =============================================================================
* Purpose : Test for positive selection on pre-specified foreground branch
*           under the NULL hypothesis of NO positive selection
*           (omega_foreground constrained to 1).
* Method  : Yang & Nielsen 2002 / Zhang, Nielsen & Yang 2005 - branch-site
*           Model A with fix_omega=1 and omega=1.
* Usage   : Run this null model, then run the ALT model
*           (00_codeml_model_a_alt.ctl), compute 2 * (lnL_alt - lnL_null),
*           compare to chi-square df=1, and halve the p-value (one-sided
*           test per Anisimova & Yang 2007 Mol Biol Evol 24:1219-1228).
*
* Inputs (substituted per-run by 01_prepare_codeml_inputs.py):
*   seqfile : codon alignment in Phylip / PAML-compatible FASTA
*   treefile: Newick tree with foreground branch labelled "#1"
*   outfile : text log written by codeml
*
* Notes:
*   - Keep identical model = 2 / NSsites = 2 between null and alt.
*   - The ONLY differences between this file and the ALT file are:
*       fix_omega = 1    (null)   vs   fix_omega = 0    (alt)
*       omega = 1        (null)   vs   omega = 1.5      (alt - init only)
*     All other flags must match.
*   - cleandata = 0 : do NOT remove gap/ambiguity columns (avoids discarding
*     informative sites that differ between lineages).
*   - CodonFreq = 2 : F3x4 (recommended for vertebrate & arthropod datasets,
*     balances realism and parameter count; sensitivity-check CodonFreq=7 in
*     a tagged subset if needed).
*   - Multiple initial values: run at least two init omega values in the ALT
*     model to protect against local optima.
* =============================================================================

      seqfile = alignment.phy
     treefile = tree_labelled.nwk
      outfile = null_mlc.out

        noisy = 3       * 0,1,2,3,9: how much rubbish on the screen
      verbose = 1       * 1: detailed output, 0: concise output
      runmode = 0       * 0: user tree

      seqtype = 1       * 1:codons; 2:AAs; 3:codons-->AAs
    CodonFreq = 2       * 0:1/61 each, 1:F1X4, 2:F3X4, 3:codon table
        clock = 0       * 0:no clock, 1:clock, 2:local clock
       aaDist = 0
        model = 2       * Branch-site Model A: 2 site classes with branch-specific omega
      NSsites = 2       * Required for branch-site Model A
        icode = 0       * 0: universal; 1: mammalian mt; etc.
    fix_kappa = 0
        kappa = 2       * initial or fixed kappa
    fix_omega = 1       * === NULL: omega_foreground FIXED at 1 ===
        omega = 1       * === NULL: omega_foreground = 1 ===
        getSE = 0
 RateAncestor = 0
   Small_Diff = 0.5e-6
    cleandata = 0       * keep alignment ambiguities / gaps
  fix_blength = 0       * 0: ignore branch lengths in input tree; 1: use as initial
       method = 0       * 0: simultaneous optimisation; 1: one branch at a time
