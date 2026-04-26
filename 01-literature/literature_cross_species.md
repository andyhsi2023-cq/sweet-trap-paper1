# Sweet Trap — Cross-Species Literature Map
**Stage:** 0γ  
**Compiled:** 2026-04-17  
**Scope:** Evolutionary biology × ecology × behavioral neuroscience × behavioral economics × evolutionary psychology × cross-species universality  
**Purpose:** Establish the literature base for repositioning Sweet Trap from Nat HB (multi-domain human behavior) to Nature main / Science (cross-species evolutionary universality of reward-fitness decoupling)

---

## Theoretical Frame: What This Literature Map Is For

Sweet Trap's new definition:
> **Ancestrally adaptive reward signal decoupled from current-environment fitness consequences, producing self-reinforcing welfare-reducing behavior at individual and group levels.**

This is not a behavioral economics paper with evolutionary garnish. It is an evolutionary biology paper with human-scale empirical evidence. The literature map must support:
1. The evolutionary necessity of ancestral reward calibration (why brains/behavior evolved reward signals at all)
2. The structural inevitability of mismatch when environments change faster than selection (why decoupling is predicted)
3. The cross-species instantiation of this decoupling (animals first, then humans)
4. The human-specific features that amplify and self-reinforce the trap (social endorsement, culture, institutions)
5. Welfare consequences at scale (why this matters beyond biology)

---

## Section 1: Evolutionary Biology Foundations

### 1.1 Sexual Selection and Runaway Dynamics

**Fisher, R. A. (1930).** *The Genetical Theory of Natural Selection.* Clarendon Press, Oxford.
- DOI: [VERIFY — book, no DOI]
- **Core contribution:** Runaway sexual selection — a preference-trait genetic correlation creates self-amplifying dynamics where female preference and male ornament co-evolve toward ever-greater excess, potentially beyond adaptive optimum. Fisher's fundamental theorem also establishes that natural selection maximizes mean fitness only in static environments.
- **Sweet Trap relation: PARENT.** Fisher runaway is the paradigm case of reward signal (female preference for ornamented males) that originally tracked fitness quality but becomes decoupled through coevolution. The hen's continued preference for peacock tails — even as the tail consumes metabolic resources — is the oldest documented sweet trap in the natural world. Sweet Trap generalizes this mechanism beyond sexual ornaments to all evolved preference signals.
- **Annotation:** The runaway dynamic is specifically a self-reinforcing equilibrium (ρ in our formal model). The female preference updates *toward* the chosen trait, locking in the equilibrium even when the trait is costly. This is formally identical to our lock-in condition.

**Zahavi, A. (1975).** Mate selection — a selection for a handicap. *Journal of Theoretical Biology*, 53(1), 205–214.
- DOI: 10.1016/0022-5193(75)90111-3
- **Core contribution:** Handicap principle — honest signaling requires costly signals precisely because cost prevents faking. The peacock tail is honest precisely because it is physiologically expensive.
- **Sweet Trap relation: COMPLEMENT.** Zahavi explains *why* costly reward signals are evolutionarily stable, not why they become decoupled in novel environments. Sweet Trap is the complement: once the environment changes so that the costly signal no longer correlates with fitness, the organism is paying the signal cost without the fitness benefit. This is reward-fitness decoupling from the receiver perspective.
- **Annotation:** Critical for the "endorsement" prong of Sweet Trap: individuals actively endorse the costly signal because it was historically associated with genuine quality. Epistemic access is absent to the decoupling.

**Grafen, A. (1990).** Biological signals as handicaps. *Journal of Theoretical Biology*, 144(4), 517–546.
- DOI: 10.1016/S0022-5193(05)80088-8
- **Core contribution:** Formal game-theoretic proof of Zahavi's handicap principle; shows costly signaling can be evolutionarily stable even without direct genetic correlations.
- **Sweet Trap relation: TECHNICAL FOUNDATION.** Grafen's signaling game formalizes the conditions under which reward signals are calibrated to fitness. Sweet Trap operates precisely when these conditions break down — i.e., when environment novelty severs the signal-quality correlation.
- **Annotation:** Used in our formal model (Section 3): the game-theoretic setup for why ancestral reward signals are calibrated, setting up the environmental change perturbation.

**Kokko, H., Brooks, R., McNamara, J. M., & Houston, A. I. (2002).** The sexual selection continuum. *Proceedings of the Royal Society B*, 269(1498), 1331–1340.
- DOI: 10.1098/rspb.2002.2019
- **Core contribution:** Unifies Fisher-Zahavi debate; shows both processes operate simultaneously on a continuum; empirically, most ornaments have both runaway and handicap components.
- **Sweet Trap relation: COMPLEMENT.** The unified view matters because it shows that virtually all evolved preference-trait systems involve reward signals (preference) calibrated by ancestral fitness associations, making the generalization of Sweet Trap broader: it applies wherever preferences were fitness-correlated.

### 1.2 Evolutionary Mismatch Theory

**Nesse, R. M., & Williams, G. C. (1994).** *Why We Get Sick: The New Science of Darwinian Medicine.* Times Books.
- DOI: [VERIFY — book]
- **Core contribution:** Foundational statement of evolutionary mismatch: human physiology and psychology were calibrated for Pleistocene environments; modern environments create mismatch diseases (obesity, anxiety, addiction). First systematic treatment of why ancestrally adaptive responses produce harm in modern contexts.
- **Sweet Trap relation: PARENT.** Mismatch theory is the direct intellectual parent of Sweet Trap. Our contribution is (a) formalizing the *reward signal* mechanism (not just "environment changed"), (b) extending to group and institutional lock-in (not just individual physiology), and (c) adding the endorsement feature — the organism *chooses* and *endorses* the mismatched stimulus.
- **Annotation:** Nesse-Williams describe the mismatch but not the self-reinforcing equilibrium. They predict *suffering*; they do not model *why organisms keep choosing the harmful stimulus*. That is our incremental contribution.

**Gluckman, P., & Hanson, M. (2006).** *Mismatch: Why Our World No Longer Fits Our Bodies.* Oxford University Press.
- DOI: [VERIFY — book]
- **Core contribution:** Developmental origins of mismatch; the developmental plasticity hypothesis — organisms calibrate their phenotype to early environmental cues, and when adult environments diverge, mismatch is amplified across generations.
- **Sweet Trap relation: COMPLEMENT.** Gluckman-Hanson add the developmental (λ) dimension: mismatch costs can be transferred across generations (intergenerational cost externalization, our λ mechanism). This supports Sweet Trap's λ-component in the 鸡娃 domain.

**Lieberman, D. E. (2013).** *The Story of the Human Body: Evolution, Health, and Disease.* Pantheon Books.
- DOI: [VERIFY — book]
- **Core contribution:** Comprehensive synthesis of evolutionary mismatch across human health domains (diet, exercise, posture, sleep, stress). Introduces concept of "dysevolution" — feedback loop where medical treatment of mismatch diseases sustains conditions that perpetuate them.
- **Sweet Trap relation: NEAR-PARALLEL.** Lieberman's "dysevolution" is structurally identical to Sweet Trap's self-reinforcing equilibrium — the treatment of symptoms perpetuates the underlying trap. His sugar/fat/salt preference mismatch argument is directly the dietary domain of Sweet Trap. Key difference: Lieberman describes mismatch as passive (bodies react) while Sweet Trap requires active endorsement (agents choose and justify).

### 1.3 Behavioral Ecology

**Krebs, J. R., & Davies, N. B. (Eds.) (1991).** *Behavioural Ecology: An Evolutionary Approach* (4th ed.). Blackwell Scientific Publications.
- DOI: [VERIFY — book]
- **Core contribution:** Standard framework for optimal foraging theory, life-history theory, and economic analysis of animal behavior. Establishes that animals behave as if maximizing fitness-related currencies.
- **Sweet Trap relation: BACKGROUND.** The optimal foraging framework is the baseline against which Sweet Trap is a *deviation*: Sweet Trap occurs when the currency being maximized (experienced reward) diverges from the currency that was evolutionarily calibrated (fitness). This is the formal setup for our evolutionary mismatch argument.

**Maynard Smith, J. (1982).** *Evolution and the Theory of Games.* Cambridge University Press.
- DOI: [VERIFY — book]
- **Core contribution:** Evolutionary stable strategies (ESS); proves that frequency-dependent selection can maintain stable behavioral equilibria even in sub-optimal states. Nash equilibrium applied to evolution.
- **Sweet Trap relation: FORMAL MODEL FOUNDATION.** The ESS framework underpins our formal model: Sweet Trap equilibria are evolutionary stable (no individual unilateral deviation is profitable) even when the collective outcome is welfare-reducing. The population-level lock-in (鸡娃 arms race, status consumption treadmill) is an ESS of a coordination game.

**Axelrod, R. (1984).** *The Evolution of Cooperation.* Basic Books.
- DOI: [VERIFY — book]
- **Core contribution:** Tit-for-tat as ESS in iterated prisoner's dilemma; cooperation evolves from selfish strategies; demonstrates that collectively suboptimal equilibria can persist.
- **Sweet Trap relation: COMPLEMENT.** Axelrod's evolutionary game theory shows how coordination games with individually rational but collectively suboptimal equilibria can be stable. Directly parallels our group-level Sweet Trap: 996 culture, 鸡娃 arms race, conspicuous consumption equilibria are each coordination game traps.

---

## Section 2: Ecological Trap / Evolutionary Trap Literature

This is the closest existing academic field to Sweet Trap. Critical to understand to position Sweet Trap as the *superordinate* concept.

**Schlaepfer, M. A., Runge, M. C., & Sherman, P. W. (2002).** Ecological and evolutionary traps. *Trends in Ecology & Evolution*, 17(10), 474–480.
- DOI: 10.1016/S0169-5347(02)02580-6
- **Core contribution:** Defines *ecological trap*: habitat where animals prefer to settle (high attractiveness cue) but fitness is lower than in other available habitats. Classic examples: sea turtle disorientation by artificial beach lights; birds attracted to roads (tar-paper = water surface cue). Distinguishes ecological traps from evolutionary traps (evolutionary adaptation to misread cues).
- **Sweet Trap relation: CHILD CONCEPT.** Ecological trap is Sweet Trap at the habitat-selection level. Our construct is broader: (1) Sweet Trap includes non-habitat domains (consumption, career, parenting); (2) Sweet Trap explicitly models the reward signal mechanism (not just "wrong cue"); (3) Sweet Trap includes the self-reinforcing equilibrium — ecological traps do not require lock-in.
- **Must cite.** Central positioning paper. We explicitly say Sweet Trap ⊃ Ecological Trap.

**Robertson, B. A., Rehage, J. S., & Sih, A. (2013).** Ecological novelty and the emergence of evolutionary traps. *Trends in Ecology & Evolution*, 28(9), 552–560.
- DOI: 10.1016/j.tree.2013.04.004
- **Core contribution:** Extends Schlaepfer 2002 to evolutionary timescale. When novel environments create mismatches faster than natural selection can respond, evolutionary traps emerge. Provides framework for when traps become permanent versus transient.
- **Sweet Trap relation: CHILD + KEY DIFFERENTIATOR.** Robertson et al. focus on *fitness* consequences of novel environments. Sweet Trap focuses on *reward signal* mechanism. Their evolutionary trap requires a novel stimulus that evolved attractiveness cues mistakenly respond to; Sweet Trap additionally requires (a) the agent endorses the choice epistemically and (b) the equilibrium self-reinforces via cultural/institutional mechanisms. This is the cleanest differentiator for our Nature submission.

**Sih, A., Ferrari, M. C. O., & Harris, D. J. (2011).** Evolution and behavioural responses to human-induced rapid environmental change. *Evolutionary Applications*, 4(2), 367–387.
- DOI: 10.1111/j.1752-4571.2010.00166.x
- **Core contribution:** HIREC (human-induced rapid environmental change) as evolutionary context; categorizes adaptive, maladaptive, and neutral responses to human-caused environmental change. Shows that many responses are maladaptive because change is too fast for evolutionary response.
- **Sweet Trap relation: COMPLEMENT.** HIREC framework explains *why* sweet traps exist historically (ancestral calibration + rapid environment change). It does not explain why agents *endorse* the maladaptive response or how self-reinforcing equilibria emerge. These are Sweet Trap's unique contributions.

**Swaddle, J. P., Francis, C. D., Barber, J. R., Cooper, C. B., Acevedo-Gutiérrez, A., et al. (2015).** A framework to assess evolutionary responses to anthropogenic light and sound. *Trends in Ecology & Evolution*, 30(2), 67–76.
- DOI: 10.1016/j.tree.2014.11.001
- **Core contribution:** Comprehensive framework for how anthropogenic sensory pollution (artificial light, noise) creates evolutionary traps; reviews evidence across >50 species; shows fitness consequences of sensory mismatch.
- **Sweet Trap relation: EMPIRICAL SUBSTRATE.** Provides the empirical catalog of non-human sweet traps. Light pollution → moth circling, sea turtle disorientation, bird window strikes. All involve ancestrally calibrated sensory reward signals (move toward light = ancestral moon navigation) decoupled from fitness in novel environment.

**Warrant, E. J., & Dacke, M. (2011).** Vision and visual navigation in nocturnal insects. *Annual Review of Entomology*, 56, 239–254.
- DOI: 10.1146/annurev-ento-120709-144852
- **Core contribution:** Mechanistic review of how moths and other nocturnal insects use moonlight for navigation; explains exactly why artificial lights create a fatal decoupling of the celestial navigation system.
- **Sweet Trap relation: MECHANISTIC CASE.** The moth-to-light example is the canonical cross-species sweet trap: (1) ancestrally adaptive reward signal (fly toward brightest light = navigate by moon); (2) novel environment (artificial light sources); (3) reward-fitness decoupling (flying toward lamp = burn or spiral to exhaustion); (4) no corrective feedback (the reward signal stays positive even as fitness goes to zero). This is our purest non-human example.

**Gjerde, I., & Blom, R. (2020).** Golden eagles caught in an agricultural trap: use of grasslands associated with high breeding failure. *Biological Conservation*, 243, 108466.
- DOI: 10.1016/j.biocon.2020.108466
- **Core contribution:** Documents golden eagles preferentially nesting in agricultural grasslands (high attractiveness as a nesting cue) but experiencing dramatically lower reproductive success than forest nesters. Classic agricultural evolutionary trap.
- **Sweet Trap relation: EMPIRICAL CASE.** Agricultural traps for raptors demonstrate that even cognitively sophisticated animals fall into Sweet Traps. The eagle "endorses" the grassland nesting site — it is not coerced — but the fitness consequence is negative. This is our animal-model instantiation for the "endorsement without epistemic access" feature.

**Schlaepfer, M. A., Sherman, P. W., Blossey, B., & Runge, M. C. (2005).** Introduced species as evolutionary traps. *Ecology Letters*, 8(3), 241–246.
- DOI: 10.1111/j.1461-0248.2005.00730.x
- **Core contribution:** Introduced (invasive) species as a major source of evolutionary traps; native species evolved no recognition of novel predators/competitors, making them easy prey.
- **Sweet Trap relation: CHILD CONCEPT + CASE STUDY.** Demonstrates that evolutionary traps are not random but follow predictable patterns: they emerge when novel stimuli mimic ancestral attractiveness cues without the associated fitness payoffs. Directly parallel to human sweet traps where novel goods/activities (social media, processed food, MLM) mimic ancestral reward signals (social connection, caloric density, coalition building) without delivering the associated fitness.

**Bauer, C. M., & Sih, A. (2020).** Evolutionary traps in changing environments. *Current Biology*, 30(23), R1430–R1435.
- DOI: 10.1016/j.cub.2020.10.021 [VERIFY]
- **Core contribution:** Reviews current state of evolutionary trap research; identifies key open questions including what prevents evolutionary escape from traps.
- **Sweet Trap relation: REVIEW ANCHOR.** Demonstrates that the evolutionary trap literature has not solved the question of self-reinforcing equilibria. This is our entry point: Sweet Trap adds (a) the endorsement mechanism, (b) the group-level lock-in via culture/institutions, (c) the cross-domain universality claim that the trap literature has not made.

**Corpus hit — CRITICAL: Lethal trap created by adaptive evolutionary response to an exotic resource.** *Nature* 2018. DOI: 10.1038/s41586-018-0074-6 (cites=102).
- **Core contribution:** Empirical Nature paper showing that an adaptive evolutionary response to an exotic (invasive) plant resource created a lethal trap for a native insect population. This is the only Nature main paper in our corpus directly documenting an evolutionary trap in a non-human species.
- **Sweet Trap relation: BENCHMARK.** This is the paper we need to supersede in scope. It shows one species × one novel resource = one trap. Sweet Trap claims: multiple species × multiple novel environments = one universal mechanism. This comparison makes our scope claim concrete.

---

## Section 3: Behavioral Neuroscience / Reward System

**Olds, J., & Milner, P. (1954).** Positive reinforcement produced by electrical stimulation of septal area and other regions of rat brain. *Journal of Comparative and Physiological Psychology*, 47(6), 419–427.
- DOI: 10.1037/h0058775
- **Core contribution:** Discovery of brain stimulation reward (intracranial self-stimulation, ICSS). Rats pressed levers to self-stimulate reward circuits to the exclusion of eating, drinking, and sex — the first laboratory demonstration that reward circuits can be decoupled from fitness.
- **Sweet Trap relation: FOUNDING EMPIRICAL CASE.** Olds-Milner is the first experimental demonstration that reward and fitness can be decoupled in a mammal. It is the neuroscience origin story of Sweet Trap: the rat's reward system was adapted to signal proximity to food/reproduction, but direct stimulation bypasses the fitness signal entirely. The rat endorses self-stimulation fully — no coercion, no deception from the rat's perspective.
- **Must cite.** Page 1 candidate.

**Berridge, K. C., & Robinson, T. E. (1998).** What is the role of dopamine in reward: hedonic impact, reward learning, or incentive salience? *Brain Research Reviews*, 28(3), 309–369.
- DOI: 10.1016/S0165-0173(98)00019-8
- **Core contribution:** Distinguishes "wanting" (incentive salience, dopamine-driven) from "liking" (hedonic impact, opioid-driven). Wanting and liking can dissociate: addiction involves pathological wanting without increased liking. This is the neural mechanism of the endorsement-without-payoff pattern.
- **Sweet Trap relation: MECHANISM.** Berridge-Robinson provides the neural substrate of Sweet Trap's "endorsement without epistemic access": the wanting system (dopamine) produces behavioral endorsement (lever pressing, consumption) while the liking system reports diminishing returns. The decoupling of wanting from liking is the neural-level instantiation of reward-fitness decoupling.

**Volkow, N. D., Koob, G. F., & McLellan, A. T. (2016).** Neurobiologic advances from the brain disease model of addiction. *New England Journal of Medicine*, 374(4), 363–371.
- DOI: 10.1056/NEJMra1511480
- **Core contribution:** Reviews how addiction hijacks the mesolimbic dopamine system; shows that repeated reward signal activation produces progressive reward system dysregulation; documents the neural bases of compulsive use despite adverse consequences.
- **Sweet Trap relation: MECHANISM + HUMAN CASE.** Addiction is Sweet Trap at its most extreme — the reward-fitness decoupling is total (drug reward signal vs. all fitness consequences). Volkow et al. provide the mechanistic model. For our paper: addiction is a special case of Sweet Trap, not the general phenomenon. We generalize beyond addiction to socially endorsed sweet traps (鸡娃, 996) where the decoupling is less extreme but operates at larger population scale.

**Corpus hit: Dopaminergic systems create reward seeking despite adverse consequences.** *Nature* 2023. DOI: 10.1038/s41586-023-06671-8 (cites=24).
- **Core contribution:** Demonstrates in rodents that dopaminergic circuits specifically drive reward-seeking behavior even when adverse consequences are experienced, through a mechanism distinct from reward learning circuits.
- **Sweet Trap relation: DIRECT NEURAL MECHANISM.** This Nature paper is the most recent and precise neural evidence for reward-fitness decoupling at the neural circuit level. The adverse-consequence-despite-consequences finding exactly matches Sweet Trap's "absence of corrective feedback" feature (D4 in our formal model). Must cite as neural mechanism evidence.

**McClure, S. M., Laibson, D. I., Loewenstein, G., & Cohen, J. D. (2004).** Separate neural systems value immediate and delayed monetary rewards. *Science*, 306(5695), 503–505.
- DOI: 10.1126/science.1100907
- **Core contribution:** Two-system model of intertemporal choice: limbic (dopaminergic) regions respond preferentially to immediate rewards; prefrontal systems evaluate both immediate and delayed rewards. This is the neural basis of hyperbolic discounting.
- **Sweet Trap relation: MECHANISM (β parameter).** McClure et al. provide the neural substrate of our β parameter (present bias/quasi-hyperbolic discounting). The limbic system's exaggerated weighting of immediate rewards (evolved for immediate fitness cues) is the neural mechanism of the temporal mismatch component of Sweet Trap.

**Kable, J. W., & Glimcher, P. W. (2007).** The neural correlates of subjective value during intertemporal choice. *Nature Neuroscience*, 10(12), 1625–1633.
- DOI: 10.1038/nn2007
- **Core contribution:** Identifies specific brain regions (posterior parietal cortex, medial prefrontal cortex, posterior cingulate) encoding subjective discounted value during intertemporal choice; supports hyperbolic rather than exponential discounting as descriptively accurate.
- **Sweet Trap relation: COMPLEMENT.** The neural valuation architecture implements hyperbolic discounting (β in our model) as the *baseline* biological temporal preference, not an anomaly. This supports our evolutionary argument: present-biased discounting is not a bias but an evolved default calibrated to ancestral environments with high mortality risk and immediate scarcity.

---

## Section 4: Behavioral Economics and Decision Science

**Kahneman, D., & Tversky, A. (1979).** Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263–291.
- DOI: 10.2307/1914185
- **Core contribution:** Reference-dependent value function; loss aversion; probability weighting. Foundational framework for departures from expected utility maximization.
- **Sweet Trap relation: ADJACENT — PARTIAL OVERLAP.** Prospect theory describes *how* choices deviate from rationality. Sweet Trap is about *why* a specific class of choices (reward-endorsed, fitness-reducing) is evolutionarily stable. Our unique contribution: Sweet Trap is not a bias but an equilibrium — agents may be fully "rational" in the prospect-theory sense and still be in a Sweet Trap. We do not require biased decision-making; we require reward-fitness decoupling.

**Laibson, D. (1997).** Golden eggs and hyperbolic discounting. *Quarterly Journal of Economics*, 112(2), 443–477.
- DOI: 10.1162/003355397555253
- **Core contribution:** Formal β-δ quasi-hyperbolic discounting model with commitment device implications; shows that present-biased agents have structured time-inconsistent preferences and demand commitment devices.
- **Sweet Trap relation: COMPONENT.** Laibson's β is our β parameter. Hyperbolic discounting is the temporal dimension of Sweet Trap: immediate reward (period 1) is over-weighted relative to long-run fitness consequences. Our contribution over Laibson: (a) evolutionary origin of β (ancestral calibration), (b) cross-species instantiation, (c) the ρ lock-in mechanism that Laibson does not model.

**O'Donoghue, T., & Rabin, M. (2001).** Choice and procrastination. *Quarterly Journal of Economics*, 116(1), 121–160.
- DOI: 10.1162/003355301556365
- **Core contribution:** Sophisticated hyperbolic discounters who are aware of their time inconsistency can be worse off than naive agents under some conditions; the awareness × temptation interaction. Self-control with commitment.
- **Sweet Trap relation: COMPLEMENT.** O'Donoghue-Rabin address the self-control aspect (β) of our model. Their sophisticated/naive distinction maps onto our "endorsement without epistemic access": Sweet Trap agents are *naive* in the specific sense that they lack access to the evolutionary decoupling information, not that they are generally irrational.

**Bernheim, B. D., & Taubinsky, D. (2018).** Behavioral public economics. *Handbook of Public Economics*, 5, 381–516.
- DOI: 10.1016/bs.hpubec.2018.09.002
- **Core contribution:** Framework for optimal policy when agents have internalities (costs/benefits they impose on their future selves that they do not account for). Distinguishes internalities from externalities; provides welfare analysis tools.
- **Sweet Trap relation: ADJACENT — DISTINGUISHED.** Sweet Trap is a specific class of internality-generating equilibrium where the internality arises from evolutionary reward-fitness decoupling rather than cognitive limitations. Our formal differentiator: in Bernheim-Taubinsky, the internality is a behavioral anomaly (bias). In Sweet Trap, it is an evolutionarily calibrated preference response in a novel environment. The welfare implications are similar but the mechanism and intervention logic differ.

**Allcott, H., Braghieri, L., Eichmeyer, S., & Gentzkow, M. (2020).** The welfare effects of social media. *Quarterly Journal of Economics*, 135(1), 211–264.
- DOI: 10.1093/qje/qjz042
- **Core contribution:** RCT deactivating Facebook: deactivation increases subjective wellbeing while reducing political knowledge and polarization; shows social media use involves internalities. Quantifies welfare loss.
- **Sweet Trap relation: DOMAIN EVIDENCE + COMPETITOR.** Allcott et al. document the Sweet Trap pattern for social media: users endorse the platform, but wellbeing declines with use. This is our Domain 7 evidence (though we dropped D7 in Stage 0). Key difference: their mechanism is "time cost + addiction" (behavioral); our mechanism is "ancestrally adapted social reward circuits hijacked by supernormal social stimuli" (evolutionary). The evolutionary framing changes the intervention logic and generalizability.

**Braghieri, L., Levy, R., & Makarin, A. (2022).** Social media and mental health. *American Economic Review*, 112(11), 3660–3693.
- DOI: 10.1257/aer.20211218
- **Core contribution:** Facebook rollout natural experiment across US college campuses: quasi-experimental identification showing Facebook adoption increased depression and anxiety. Largest causal estimate to date for social media mental health effects.
- **Sweet Trap relation: DOMAIN EVIDENCE.** Braghieri et al. provide the gold-standard causal identification for social media Sweet Trap. Their natural experiment is methodologically the closest existing work to our identification strategy. Key asymmetry: they study adoption (did Facebook cause harm?); Sweet Trap asks why students voluntarily adopted and endorsed Facebook despite harm.

**Thaler, R. H., & Sunstein, C. R. (2008).** *Nudge: Improving Decisions about Health, Wealth, and Happiness.* Yale University Press.
- DOI: [VERIFY — book]
- **Core contribution:** Libertarian paternalism; default effects; choice architecture as behavioral policy tool.
- **Sweet Trap relation: ADJACENT — DIFFERENT LEVEL.** Nudge operates at the choice architecture level (change defaults, framing). Sweet Trap is an equilibrium phenomenon that is *resistant* to nudges precisely because the reward signal continues to override the nudged choice — agents re-endorse the Sweet Trap even after nudges. This is an important policy differentiator: Sweet Trap predicts nudge failure in high-reward-signal domains.

**Heiner, R. A. (1983).** The origin of predictable behavior. *American Economic Review*, 73(4), 560–595.
- DOI: [VERIFY]
- **Core contribution:** Behavioral regularities arise from the gap between agent competence and decision complexity (C-D gap); simple rules are optimal when agents cannot reliably evaluate all options.
- **Sweet Trap relation: COMPLEMENT.** Heiner's C-D gap explains why agents cannot exit Sweet Traps through information alone: the complexity of evaluating long-run fitness consequences (evolutionary timescale) exceeds behavioral cognitive competence. This is a rationalization for the "absence of epistemic access" feature of Sweet Trap.

**Frank, R. H. (1999).** *Luxury Fever: Why Money Fails to Satisfy in an Era of Excess.* Free Press.
- DOI: [VERIFY — book]
- **Core contribution:** Positional externalities in consumption; spending arms race where increasing income leads to proportional increases in aspirational spending without welfare gains. Aggregate utility neutral or negative despite individual rationality.
- **Sweet Trap relation: CHILD CONCEPT.** Frank's luxury fever is Sweet Trap in the consumption domain: individually rational positional spending creates a collectively sub-optimal arms race (our ρ lock-in mechanism). Sweet Trap generalizes this: the arms race is not just about positional goods but any domain where ancestral reward signals are exploited.

**Heffetz, O. (2011).** A test of conspicuous consumption: Visibility and income elasticities. *Review of Economics and Statistics*, 93(4), 1101–1117.
- DOI: 10.1162/REST_a_00116
- **Core contribution:** Develops a visibility index for consumption goods; higher visibility predicts higher income elasticity, consistent with conspicuous consumption theory. Empirically validates Veblen goods.
- **Sweet Trap relation: DOMAIN EVIDENCE.** Provides empirical infrastructure for measuring the θ (amenity) component of Sweet Trap in the consumption domain: visible goods signal status (ancestrally, coalition membership and resource quality) — the original adaptive function. Sweet Trap: visibility signal hijacked by goods that deliver social recognition without the underlying fitness correlates.

---

## Section 5: Evolutionary Psychology

**Cosmides, L., & Tooby, J. (1992).** The psychological foundations of culture. In J. H. Barkow, L. Cosmides, & J. Tooby (Eds.), *The Adapted Mind: Evolutionary Psychology and the Generation of Culture* (pp. 19–136). Oxford University Press.
- DOI: [VERIFY — book chapter]
- **Core contribution:** Massive modularity thesis; the mind consists of evolved domain-specific computational modules calibrated for ancestral environments. The Standard Social Science Model (culture creates psychology) is inverted: evolved psychology creates culture.
- **Sweet Trap relation: THEORETICAL FOUNDATION.** Cosmides-Tooby provide the mechanistic basis for why reward signals are *domain-specific and ancestrally calibrated*. Each module was calibrated in a specific ancestral domain; Sweet Traps arise when novel stimuli activate ancestral modules out of context (e.g., social media activates the social coalition-monitoring module; processed food activates the caloric-density seeking module).

**Buss, D. M. (1989).** Sex differences in human mate preferences: Evolutionary hypotheses tested in 37 cultures. *Behavioral and Brain Sciences*, 12(1), 1–14.
- DOI: 10.1017/S0140525X00023992
- **Core contribution:** Cross-cultural universality (37 societies) of sex-differentiated mate preferences; women prefer resource-acquiring ability, men prefer fertility cues. Interpreted as evolved mate choice modules.
- **Sweet Trap relation: DOMAIN EVIDENCE + CROSS-CULTURAL UNIVERSALITY.** Buss provides the cross-cultural universality argument for evolved preferences. For Sweet Trap: the universality of mate preferences means that when novel environments (e.g., extreme brideprice inflation, social media-mediated mate assessment) trigger these evolved modules with decoupled fitness consequences, the Sweet Trap should also be universal. Buss's 37-culture evidence supports our cross-cultural claim.

**Henrich, J. (2015).** *The Secret of Our Success: How Culture Is Driving Human Evolution, Domesticating Our Species, and Making Us Smarter.* Princeton University Press.
- DOI: [VERIFY — book]
- **Core contribution:** Gene-culture coevolution; cumulative culture as evolutionary driver; cultural learning heuristics (prestige bias, success bias, conformist bias) as evolved psychological mechanisms. Human evolutionary success depends on cultural transmission, not individual intelligence.
- **Sweet Trap relation: AMPLIFICATION MECHANISM.** Henrich's cultural learning mechanisms explain why Sweet Traps self-reinforce at the cultural level: prestige bias causes individuals to copy the most successful (high status) individuals' behaviors, even when those behaviors involve Sweet Traps. If high-status individuals engage in 996 or conspicuous consumption, conformist bias spreads the behavior. This is our ρ lock-in mechanism at the cultural level.

**Tooby, J., & Cosmides, L. (1996).** Friendship and the Banker's Paradox: Other pathways to the evolution of adaptations for altruism. *Proceedings of the British Academy*, 88, 119–143.
- DOI: [VERIFY]
- **Core contribution:** Evolutionary analysis of deep social relationships; the "banker's paradox" — rational banking won't lend to those most in need, just as the social reward system won't activate for desperate individuals without track record.
- **Sweet Trap relation: COMPLEMENT.** Relevant for the status signaling domain: social rewards (approval, belonging) activate the social bonding module. Sweet Trap in social domains (brideprice, luxury, 996 overwork for career) hijacks the social reward system.

**Barkow, J. H. (1989).** *Darwin, Sex, and Status: Biological Approaches to Mind and Culture.* University of Toronto Press.
- DOI: [VERIFY — book]
- **Core contribution:** Status as the fundamental currency of human evolution; social status tracks ancestral fitness; evolved psychology orients toward status acquisition across all domains.
- **Sweet Trap relation: THEORETICAL FOUNDATION.** Barkow provides the evolutionary account of why status-signaling behaviors are so powerful as trap mechanisms: status-seeking is not a bias but an evolved motivation calibrated to ancestral fitness. Sweet Trap operates in any domain where novel stimuli exploit the status-tracking module (conspicuous consumption, brideprice inflation, academic arms race).

---

## Section 6: Human-Specific Phenomena — Empirical Evidence

### 6.1 鸡娃 (Intensive Parenting / Shadow Education)

**Fong, V. L. (2004).** *Only Hope: Coming of Age Under China's One-Child Policy.* Stanford University Press.
- DOI: [VERIFY — book]
- **Core contribution:** Ethnographic account of Chinese one-child households; parents invest intensively in single child's education as the only vehicle for family upward mobility; parental identity fused with child success.
- **Sweet Trap annotation:** Provides the endorsement pattern — parents are intensely committed to the investment — and the mechanism (θ: parental status + λ: intergenerational cost transfer to child through pressure). Does not quantify welfare paradox. Our CFPS analysis operationalizes what Fong documents ethnographically.

**Xie, Y., & Zhou, X. (2014).** Income inequality in today's China. *Proceedings of the National Academy of Sciences*, 111(19), 6928–6933.
- DOI: 10.1073/pnas.1403158111
- **Core contribution:** China's income inequality surpasses US by standard Gini measures; documents growing positional competition pressure.
- **Sweet Trap annotation:** Provides the structural driver for 鸡娃 Sweet Trap intensity: high inequality → high returns to marginal position → arms race in parental investment → all are worse off but no unilateral exit.

### 6.2 彩礼 (Bride Price / Marriage Payments)

**Anderson, S. (2007).** The economics of dowry and brideprice. *Journal of Economic Perspectives*, 21(4), 151–174.
- DOI: 10.1257/jep.21.4.151
- **Core contribution:** Comprehensive review of dowry and brideprice economics across cultures; shows that marriage payments can serve as equilibrium mechanisms for match quality signals, but when competitive dynamics inflate payments, welfare losses emerge.
- **Sweet Trap annotation:** Anderson's competitive dynamics section is directly Sweet Trap: individual families escalate brideprice to signal son quality (status × marriage market), creating an arms race where aggregate welfare declines. The key mechanism: the status-signal reward (高门槛婚姻 = 高质量) is ancestrally calibrated, but in modern environments with sex ratio imbalances and parental over-investment in sons, the signal becomes decoupled from actual quality.

**Wei, S.-J., & Zhang, X. (2011).** The competitive saving motive: Evidence from rising sex ratios and savings rates in China. *Journal of Political Economy*, 119(3), 511–564.
- DOI: 10.1086/660887
- **Core contribution:** Exogenous sex ratio variation (preference for male births under one-child policy) → intensified mating competition → elevated household savings rates as competitive marriage resource accumulation.
- **Sweet Trap annotation:** Wei-Zhang document the aggregate welfare loss from mating competition arms race: elevated savings rates are individually rational but socially suboptimal. This is the classic Sweet Trap at the macro level: rational individual responses to an evolved status signal (resource acquisition for mate competition) creating an evolutionarily stable but collectively harmful equilibrium.

### 6.3 Diet and Metabolic Mismatch

**Corpus hit: Gut-brain circuits for fat preference.** *Nature* 2022. DOI: 10.1038/s41586-022-05266-z (cites=153).
- **Core contribution:** Demonstrates that gut-brain signaling circuits independently drive fat preference at the neural level, independent of conscious taste preferences — showing that dietary fat preference has a deep evolved circuit basis.
- **Sweet Trap annotation:** This Nature paper is the mechanistic foundation for dietary Sweet Trap: the fat preference circuit was calibrated for high-scarcity ancestral environments where fat was rare and calorically valuable. In modern environments with abundant processed fat, the same circuit drives overconsumption. Reward-fitness decoupling at the neural gut-brain level.

**Popkin, B. M., Adair, L. S., & Ng, S. W. (2012).** Global nutrition transition and the pandemic of obesity in developing countries. *Nutrition Reviews*, 70(1), 3–21.
- DOI: 10.1111/j.1753-4887.2011.00456.x
- **Core contribution:** Documents the global nutrition transition: as countries develop economically, traditional diets are replaced by high-fat, high-sugar ultra-processed foods; obesity and metabolic disease follow. Epidemiological characterization of dietary mismatch at population scale.
- **Sweet Trap annotation:** Nutrition transition is Sweet Trap at civilizational scale: the reward signals for caloric density (sugar, fat, salt) were fitness-calibrated in scarcity environments; economic development creates novel food environments where these signals are hijacked. The transition happens rapidly (1-2 generations) — too fast for evolutionary response. Popkin et al. document the Consequence chain in our PMC framework.

### 6.4 Social Media

**Orben, A., & Przybylski, A. K. (2019).** The association between adolescent well-being and digital technology use. *Nature Human Behaviour*, 3(2), 173–182.
- DOI: 10.1038/s41562-018-0506-1
- **Core contribution:** Specification curve analysis across multiple datasets and operationalizations; digital technology-wellbeing association is small and highly variable (effect size comparable to wearing glasses or eating potatoes). Challenges simple causal narratives.
- **Sweet Trap annotation:** Orben-Przybylski is the strongest challenge to social media as Sweet Trap: if the effect is small and inconsistent, the harm is insufficient for a "trap." Our response: Sweet Trap is defined by endorsement paradox, not merely harm — even if digital technology has small average effects, the *voluntary self-reinforcing endorsement* pattern in the presence of any negative signal is the phenomenon of interest. Additionally, Braghieri et al. 2022 using causal identification finds larger effects than Orben's correlational specification curve.

### 6.5 Career Overwork (996)

**Kivimäki, M., et al. (2015).** Long working hours and risk of coronary heart disease and stroke: A systematic review and meta-analysis of published and unpublished data for 603,838 individuals. *The Lancet*, 386(10005), 1739–1746.
- DOI: 10.1016/S0140-6736(15)60295-1
- **Core contribution:** N=600,000+ meta-analysis; dose-response relationship between long working hours and CVD/stroke risk; 10% increase in CVD risk at >55 hours/week vs. standard hours.
- **Sweet Trap annotation:** Kivimäki et al. document the harm side at population scale. For Sweet Trap: the career satisfaction / promotion reward (sweet side) is documented in Goldin 2014 (see below). Together, these provide the endorsement-harm paradox at macro scale. The mechanism: career advancement reward signals (social status, income, promotion) are ancestrally calibrated to coalition hierarchy. Working longer hours activates this reward system even when health consequences are negative.

**Goldin, C. (2014).** A grand gender convergence: Its last chapter. *American Economic Review*, 104(4), 1091–1119.
- DOI: 10.1257/aer.104.4.1091
- **Core contribution:** "Greedy jobs" hypothesis: nonlinear pay structure where long hours are rewarded disproportionately (superlinear returns to time); explains gender gap in wages through differential hours not discrimination.
- **Sweet Trap annotation:** Goldin documents the sweet side of 996 Sweet Trap: superlinear income returns to overwork make the choice individually rational (higher pay + career advancement). This is the θ parameter: immediate career reward. The λ = health + family externalization; β = present-biased over-weighting of immediate income gain.

---

## Section 7: Cross-Species Universality — Nature/Science Benchmarks

These papers establish the genre of "same mechanism across species" in Nature/Science.

**Corpus hit: Local convergence of behavior across species.** *Science* 2021. DOI: 10.1126/science.abb7481 (cites=106).
- **Core contribution:** Documents convergent behavioral strategies across ecologically distinct species using large-scale tracking data; shows that despite phylogenetic distance, shared environmental pressures produce similar behavioral solutions.
- **Sweet Trap relevance: METHOD BENCHMARK.** The "convergence across species" framework is exactly the genre we need. Their method: large-scale data across species → document behavioral convergence → claim universal mechanism. Our analogous structure: cross-species review of reward-fitness decoupling → human empirical instantiation → claim universal mechanism.

**Corpus hit: Humans share acoustic preferences with other animals.** *Science* 2026. DOI: 10.1126/science.aea1202 (cites=1).
- **Core contribution:** Cross-species study showing humans and non-human animals share specific acoustic preferences rooted in shared evolutionary history; uses comparative psychoacoustics.
- **Sweet Trap relevance: GENRE BENCHMARK.** Published in Science 2026. Demonstrates that the "cross-species universal preference" genre remains publishable in top journals in 2025-2026. Directly supports our framing: shared reward signals across species (acoustic preferences, visual preferences, social rewards) are the substrate from which Sweet Traps arise.

**Corpus hit: Conserved brain-wide emergence of emotional response from sensory experience in humans and mice.** *Science* 2025. DOI: 10.1126/science.adt3971 (cites=18).
- **Core contribution:** Large-scale whole-brain imaging across humans and mice; shows that emotional response patterns to sensory stimuli are conserved across species, mediated by homologous brain circuits.
- **Sweet Trap relevance: NEURAL MECHANISM CROSS-SPECIES.** Demonstrates that reward/emotional circuits are conserved across mammals. This is the neural-level evidence that the Sweet Trap's reward signal mechanism is cross-species: if emotional processing is conserved, then the decoupling of reward from fitness in novel environments should produce Sweet Trap patterns in all species with these circuits.

**Corpus hit: Cultural flies — Conformist social learning in fruitflies predicts long-lasting mate-choice tradition.** *Science* 2018. DOI: 10.1126/science.aat1590 (cites=223).
- **Core contribution:** Drosophila melanogaster display cultural transmission of mate choice preferences through conformist social learning — previously thought unique to humans and some vertebrates.
- **Sweet Trap relevance: CULTURAL LOCK-IN IS CROSS-SPECIES.** The ρ (lock-in) mechanism of Sweet Trap — cultural self-reinforcement — extends even to invertebrates. Conformist learning in fruit flies means that once a preference is established in a population, it self-reinforces regardless of its current fitness value. This extends Sweet Trap's scope claim dramatically.

**Corpus hit: Why reciprocity is common in humans but rare in other animals.** *Nature* 2024. DOI: 10.1038/d41586-024-00308-0 (cites=3).
- **Core contribution:** Reviews cross-species evidence on reciprocity; argues that human reciprocity is unusually prevalent because of unique cognitive and social features.
- **Sweet Trap relevance: BOUNDARY CONDITION.** This paper helps define where Sweet Trap is more vs. less intense across species: species with greater cultural transmission capacity (humans, great apes, corvids) will show stronger self-reinforcing Sweet Traps because cultural learning amplifies the lock-in.

**Corpus hit: Irrationality in mate choice revealed by túngara frogs.** *Science* 2015. DOI: 10.1126/science.aab2012 (cites=127).
- **Core contribution:** Demonstrates "irrational" choice behavior (context effects, decoy effects) in túngara frogs' mate selection — showing that systematic choice anomalies previously thought human-specific occur in amphibians.
- **Sweet Trap relevance: IRRATIONAL-LOOKING CHOICE IS CROSS-SPECIES.** This Science paper provides strong evidence that the systematic departures from utility maximization that behavioral economics documents in humans also occur in distant taxa. For Sweet Trap: if frogs show decoy effects, then the endorsement of suboptimal choices by evolved reward systems is a cross-species phenomenon, not a human cognitive quirk.

**Corpus hit: Female preference for rare males maintained by indirect selection in Trinidadian guppies.** *Science* 2023. DOI: 10.1126/science.ade5671 (cites=22).
- **Core contribution:** Shows that female mate preference for rare male coloration in guppies is maintained by indirect selection (genetic benefits) even when direct survival costs are present.
- **Sweet Trap relevance: REWARD-FITNESS TRADEOFF IN WILD POPULATIONS.** Directly documents the reward-fitness tradeoff in a wild population: females pay a cost (choosing rare males in novel color environments) because the ancestral preference for rare coloration was fitness-calibrated. In novel environments (changed predator pressure, introduced invasives), this preference becomes partially decoupled from fitness. Sweet Trap in a vertebrate.

---

## Section 8: Target Journal Benchmarks — Nature main / Science Recent Cross-Species Papers

**[B1] Corpus hit: Lethal trap created by adaptive evolutionary response to an exotic resource.** *Nature* 2018. DOI: 10.1038/s41586-018-0074-6 (cites=102).
- **Paper type:** Experimental/observational; one species × one novel resource → evolutionary trap.
- **Sweet Trap match:** Direct conceptual predecessor. Shows Nature publishes evolutionary trap papers. Our scope: multiple species × multiple domains × formal mechanism model × human empirical validation.

**[B2] Corpus hit: Dopaminergic systems create reward seeking despite adverse consequences.** *Nature* 2023. DOI: 10.1038/s41586-023-06671-8 (cites=24).
- **Paper type:** Mechanistic neuroscience in rodent model; identifies specific neural circuit for adverse-consequence reward seeking.
- **Sweet Trap match:** Provides neural mechanism for one component of Sweet Trap. Our contribution: generalize from neural mechanism (single species) to evolutionary mechanism (cross-species) and human welfare consequences.

**[B3] Corpus hit: Local convergence of behavior across species.** *Science* 2021. DOI: 10.1126/science.abb7481 (cites=106).
- **Paper type:** Comparative behavioral ecology using large-scale tracking data; demonstrates convergent behavioral solutions across distant taxa.
- **Sweet Trap match:** Genre template. We use analogous structure: cross-species convergence of reward-fitness decoupling phenomenon.

**[B4] Corpus hit: Conserved brain-wide emergence of emotional response in humans and mice.** *Science* 2025. DOI: 10.1126/science.adt3971 (cites=18).
- **Paper type:** Large-scale neuroimaging with human-rodent comparison; shows conservation of emotional circuitry.
- **Sweet Trap match:** Neural conservation argument supports our cross-species mechanism claim.

**[B5] Corpus hit: Humans share acoustic preferences with other animals.** *Science* 2026. DOI: 10.1126/science.aea1202 (cites=1).
- **Paper type:** Comparative psychoacoustics; demonstrates shared evolved preferences across phylogenetically distant species.
- **Sweet Trap match:** Most recent (2026) example of "shared evolved preference" genre in Science. Confirms the genre remains publishable. Our parallel: shared evolved reward signals (status, caloric density, social connection) across species → Sweet Trap when those signals decouple from fitness.

**[B6] Corpus hit: Cultural flies — Conformist social learning in fruitflies.** *Science* 2018. DOI: 10.1126/science.aat1590 (cites=223).
- **Paper type:** Behavioral experiment demonstrating cultural transmission in invertebrates.
- **Sweet Trap match:** Establishes that our ρ (cultural lock-in) mechanism operates even in invertebrates, supporting the universality of our self-reinforcing equilibrium claim.

**[B7] Corpus hit: Reducing nighttime light exposure to benefit human health.** *Science* 2023. DOI: 10.1126/science.adg5277 (cites=128).
- **Paper type:** Policy-relevant review on anthropogenic light pollution consequences across species and humans.
- **Sweet Trap match:** Documents that the same stimulus (artificial light) creates Sweet Traps across species (moths, sea turtles, birds, humans' circadian disruption) — a multidomain, multi-species example of exactly the pattern we claim.

---

## Sweet Trap Construct Differentiation Table

| Construct | Level | Mechanism | Self-reinforcing? | Endorsement required? | Formal model? | Scope |
|---|---|---|---|---|---|---|
| **Ecological trap** (Schlaepfer 2002) | Habitat choice | Wrong attractiveness cue | No | Behavioral only | No formal model | Single species, single habitat |
| **Evolutionary trap** (Robertson 2013) | Habitat + evolutionary timescale | Novel env faster than selection | Partial | Not modeled | No formal model | Cross-species, single domain |
| **HIREC maladaptation** (Sih 2011) | Behavior + evolutionary | Rapid human-caused change | No | Not modeled | No | Cross-species, multiple domains |
| **Mismatch theory** (Nesse 1994, Lieberman 2013) | Physiology + behavior | Ancestral calibration × modern env | No formal model | Not modeled | No | Humans only, multiple domains |
| **Behavioral addiction** (Volkow 2016) | Neural + behavior | Dopamine hijacking | Yes | Implicit | Partially | Humans + rodents, single domain |
| **Prospect theory / internality** (Kahneman; Bernheim) | Decision | Cognitive bias | No | Not applicable | Yes | Humans, domain-general |
| **Runaway selection** (Fisher 1930) | Evolutionary | Preference-trait coevolution | Yes | Implicit | Yes (genetic model) | Cross-species, mate choice only |
| **SWEET TRAP** (this paper) | Decision + evolutionary + neural + cultural | Reward-fitness decoupling + endorsement + lock-in | Yes (formal) | Yes (defined condition) | Yes (θ, λ, β, ρ) | Cross-species, domain-universal |

**Sweet Trap is the only construct that simultaneously requires: (1) cross-species scope, (2) formal endorsement condition, (3) self-reinforcing equilibrium, (4) absence of corrective feedback, (5) multi-domain applicability.**

---

## Citation Budget for Nature Introduction

Nature Introduction: ~600 words, 10-15 references maximum.

**Paragraph 1 — Scale of the problem (human welfare losses):**
- Kivimäki et al. 2015 (Lancet, 600K meta-analysis)
- Popkin et al. 2012 (global nutrition transition)
- Allcott et al. 2020 QJE (social media welfare)
- Wei & Zhang 2011 JPE (marriage competition)

**Paragraph 2 — The evolutionary puzzle ("why do organisms keep choosing this?"):**
- Nesse & Williams 1994 (mismatch theory foundation)
- Olds & Milner 1954 (neural dissociation of reward and fitness)
- Schlaepfer et al. 2002 TREE (ecological trap definition)
- Fisher 1930 (runaway selection as prototype)

**Paragraph 3 — Our framework and what's new:**
- Robertson et al. 2013 TREE (evolutionary trap, nearest construct)
- Berridge & Robinson 1998 (wanting/liking dissociation = mechanism)
- Laibson 1997 QJE (β parameter)
- McClure et al. 2004 Science (neural present bias)

**Paragraph 4 — What we show:**
- Braghieri et al. 2022 AER (causal identification benchmark)
- Science 2021 convergence paper (cross-species benchmark)

Total: 14 references. All justified.
