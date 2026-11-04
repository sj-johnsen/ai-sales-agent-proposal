---
kurs: topics-in-econometrics-b
typ: assignment
titel: "Can an AI Agent Replace a Sales Rep Who Already Uses AI?"
untertitel: A Proposal for a Multi-Firm Field Experiment in B2B Outbound Sales
name: Simon Jensen
matrikel: 2226237U
dozent: Masayuki Sawada
datum: 2026-11-06
status: entwurf
---

## 1. Motivation

My bachelor thesis starts from a simple premise: what keeps a start-up small is staff. Growth needs people, and people are slow to hire and expensive to keep. AI agents promise to loosen this constraint, and the entry-level sales role is where they make that claim first. A business development associate (BDA) researches prospects, contacts them by phone, e-mail and LinkedIn, follows up and books meetings; an autonomous agent can now do the same by e-mail. Whether it does them as well decides whether a start-up still needs to hire for this role. This proposal asks:

"How much does replacing an AI-assisted BDA with an autonomous AI agent change the share of contacted prospects that book a meeting, and at what cost per prospect?"

## 2. Related Work and Contribution

Most field evidence on generative AI at work answers a neighboring question. In customer support, an AI assistant raised the number of issues resolved per hour by 15% on average, especially for less experienced workers (Brynjolfsson et al., 2025). In professional writing tasks, ChatGPT cut the time needed and raised quality (Noy & Zhang, 2023). Both studies treat AI as a tool in a human's hand. They measure augmentation, not replacement.

The closest study compares human and automated sales agents directly. In a randomized field experiment (n = 325) and an online experiment (n = 408), Adam et al. (2023) find that customers are more willing to show initial interest to a human sales agent, but more willing to leave their contact details with an automated one. As far as its abstract reports, the study compares automated agents with humans and with human-automated combinations, not with a human who does the whole job with AI. Both decisions it studies come before a meeting. Who makes the contact also matters in its own right: in outbound sales calls, disclosing that the caller was a chatbot cut purchase rates by 79.7% (Luo et al., 2019).

To my knowledge, no randomized study compares an autonomous agent with a human who already uses AI, on booked meetings, across more than one start-up. This proposal fills that gap, with Adam et al. (2023) as its benchmark.

## 3. Data: Where and How

Such a comparison needs data from more than one start-up. The experiment would run at Finto and three further B2B start-ups, each contributing one BDA for a two-week pilot and a twelve-week main phase. In return, each start-up uses the agent free of charge during the study and receives its own results. Finto, a Munich-based AI start-up where I worked over the summer, sets the baseline: of the roughly 1,000 firms I contacted there, about 100 a week, two to three in every 100 booked a meeting. The pilot rechecks this rate for the BDAs' channel mix. The pool of prospects is finite, so each start-up confirms before the start that its target profile, drawn from its CRM and a commercial prospect database, yields about 4,800 accounts: 1,200 for the BDA and 3,600 for the agent.

All outcomes come from systems the start-ups already run. The sending tool records every e-mail, bounce and reply; the dialer and the CRM record calls, LinkedIn messages and booked and held meetings with timestamps; the BDA logs working hours; the agent logs its API spend. Pre-assignment covariates (industry, firm size, country, lead source) come from the CRM and the prospect database. Each start-up exports pseudonymized account-level records under a data-sharing agreement. The BDAs consent, outreach follows the rules on unsolicited messages, and the study needs ethics approval.

## 4. Design and Parameter of Interest

So what should the agent be compared with? The obvious control group is a human without AI. It would be the easier comparison and would show the larger effect. It is also the wrong one. A start-up that considers replacing its BDA today compares the agent with a BDA who already drafts e-mails with ChatGPT, so only this comparison answers the replacement question. The control arm is therefore a BDA who works as usual, by e-mail, phone and LinkedIn, and may use any general-purpose AI tool but not the agent; the tools used are logged. The comparison thus bundles author and channel, which is exactly what a replacement changes.

Field experiments with sales and call-center staff usually randomize the workers (Bloom et al., 2015; Sandvik et al., 2020). Here the agent does not change how the BDA works but takes the BDA's place, so the unit of randomization is the prospect firm (the account), not the contact person; two colleagues at the same prospect then never hear from both arms (Sawada, 2026, Lecture 2). Each week, a new batch of accounts is assigned within strata of start-up × week (Bruhn & McKenzie, 2009). Because only the human arm is capacity-bound, three accounts go to the agent for every account the BDA handles (List et al., 2011). Each arm owns its accounts until a meeting is booked or the sequence ends, and the arms send from separate domains. Both rules limit interference between the arms. The agent writes only e-mails and states in each that it is an AI assistant.

The two arms hit different limits. The median sales development representative (SDR, the common US title for a BDA) logs 112 activities a day, 44 of them calls and 41 e-mails (Bertuzzi, 2025). These are touches across sequences: at an assumed eight to ten touches per account, 560 touches a week reach only 56 to 70 new accounts, so my 100 a week at Finto is an optimistic pace. The pilot therefore measures each BDA's pace, which then fixes the size of all twelve weekly batches; a researcher draws each batch from the pool and randomizes it before the BDA sees it. The agent is limited by deliverability, not time. A new mailbox needs weeks of warm-up, after which a typical mailbox sends 14 to 42 cold e-mails a day (Smartlead, n.d.), and Google's sender guidelines ask for authentication and reported spam below 0.1% (Google, n.d.). Every mailbox in either arm is therefore capped at an assumed 40 cold e-mails a day. At an assumed four e-mails per account, the agent's 300 new accounts a week need six warmed mailboxes per start-up and the BDA's 100 need two. The agent wins on volume, the BDA perhaps on quality, so both the meeting rate per account and meetings per week are measured.

The parameter of interest is the intention-to-treat effect $\tau = \mathbb{E}[Y_i(1) - Y_i(0)]$ on the accounts of the participating start-ups, where $Y_i$ equals one if account $i$ books a meeting within 30 days of the first contact. $\tau$ is the net policy effect of deploying an e-mail-only, disclosed agent rather than an AI-assisted, multichannel BDA, and the booked meeting is the single primary outcome. Cost is the second quantity the question names. Hours and set-up time accrue per week, not per account, so cost per account is measured for each start-up, week and arm: API spend, mailboxes and a share of supervision time for the agent, logged hours times the start-up's loaded wage for the BDA. As a benchmark, the median SDR earns a base of USD 55,000, or USD 80,000 with variable pay (Bertuzzi, 2025), and wages are 70.3% of employer costs (U.S. Bureau of Labor Statistics, 2025). That puts a BDA at roughly USD 38 to 55 per hour, or USD 15 to 22 per account at 100 accounts a week. The cost difference between the arms, $\tau_C$, gives the net value of a meeting worth $v$ as $v\tau - \tau_C$, reported over a range of $v$ so that no estimate close to zero ever sits in a denominator.

## 5. Estimation and Power

The meeting effect is estimated by

$$Y_i = \tau A_i + \gamma_{s(i)} + (X_i - \bar X)'\beta + A_i (X_i - \bar X)'\delta + \varepsilon_i ,$$

where $A_i$ is assignment to the agent, $\gamma_{s(i)}$ are stratum fixed effects and $X_i$ are the centered pre-assignment covariates, interacted with $A_i$ as in Lin (2013). The covariates add precision, not identification. Assignment varies at the account level, and the four start-ups are not a random sample of start-ups, so heteroskedasticity-robust standard errors fit the estimand (Abadie et al., 2023). $\tau_C$ is estimated across the 48 start-up-weeks.

Three further rules are fixed in advance. Secondary outcomes (any reply, positive reply, bounce, unsubscribe) are corrected for multiple testing with the Romano-Wolf step-down procedure (Romano & Wolf, 2005; Sawada, 2026, Lecture 2, Part 2). Accounts the BDA never works stay in their arm under ITT. If a prospect bypasses the agent and reaches the BDA, assignment serves as an instrument for the arm that handled the account, which identifies the effect for compliers as long as no BDA account reaches the agent (Bloom, 1984; Imbens & Angrist, 1994; Sawada, 2026, Lecture 3). Whether a booked meeting is held is defined only for accounts that book, so comparing show-up rates would condition on a post-treatment outcome; the target is the effect on accounts that would book with either arm, bounded under monotonicity of booking (Frangakis & Rubin, 2002; Lee, 2009; Sawada, 2026, Lecture 10).

How large an effect the design can detect depends on the base rate and on the BDAs' pace. At $p_0 = 2.5$% and 100 accounts a week, four BDAs over twelve weeks give 4,800 human accounts, and with 14,400 agent accounts on top the design detects a rise to 3.26% (+30%) or a fall to 1.80% (−28%). At 150 accounts a week the bounds narrow to +25% and −23%; at 50 they widen to +43% and −39% (Appendix, Tables A2 and A3). A Monte Carlo check of the estimator under independent accounts agrees: its 95% intervals cover the true effect in 93 to 95% of 1,000 replications, it rejects a true null in 6.2% and detects +30% in 76 to 78% (Appendix, Table B1). A null result therefore means that changes of about 30% would probably have been found, not that the arms perform equally. The experiment runs into the very constraint it is meant to test: the number of people.

## 6. Threats to Validity

Size is not the only threat. The agent learns, so the treatment changes while it is being measured, which breaks the "no hidden treatments" part of SUTVA (Sawada, 2026, Lecture 2). Updates are therefore allowed only between weekly batches and are logged, so the pooled $\tau$ averages over the agent versions used. BDAs who know about the comparison may work harder, a John Henry effect that would understate $\tau$; activity and hours are logged to check this. Because the agent only writes, a positive result shows that e-mail alone can do the BDA's multichannel job, not that an agent could also call. Finally, four participating start-ups chosen by access are not all start-ups, and each BDA is one person. The estimate holds for these start-ups and these people.

The experiment returns to the opening premise with a number. If the agent's net value per account is positive across plausible meeting values, staff stops being the constraint at the first stage of sales. If it is negative, a start-up still needs people to grow.

## References

Abadie, A., Athey, S., Imbens, G. W., & Wooldridge, J. M. (2023). When should you adjust standard errors for clustering? *The Quarterly Journal of Economics, 138*(1), 1-35. https://doi.org/10.1093/qje/qjac038

Adam, M., Roethke, K., & Benlian, A. (2023). Human vs. automated sales agents: How and why customer responses shift across sales stages. *Information Systems Research, 34*(3), 1148-1168. https://doi.org/10.1287/isre.2022.1171

Bertuzzi, M. (2025). *2025 SDR models & metrics report*. The Bridge Group. https://www.bridgegroupinc.com/research/2025-sdr-models-metrics-report-the-bridge-group

Bloom, H. S. (1984). Accounting for no-shows in experimental evaluation designs. *Evaluation Review, 8*(2), 225-246. https://doi.org/10.1177/0193841X8400800205

Bloom, N., Liang, J., Roberts, J., & Ying, Z. J. (2015). Does working from home work? Evidence from a Chinese experiment. *The Quarterly Journal of Economics, 130*(1), 165-218. https://doi.org/10.1093/qje/qju032

Bruhn, M., & McKenzie, D. (2009). In pursuit of balance: Randomization in practice in development field experiments. *American Economic Journal: Applied Economics, 1*(4), 200-232. https://doi.org/10.1257/app.1.4.200

Brynjolfsson, E., Li, D., & Raymond, L. (2025). Generative AI at work. *The Quarterly Journal of Economics, 140*(2), 889-942. https://doi.org/10.1093/qje/qjae044

Frangakis, C. E., & Rubin, D. B. (2002). Principal stratification in causal inference. *Biometrics, 58*(1), 21-29. https://doi.org/10.1111/j.0006-341X.2002.00021.x

Google. (n.d.). *Email sender guidelines FAQ*. Gmail Help. Retrieved November 4, 2026, from https://support.google.com/a/answer/14229414

Ibragimov, R., & Müller, U. K. (2010). t-Statistic based correlation and heterogeneity robust inference. *Journal of Business & Economic Statistics, 28*(4), 453-468. https://doi.org/10.1198/jbes.2009.08046

Imbens, G. W., & Angrist, J. D. (1994). Identification and estimation of local average treatment effects. *Econometrica, 62*(2), 467-475. https://doi.org/10.2307/2951620

Jensen, S. (2026). *ai-sales-agent-proposal: Power calculation and Monte Carlo check for a research proposal* [Computer software]. GitHub. https://github.com/sj-johnsen/ai-sales-agent-proposal

Lee, D. S. (2009). Training, wages, and sample selection: Estimating sharp bounds on treatment effects. *The Review of Economic Studies, 76*(3), 1071-1102. https://doi.org/10.1111/j.1467-937X.2009.00536.x

Lin, W. (2013). Agnostic notes on regression adjustments to experimental data: Reexamining Freedman's critique. *The Annals of Applied Statistics, 7*(1), 295-318. https://doi.org/10.1214/12-AOAS583

List, J. A., Sadoff, S., & Wagner, M. (2011). So you want to run an experiment, now what? Some simple rules of thumb for optimal experimental design. *Experimental Economics, 14*(4), 439-457. https://doi.org/10.1007/s10683-011-9275-7

Luo, X., Tong, S., Fang, Z., & Qu, Z. (2019). Frontiers: Machines vs. humans: The impact of artificial intelligence chatbot disclosure on customer purchases. *Marketing Science, 38*(6), 937-947. https://doi.org/10.1287/mksc.2019.1192

Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity effects of generative artificial intelligence. *Science, 381*(6654), 187-192. https://doi.org/10.1126/science.adh2586

Romano, J. P., & Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. *Econometrica, 73*(4), 1237-1282. https://doi.org/10.1111/j.1468-0262.2005.00615.x

Sandvik, J. J., Saouma, R. E., Seegert, N. T., & Stanton, C. T. (2020). Workplace knowledge flows. *The Quarterly Journal of Economics, 135*(3), 1635-1680. https://doi.org/10.1093/qje/qjaa013

Sawada, M. (2026). *Topics in Econometrics B: Lectures 2, 3 and 10* [Lecture slides]. Hitotsubashi University.

Smartlead. (n.d.). *How long should you warm up an email domain before a campaign?* Retrieved November 4, 2026, from https://www.smartlead.ai/benchmarks/how-long-to-warm-up-email-before-cold-outreach

U.S. Bureau of Labor Statistics. (2025). *Employer costs for employee compensation, March 2025* (News Release USDL-25-0958). https://www.bls.gov/news.release/archives/ecec_06132025.htm
