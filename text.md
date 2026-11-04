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

My bachelor thesis starts from a simple premise: what keeps a start-up small is staff. Acemoglu and Restrepo (2019) separate a tool that makes labor more productive at its current tasks from automation that takes those tasks over. Growth needs people, and people are slow to hire and expensive to keep. AI agents promise to loosen this constraint, and the entry-level sales role is where they make that claim first. A business development associate (BDA) researches prospects, contacts them by phone, e-mail and LinkedIn, follows up and books meetings; an autonomous agent can now do the same by e-mail. Whether it does them as well decides whether a start-up still needs to hire for this role. This proposal asks:

"How much does replacing an AI-assisted BDA with an autonomous AI agent change the share of prospect accounts that book a meeting, and at what cost per account?"

## 2. Related Work and Contribution

Most field evidence on generative AI at work answers a neighboring question. An AI assistant raised the issues resolved per hour in customer support by 15% (Brynjolfsson et al., 2025), and ChatGPT made professional writing faster and better (Noy & Zhang, 2023). They measure augmentation, not replacement.

The closest study compares human and automated sales agents directly. In a randomized field experiment (n = 325) and an online experiment (n = 408), Adam et al. (2023) find that customers are more willing to show initial interest to a human sales agent, but more willing to leave their contact details with an automated one. As far as its abstract reports, it never compares the automated agent with a human who does the whole job with AI. Both decisions it studies come before a meeting. Who makes the contact also matters in its own right: in outbound sales calls, disclosing that the caller was a chatbot cut purchase rates by 79.7% (Luo et al., 2019).

Tannenbaum (2026) randomizes a disclosed chat agent against live-chat staff on retail and hospitality sites, not an AI-assisted BDA on booked meetings across start-ups. This proposal would fill that gap, with Adam et al. (2023) as its benchmark.

## 3. Data: Where and How

Such a comparison needs data from more than one start-up. The experiment would run at Finto and three further B2B start-ups, each contributing one BDA for a two-week pilot and a twelve-week main phase. In return, each start-up uses the agent free of charge and receives its own results. Finto, a Munich-based AI start-up where I worked over the summer, sets the baseline: of the roughly 1,000 firms I contacted there, about 100 a week, two to three in every 100 booked a meeting. Because the pool of prospects is finite, each start-up's target profile, drawn from its CRM and a commercial prospect database, must yield up to 4,800 accounts (up to 1,200 for the BDA and 3,600 for the agent), de-duplicated across start-ups.

All outcomes come from systems the start-ups already run: the sending tool, the dialer and the CRM record every contact, reply and meeting, the BDA logs hours and the agent its API spend. Covariates (industry, firm size, country, lead source) come from the CRM and the prospect database. Each start-up exports pseudonymized account-level records under a data-sharing agreement; the BDAs consent, outreach follows the rules on unsolicited messages, and the study needs ethics approval.

## 4. Design and Parameter of Interest

So what should the agent be compared with? The obvious control group is a human without AI. It would be the easier comparison and would show the larger effect. It is also the wrong one. A start-up that replaces its BDA today replaces one who already drafts e-mails with ChatGPT. The control arm is therefore a BDA who works as usual, by e-mail, phone and LinkedIn, and may use any general-purpose AI tool but not the agent; the tools used are logged. The comparison thus bundles author and channel, which is exactly what a replacement changes.

Field experiments with sales and call-center staff usually randomize the workers (Bloom et al., 2015; Sandvik et al., 2020). Here the agent does not change how the BDA works but takes the BDA's place, so the unit of randomization is the prospect firm (the account), not the contact person; two colleagues at the same prospect then never hear from both arms (Sawada, 2026, Lecture 2). Each week, a new batch of accounts is assigned within strata of start-up × week (Bruhn & McKenzie, 2009). Because only the human arm is capacity-bound, three accounts go to the agent for every account the BDA handles (List et al., 2011). Each arm keeps its accounts and sends from its own domains, which limits interference between the arms. The agent writes only e-mails and states in each that it is an AI assistant, the disclosure that Article 50(1) of Regulation (EU) 2024/1689 has required since 2 August 2026.

The two arms hit different limits. The median sales development representative (SDR, the common US title for a BDA) logs 112 activities a day, 44 of them calls and 41 e-mails (Bertuzzi, 2025). These are touches across sequences: at an assumed eight to ten touches per account, 560 touches a week reach only 56 to 70 new accounts, so my 100 a week at Finto is optimistic and the design plans with 85 to 100. The pilot therefore measures each BDA's pace, which then fixes the size of all twelve weekly batches; a researcher draws each batch from the pool and randomizes it before the BDA sees it. The agent is limited by deliverability, not time, so each mailbox is capped at an assumed 40 (Jensen, 2026). The agent wins on volume, the BDA perhaps on quality, so the meeting rate per account is the estimand.

The parameter of interest is the intention-to-treat effect $\tau = \mathbb{E}[Y_i(1) - Y_i(0)]$ on the accounts of the participating start-ups, where $Y_i$ equals one if account $i$ books a meeting within 45 days of its batch date, a window fixed at assignment and long enough for both arms' sequences. $\tau$ is the net policy effect of deploying an e-mail-only, disclosed agent rather than an AI-assisted, multichannel BDA, and the booked meeting is the single primary outcome. Cost, the second quantity the question names, accrues per week, so cost per account is measured for each start-up, week and arm: API spend, mailboxes and supervision time for the agent, logged hours times the loaded wage for the BDA. A BDA costs about USD 15 to 26 per account at 85 to 100 accounts a week and USD 22 to 39 at 56 to 70 (Bertuzzi, 2025; U.S. Bureau of Labor Statistics, 2025). The cost difference between the arms, $\tau_C$, gives the net value of a meeting worth $v$ as $v\tau - \tau_C$, reported over a range of $v$ so that no estimate close to zero ever sits in a denominator.

## 5. Estimation and Power

The meeting effect is estimated by

$$Y_i = \tau A_i + \gamma_{s(i)} + (X_i - \bar X)'\beta + A_i (X_i - \bar X)'\delta + \varepsilon_i ,$$

where $A_i$ is assignment to the agent, $\gamma_{s(i)}$ are stratum fixed effects and $X_i$ are the centered pre-assignment covariates, interacted with $A_i$ as in Lin (2013). The covariates add precision, not identification. Assignment varies at the account level, and the four start-ups are not a random sample of start-ups, so heteroskedasticity-robust standard errors fit the estimand (Abadie et al., 2023). $\tau_C$ is estimated across the 48 start-up-weeks. Because BDA cost per account moves with batch size, the interval for $v\tau - \tau_C$ is a bootstrap over these 48 weeks.

Secondary outcomes (any reply, positive reply, bounce, unsubscribe) use the Romano-Wolf step-down procedure (Romano & Wolf, 2005; Sawada, 2026, Lecture 2, Part 2). Under ITT, every account stays in its assigned arm, including accounts the BDA never works and prospects who answer the BDA after the agent's e-mails. Whether a booked meeting is held is bounded under monotonicity (Frangakis & Rubin, 2002; Lee, 2009; Sawada, 2026, Lecture 10).

At $p_0 = 2.5$% and 85 to 100 accounts a week, four BDAs over twelve weeks give 4,080 to 4,800 human accounts, and with three times as many agent accounts the design detects a rise of 30 to 33% or a fall of 28 to 30%. At 150 accounts a week the bounds narrow to +25% and −23%; at 50 they widen to +43% and −39% (Jensen, 2026). A Monte Carlo check under independent accounts comes close: 93 to 95% coverage, 6.2% false rejections and 76 to 78% power at +30% (Jensen, 2026). A null result therefore means that, at the planned pace, changes of about 30% would probably have been found, not that the arms perform equally. The experiment runs into the very constraint it is meant to test: the number of people.

## 6. Threats to Validity

The agent learns, so the treatment changes while it is being measured, which breaks the "no hidden treatments" part of SUTVA (Sawada, 2026, Lecture 2). Updates are therefore allowed only between weekly batches and are logged, so the pooled $\tau$ averages over the agent versions used. A John Henry effect, BDAs working harder because they know the comparison, would understate $\tau$; activity and hours are logged. Because the agent only writes, a positive result shows that e-mail alone can do the BDA's multichannel job, not that an agent could also call. Finally, four start-ups chosen by access are not all start-ups; the estimate holds for them and their four BDAs, and start-up-specific estimates are reported alongside.

The experiment returns to the opening premise with a number. If the agent's net value per account is positive across plausible meeting values, staff stops being the constraint at the first stage of sales. If it is negative, a start-up still needs people to grow.

## References

Abadie, A., Athey, S., Imbens, G. W., & Wooldridge, J. M. (2023). When should you adjust standard errors for clustering? *The Quarterly Journal of Economics, 138*(1), 1-35. https://doi.org/10.1093/qje/qjac038

Acemoglu, D., & Restrepo, P. (2019). Automation and new tasks: How technology displaces and reinstates labor. *Journal of Economic Perspectives, 33*(2), 3-30. https://doi.org/10.1257/jep.33.2.3

Adam, M., Roethke, K., & Benlian, A. (2023). Human vs. automated sales agents: How and why customer responses shift across sales stages. *Information Systems Research, 34*(3), 1148-1168. https://doi.org/10.1287/isre.2022.1171

Bertuzzi, M. (2025). *2025 SDR models & metrics report*. The Bridge Group. https://www.bridgegroupinc.com/research/2025-sdr-models-metrics-report-the-bridge-group

Bloom, N., Liang, J., Roberts, J., & Ying, Z. J. (2015). Does working from home work? Evidence from a Chinese experiment. *The Quarterly Journal of Economics, 130*(1), 165-218. https://doi.org/10.1093/qje/qju032

Bruhn, M., & McKenzie, D. (2009). In pursuit of balance: Randomization in practice in development field experiments. *American Economic Journal: Applied Economics, 1*(4), 200-232. https://doi.org/10.1257/app.1.4.200

Brynjolfsson, E., Li, D., & Raymond, L. (2025). Generative AI at work. *The Quarterly Journal of Economics, 140*(2), 889-942. https://doi.org/10.1093/qje/qjae044

Frangakis, C. E., & Rubin, D. B. (2002). Principal stratification in causal inference. *Biometrics, 58*(1), 21-29. https://doi.org/10.1111/j.0006-341X.2002.00021.x

Jensen, S. (2026). *ai-sales-agent-proposal: Code and appendix for a research proposal* [Computer software]. GitHub. https://github.com/sj-johnsen/ai-sales-agent-proposal

Lee, D. S. (2009). Training, wages, and sample selection: Estimating sharp bounds on treatment effects. *The Review of Economic Studies, 76*(3), 1071-1102. https://doi.org/10.1111/j.1467-937X.2009.00536.x

Lin, W. (2013). Agnostic notes on regression adjustments to experimental data: Reexamining Freedman's critique. *The Annals of Applied Statistics, 7*(1), 295-318. https://doi.org/10.1214/12-AOAS583

List, J. A., Sadoff, S., & Wagner, M. (2011). So you want to run an experiment, now what? Some simple rules of thumb for optimal experimental design. *Experimental Economics, 14*(4), 439-457. https://doi.org/10.1007/s10683-011-9275-7

Luo, X., Tong, S., Fang, Z., & Qu, Z. (2019). Frontiers: Machines vs. humans: The impact of artificial intelligence chatbot disclosure on customer purchases. *Marketing Science, 38*(6), 937-947. https://doi.org/10.1287/mksc.2019.1192

Noy, S., & Zhang, W. (2023). Experimental evidence on the productivity effects of generative artificial intelligence. *Science, 381*(6654), 187-192. https://doi.org/10.1126/science.adh2586

Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence. *Official Journal of the European Union, L 2024/1689*. http://data.europa.eu/eli/reg/2024/1689/oj

Romano, J. P., & Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. *Econometrica, 73*(4), 1237-1282. https://doi.org/10.1111/j.1468-0262.2005.00615.x

Sandvik, J. J., Saouma, R. E., Seegert, N. T., & Stanton, C. T. (2020). Workplace knowledge flows. *The Quarterly Journal of Economics, 135*(3), 1635-1680. https://doi.org/10.1093/qje/qjaa013

Sawada, M. (2026). *Topics in Econometrics B: Lectures 2 and 10* [Lecture slides]. Hitotsubashi University.

Tannenbaum, B. (2026). *Selling in the wild: Benchmark and randomized field evidence for a sales agent trained on commercial conversations* (arXiv:2610.25461). https://arxiv.org/abs/2610.25461

U.S. Bureau of Labor Statistics. (2025). *Employer costs for employee compensation, March 2025* (News Release USDL-25-0958). https://www.bls.gov/news.release/archives/ecec_06132025.htm
