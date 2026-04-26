* =============================================================================
* PAML codeml control file - Branch-site Model A (ALTERNATIVE)
* =============================================================================
* Purpose : Test for positive selection on pre-specified foreground branch
*           under the ALTERNATIVE hypothesis of positive selection
*           (omega_foreground >= 1, estimated freely).
* Method  : Yang & Nielsen 2002 / Zhang, Nielsen & Yang 2005 - branch-site
*           Model A with fix_omega=0. Posterior probabilities for site class 2a/2b
*           give Bayesian Empirical Bayes (BEB) scores for individual codons
*           under positive selection on the foreground branch.
*
* Usage   :
*   1. Run 00_codeml_model_a_null.ctl first, capture lnL_null.
*   2. Run this file, capture lnL_alt.
*   3. LRT statistic = 2 * (lnL_alt - lnL_null), df = 1.
*   4. p_raw = pchisq(LRT, df=1, lower.tail=FALSE) / 2
*      (half-chi-square; Anisimova & Yang 2007 MBE 24:1219-1228).
*   5. Report BEB posterior probabilities from rst file: codons with
*      P(site_class=2a|data) > 0.95 are candidate positive-selection sites.
*
* IMPORTANT: Re-run the alt with at least TWO initial omega values
*   (0.5 and 1.5) to guard against local optima. Retain the run with higher
*   lnL. The 02_run_branch_site.sh wrapper does this automatically.
*
* Differences vs NULL control file:
*   fix_omega = 0    (alt, freely estimated)
*   omega     = 1.5  (alt initial value)
*   - - - all other parameters IDENTICAL to null - - -
* =============================================================================

      seqfile = alignment.phy
     treefile = tree_labelled.nwk
      outfile = alt_mlc.out

        noisy = 3
      verbose = 1
      runmode = 0

      seqtype = 1
    CodonFreq = 2
        clock = 0
       aaDist = 0
        model = 2
      NSsites = 2
        icode = 0
    fix_kappa = 0
        kappa = 2
    fix_omega = 0       * === ALT: omega_foreground estimated freely ===
        omega = 1.5     * === ALT: initial value for omega_foreground ===
        getSE = 0
 RateAncestor = 1       * request BEB posterior probabilities (rst file)
   Small_Diff = 0.5e-6
    cleandata = 0
  fix_blength = 0
       method = 0
