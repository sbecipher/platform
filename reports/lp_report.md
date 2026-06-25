# Institutional LP Due-Diligence Brief

Run Context: RUN_ID `pm-lp-scm-20260624T212419Z`; run_root `output/runs/pm-lp-scm-20260624T212419Z`. All artifact references are relative to `run_root`; source aliases resolve in `## Source Key`.

## Strategy Overview

This is a post-deployment, concentrated materials-and-mining portfolio review, not a staged-deployment plan. The selected book is the `min_variance` construction with 38 [portfolio_size_selection] active equity positions, 80.00% [post_deployment_portfolio_summary] target equity weight, and 20.00% [post_deployment_portfolio_summary] cash/opportunity sleeve weight. The portfolio is implementation trade-ready [implementation_readiness_status], while institutional clearance status remains `not_requested` [institutional_clearance_status] and must not be described as institutionally cleared.

## Investment Process

The workflow emits run-scoped artifacts and manifests for repeatability; the artifact manifest lists no missing rows [artifact_manifest]. Selection used the emitted frontier rather than a hardcoded position count: the primary book has validation Sharpe 1.6724 [portfolio_size_selection], in-sample Sharpe 1.0249 [portfolio_size_selection], and shrunk score 1.0264 [portfolio_size_selection]. Sharpe decay is floored at 0.0000 [selection_decay_diagnostics] because validation exceeded in-sample; it is a single validation regime with CV Sharpe mean 1.2858 [selection_decay_diagnostics], std 1.0057 [selection_decay_diagnostics], min 0.1461 [selection_decay_diagnostics], and 4 folds.

## Portfolio Construction Discipline

Book-level forward E[R] means sleeve-inclusive and is -5.52% [forward_expected_returns_summary]; equity-sleeve/equity-weighted forward E[R] is -6.91% [forward_expected_returns_summary]. The negative expected-return signal governs fiduciary caveats, while the capital decision is based on risk-control, capacity, and governance-readiness evidence rather than a return-accretive forecast. The comparison book has 46 [portfolio_size_selection] active equities and validation Sharpe 1.7160 [portfolio_size_selection].

## Position-Level Investment Case

| Ticker | Weight | Mandate fit | Forward E[R] | Valuation basis | Governance/risk caveat |
|---|---:|---|---:|---|---|
| MT | 6.063819% [target_equity_portfolio] | steel | 0.989086% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| STLD | 5.983926% [target_equity_portfolio] | steel | -5.378231% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| MP | 0.625000% [target_equity_portfolio] | rare_earth_critical_minerals | -10.630533% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| LEU | 0.625000% [target_equity_portfolio] | uranium_nuclear_fuel | -12.412834% [forward_expected_returns] | needs_adjusted_noa_review; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| CMP | 2.649215% [target_equity_portfolio] | industrial_minerals_chemicals | -18.027611% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| TMC | 0.625000% [target_equity_portfolio] | critical_minerals | 8.197767% [forward_expected_returns] | roim_not_applicable_project_nav_required; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| HBM | 0.625000% [target_equity_portfolio] | base_metals_copper | 4.335986% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| UAMY | 0.625000% [target_equity_portfolio] | specialty_minerals | -11.443711% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| IDR | 2.500862% [target_equity_portfolio] | critical_minerals | -7.143872% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| LTBR | 0.625000% [target_equity_portfolio] | uranium_nuclear_fuel | -11.508403% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| IPX | 2.064310% [target_equity_portfolio] | titanium_advanced_materials | -11.674873% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| ABAT | 0.625000% [target_equity_portfolio] | battery_recycling | -11.007149% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| NB | 0.625014% [target_equity_portfolio] | critical_minerals | -10.624078% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| TMQ | 0.625000% [target_equity_portfolio] | base_metals_copper | -15.534345% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| UUUU | 0.625000% [target_equity_portfolio] | uranium_rare_earth_critical_minerals | -9.138105% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| CENX | 0.625000% [target_equity_portfolio] | aluminum | 30.983618% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| HCC | 0.625002% [target_equity_portfolio] | metallurgical_coal | -21.531176% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| CCJ | 4.259932% [target_equity_portfolio] | uranium_nuclear_fuel | -23.265030% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| SQM | 3.526695% [target_equity_portfolio] | specialty_materials | 4.131226% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| UEC | 0.625000% [target_equity_portfolio] | uranium_nuclear_fuel | -11.247071% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| BTU | 0.625001% [target_equity_portfolio] | coal | -12.329642% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| METC | 0.625000% [target_equity_portfolio] | metallurgical_coal | -12.515482% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| GGB | 8.749999% [target_equity_portfolio] | steel | 50.963327% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| SCCO | 3.934209% [target_equity_portfolio] | base_metals_copper | -9.676919% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| LAC | 0.625000% [target_equity_portfolio] | battery_materials_lithium | -12.433090% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| TX | 12.500000% [target_equity_portfolio] | steel | -34.434489% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| RS | 18.750000% [target_equity_portfolio] | steel_distribution | -5.178337% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action monitor [risk_budget_analysis] |
| USAR | 0.625002% [target_equity_portfolio] | rare_earth_critical_minerals | -12.076986% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| CMC | 0.625005% [target_equity_portfolio] | steel | -24.195174% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| MTRN | 4.780879% [target_equity_portfolio] | specialty_materials | -18.367751% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| KALU | 0.625002% [target_equity_portfolio] | aluminum | -6.667538% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| RYZ | 0.625001% [target_equity_portfolio] | steel_distribution | -15.611297% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| WS | 0.625000% [target_equity_portfolio] | steel | 0.372591% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| NUE | 0.625117% [target_equity_portfolio] | steel | -5.856816% [forward_expected_returns] | valued; no negative-NOPAT flag [roim_valuation] | ok; binding_action trade_ready [risk_budget_analysis] |
| ALB | 0.625000% [target_equity_portfolio] | battery_materials_lithium | -16.415107% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| IE | 0.625000% [target_equity_portfolio] | critical_minerals | -13.353671% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| CNR | 4.588969% [target_equity_portfolio] | coal | -17.274778% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |
| SXC | 4.647037% [target_equity_portfolio] | coke_processing | -15.164747% [forward_expected_returns] | valued_negative_nopat; negative-NOPAT caveat [roim_valuation] | exception_active; binding_action trade_ready [risk_budget_analysis] |

PM-approved exception theses are fiduciary caveats, not underwriteable conclusions. Required PM approval disclosures follow:

| Ticker | Selected weight | Approved full-book band | Fiduciary caveat |
|---|---:|---|---|
| ABAT | 0.625000% [target_equity_portfolio] | 0.250000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 0.750000% [pm_exception_register] cap | Full-book implemented 0.500000% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve ABAT as a small battery-recycling and circular-supply-chain exposure. The thesis is materials recovery and domestic battery-metal optionality, while negative NOPAT and early execution risk require a narrow starter band. [pm_exception_register] |
| ALB | 0.625000% [target_equity_portfolio] | 0.000000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 10.000000% [pm_exception_register] cap | Full-book implemented 0.500000% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve ALB inside a 0%-10% full-book range as lithium and battery-materials exposure linked to the fund's electrification and supply-chain materials thesis. The position must be sized as cyclical lithium optionality: negative NOPAT, lithium price compression, and incomplete valuation readiness remain explicit caveats and require continued monitoring. [pm_exception_register] |
| BTU | 0.625001% [target_equity_portfolio] | 0.000000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 10.000000% [pm_exception_register] cap | Full-book implemented 0.500001% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve BTU inside a 0%-10% full-book range as cyclical coal and metallurgical-coal optionality supporting steel and energy-materials exposure. The PM approval depends on cycle-normalized economics and cash generation recovering from negative NOPAT, with carbon, regulatory, and coal price risks carried as explicit monitoring conditions. [pm_exception_register] |
| CNR | 4.588969% [target_equity_portfolio] | 0.000000% [pm_exception_register] min / 3.660000% [pm_exception_register] target / 10.000000% [pm_exception_register] cap | Full-book implemented 3.671175% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve CNR inside a 0%-10% full-book range as a scaled coal and metallurgical-coal exposure supporting the steel supply-chain and industrial-materials thesis. The target reflects optimizer demand for the exposure, but negative NOPAT, coal-cycle volatility, and balance-sheet sensitivity must be carried as active caveats. [pm_exception_register] |
| IE | 0.625000% [target_equity_portfolio] | 0.000000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 10.000000% [pm_exception_register] cap | Full-book implemented 0.500000% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve IE inside a 0%-10% full-book range as US copper and critical-minerals development exposure tied to the fund's electrification and domestic supply-chain thesis. The position is project-stage optionality, not valuation-ready mature operating exposure; negative NOPAT, financing, permitting, and milestone execution require continued monitoring. [pm_exception_register] |
| LAC | 0.625000% [target_equity_portfolio] | 0.250000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 1.000000% [pm_exception_register] cap | Full-book implemented 0.500000% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve LAC as a development-stage lithium exposure linked to the battery-materials thesis, specifically with project-NAV framing. Reports must preserve the pre-revenue/project-development caveat and present it as not valuation-ready on operating fundamentals. [pm_exception_register] |
| METC | 0.625000% [target_equity_portfolio] | 0.250000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 1.000000% [pm_exception_register] cap | Full-book implemented 0.500000% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve METC as a domestic industrial-materials and metallurgical-coal exposure supporting the steel supply-chain thesis. This is not a clean critical-minerals approval; reports should frame it as cyclical industrial-base exposure with negative-NOPAT caveats. [pm_exception_register] |
| MP | 0.625000% [target_equity_portfolio] | 0.250000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 1.000000% [pm_exception_register] cap | Full-book implemented 0.500000% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve MP as a controlled rare-earths and magnet-supply-chain exposure tied to the fund's national-security materials thesis. The approval is strategic, not valuation-led: fundamentals show negative NOPAT and the position should remain capped as an optionality exposure. [pm_exception_register] |
| NB | 0.625014% [target_equity_portfolio] | 0.500000% [pm_exception_register] min / 0.810000% [pm_exception_register] target / 1.250000% [pm_exception_register] cap | Full-book implemented 0.500011% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve NB as a critical-minerals exposure tied to niobium, scandium, and titanium supply-chain diversification. The position can be modestly larger than the starter names because the current optimizer weight is higher, but negative NOPAT keeps it capped. [pm_exception_register] |
| RYZ | 0.625001% [target_equity_portfolio] | 0.000000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 10.000000% [pm_exception_register] cap | Full-book implemented 0.500001% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve RYZ inside a 0%-10% full-book range as a steel-distribution and scrap-linked industrial base exposure. The economics depend on volume, spread, inventory, and working-capital normalization; negative NOPAT and limited current valuation support must be disclosed as active caveats. [pm_exception_register] |
| SXC | 4.647037% [target_equity_portfolio] | 0.000000% [pm_exception_register] min / 3.730000% [pm_exception_register] target / 10.000000% [pm_exception_register] cap | Full-book implemented 3.717630% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve SXC inside a 0%-10% full-book range as coke-processing and coking-coal exposure tied to steel feedstock economics. The PM thesis rests on contract cash flows, utilization, and steel-production demand recovering from negative NOPAT; carbon and customer-concentration risks remain active monitoring items. [pm_exception_register] |
| UAMY | 0.625000% [target_equity_portfolio] | 0.250000% [pm_exception_register] min / 0.500000% [pm_exception_register] target / 0.750000% [pm_exception_register] cap | Full-book implemented 0.500000% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve UAMY as a small domestic antimony exposure linked to defense and battery-materials supply-chain resilience. Because the company is micro-cap and negative-NOPAT, the position must stay below a tighter cap than broader critical-minerals names. [pm_exception_register] |
| UEC | 0.625000% [target_equity_portfolio] | 1.000000% [pm_exception_register] min / 1.500000% [pm_exception_register] target / 2.000000% [pm_exception_register] cap | Full-book implemented 0.500000% [post_deployment_portfolio]. PM-approved full-book range; not valuation-ready, not fully cleared, and not an underwriteable conclusion without ongoing diligence. Negative-NOPAT caveat applies. Approve UEC as the largest of this group because it directly supports the uranium and nuclear-fuel security thesis and is already selected at a higher optimizer weight. Negative NOPAT remains the binding caveat, so the cap stays materially below ordinary max-name limits. [pm_exception_register] |

## Risk And Drawdown Profile

![Drawdown Expanded](output/runs/pm-lp-scm-20260624T212419Z/03_expanded/drawdown_expanded.png)

![Var Cvar Distribution](output/runs/pm-lp-scm-20260624T212419Z/06_institutional/var_cvar_distribution.png)

Historical max drawdown is -20.92% [institutional_risk_summary], VaR95 is -2.11% [institutional_risk_summary], and CVaR95 is -3.02% [institutional_risk_summary]. The portfolio VaR95 is more adverse than SPY by 0.47%, with portfolio VaR95 -2.11% [institutional_risk_summary] versus SPY VaR95 -1.64% [institutional_risk_summary]. Risk metrics use 463 trading days and a 252 trading-day annualization assumption.

Risk-budget hard-breach flags are false for every selected row [risk_budget_analysis]; the largest vol contribution is RS at 13.02% [risk_budget_analysis]. Active risk versus XME includes tracking error 16.44% [tracking_error_summary] and active share 60.71% [tracking_error_summary].

## Valuation Framework

![Roim Valuation Scatter](output/runs/pm-lp-scm-20260624T212419Z/13_valuation/roim_valuation_scatter.png)

![Roim Waterfall](output/runs/pm-lp-scm-20260624T212419Z/13_valuation/roim_waterfall.png)

Valuation coverage gate status is `pass` [governance_gates], basis `trailing_roim_claim_ready_or_forward_consensus_roim` [governance_gates], coverage 81.58% [governance_gates], covered count 31 [governance_gates], primary ROIM claim-ready count 18 [governance_gates], supplemental forward-consensus valuation count 13 [governance_gates], and selected equity count 38 [governance_gates]. ROIM remains the primary framework [roim_summary]; capital imbalance is a supplemental report-only NAV lens with 2 [capital_imbalance_summary] claim-ready rows, configured copper price 4.50 [capital_imbalance_price_provenance], and caveat `configured_spot_override` [capital_imbalance_price_provenance]. SBIC context has 3 [sbic_summary] eligible-or-likely tickers and is not legal advice or a financing conclusion [sbic_summary].

## Liquidity Capacity And Scalability

![Liquidity Dashboard](output/runs/pm-lp-scm-20260624T212419Z/03_expanded/liquidity_dashboard.png)

Selected capacity rows indicate a limiting selected policy AUM of $9,610,136 [capacity_policy]. SCYB ETF depth is documented in the ETF liquidity diligence artifact; current sleeve trade dollars are $1,000,000 [etf_liquidity_diligence_summary], and current SCYB instrument trade dollars are $231,374 [etf_liquidity_diligence_summary]. These measures distinguish full-sleeve liquidity from actual SCYB instrument liquidity.

## Governance And Constraints

Readiness is `trade_ready` [implementation_readiness_status] with 0 [implementation_readiness_status] blocking tickers, no listed binding governance breaches [governance_capital_constraints] in the held book, and no listed exception-cap breaches [governance_capital_constraints]. Size-tier constraints are monitored because hard constraints are disabled [portfolio_size_selection]; Large actual 43.14% [portfolio_size_selection] and Small actual 29.52% [portfolio_size_selection] remain important diligence items.

## Cash Opportunity Sleeve Disclosure

The cash/opportunity sleeve total is 20.00% [post_deployment_portfolio_summary]. SCYB is 4.63% [cash_opportunity_sleeve] of the total portfolio and 23.14% [etf_liquidity_diligence_summary] of the sleeve internally; residual CASH is 15.37% [cash_opportunity_sleeve]. SCYB is an approved high-yield credit ETF instrument inside the cash/opportunity sleeve, not Treasury cash, not risk-free, and not a cash substitute [cash_opportunity_sleeve_policy] [credit_sleeve_analysis].

## Data Quality And Model Governance

Selected-name source-date freshness status is `pass` [governance_gates] across 38 [governance_gates] selected names, with empty missing-ticker lists across price, market value, volume, volatility, SMA-50, and SMA-200 classes [governance_gates]. Consensus support is report-supported with claim-ready ticker count 31 [governance_gates]. Model limitations include factor attribution as OLS, historical covariance limits, OHLCV liquidity proxies, Damodaran WACC mapping, SBIC as catalyst context only, capital imbalance as supplemental NAV only, and SCYB not being Treasury cash, risk-free, or a cash substitute [model_limitations].

## Scenario And Stress Testing

![Commodity Scenarios Chart](output/runs/pm-lp-scm-20260624T212419Z/03_expanded/commodity_scenarios_chart.png)

Commodity and severe-stress work should be read as model-output stress evidence, not forecasts. Commodity proxy coverage has uncovered proxy count 0 [commodity_direct_stress], and sleeve stress is governed through cash_sleeve_stress_scenarios.csv and scyb_credit_stress.csv [cash_sleeve_stress_scenarios] [scyb_credit_stress]. Precious-metals-primary exposure remains a strict mandate risk; commodity valuation claims must cite price provenance, including the configured copper override at 4.50 [capital_imbalance_price_provenance] and as-of date 2026-06-22 [capital_imbalance_price_provenance].

## Key Risks And Mitigants

The key risks are negative sleeve-inclusive forward E[R] at -5.52% [forward_expected_returns_summary], VaR more adverse than SPY by 0.47%, PM-approved negative-NOPAT exceptions, size-tier drift, and SCYB credit-spread/liquidity risk. Mitigants are fail-closed readiness gates, no current binding held-name blockers [implementation_readiness_status], explicit PM approval bands in the exception register [pm_exception_register], capacity and ETF liquidity evidence [capacity_policy] [etf_liquidity_diligence_summary], and truncated but complete-row source coverage in rebalance_actions.csv with a truncated row set covering every selected line [rebalance_actions].

## LP Takeaway

The package is trade-ready at the implementation layer [implementation_readiness_status], but it is not institutionally cleared because clearance was not requested [institutional_clearance_status]. The negative book-level forward E[R] of -5.52% [forward_expected_returns_summary] is the binding fiduciary caveat, while validation Sharpe 1.6724 [portfolio_size_selection] and risk controls support a measured PM approval rather than a return-accretive claim. LP diligence should focus on PM exception monitoring, valuation coverage composition, size-tier drift, and SCYB credit/liquidity behavior.

## Source Key

- [03_expanded_capacity_policy] = `03_expanded/capacity_policy.json`
- [06_institutional_institutional_risk_summary] = `06_institutional/institutional_risk_summary.json`
- [artifact_manifest] = `reports/artifact_manifest.json`
- [capacity_clearance_reconciliation] = `03_expanded/capacity_clearance_reconciliation.json`
- [capacity_policy] = `03_expanded/capacity_policy.csv`
- [capital_imbalance_price_provenance] = `13_valuation/capital_imbalance_price_provenance.csv`
- [capital_imbalance_sensitivity] = `13_valuation/capital_imbalance_sensitivity.csv`
- [capital_imbalance_summary] = `13_valuation/capital_imbalance_summary.json`
- [capital_imbalance_valuation] = `13_valuation/capital_imbalance_valuation.csv`
- [cash_opportunity_sleeve] = `02_implementation/cash_opportunity_sleeve.csv`
- [cash_opportunity_sleeve_capacity_summary] = `03_expanded/cash_opportunity_sleeve_capacity_summary.json`
- [cash_opportunity_sleeve_policy] = `02_implementation/cash_opportunity_sleeve_policy.json`
- [cash_opportunity_waterfall] = `02_implementation/cash_opportunity_waterfall.csv`
- [cash_sleeve_stress_scenarios] = `06_institutional/cash_sleeve_stress_scenarios.csv`
- [commodity_direct_stress] = `03_expanded/commodity_direct_stress.csv`
- [commodity_scenarios] = `03_expanded/commodity_scenarios.csv`
- [consensus_estimates] = `06_institutional/consensus_estimates.csv`
- [consensus_field_coverage] = `06_institutional/consensus_field_coverage.csv`
- [credit_sleeve_analysis] = `06_institutional/credit_sleeve_analysis.csv`
- [drawdown_summary] = `03_expanded/drawdown_summary.csv`
- [efficient_size_portfolios] = `01_optimization_core/efficient_size_portfolios.json`
- [equity_sleeve_capacity_summary] = `03_expanded/equity_sleeve_capacity_summary.json`
- [etf_liquidity_diligence_summary] = `03_expanded/etf_liquidity_diligence_summary.csv`
- [factor_attribution] = `03_expanded/factor_attribution.csv`
- [factor_model_manifest] = `05_factor_model/factor_model_manifest.json`
- [factor_return_attribution] = `03_expanded/factor_return_attribution.csv`
- [forward_expected_returns] = `14_calibration/forward_expected_returns.csv`
- [forward_expected_returns_summary] = `14_calibration/forward_expected_returns_summary.json`
- [governance_capital_constraints] = `06_institutional/governance_capital_constraints.csv`
- [governance_gates] = `reports/governance_gates.json`
- [implementation_readiness_status] = `reports/implementation_readiness_status.json`
- [insights_context] = `reports/insights_context.json`
- [institutional_clearance_status] = `reports/institutional_clearance_status.json`
- [institutional_risk_summary] = `06_institutional/institutional_risk_summary.csv`
- [liquidity_capacity] = `03_expanded/liquidity_capacity.csv`
- [liquidity_dashboard] = `03_expanded/liquidity_dashboard.png`
- [liquidity_evidence_quality] = `03_expanded/liquidity_evidence_quality.csv`
- [liquidity_quality_summary] = `03_expanded/liquidity_quality_summary.csv`
- [model_limitations] = `reports/model_limitations.md`
- [pm_exception_register] = `06_institutional/pm_exception_register.csv`
- [portfolio_size_comparison] = `01_optimization_core/portfolio_size_comparison.csv`
- [portfolio_size_selection] = `01_optimization_core/portfolio_size_selection.json`
- [post_deployment_capacity_summary] = `03_expanded/post_deployment_capacity_summary.json`
- [post_deployment_portfolio] = `02_implementation/post_deployment_portfolio.csv`
- [post_deployment_portfolio_summary] = `02_implementation/post_deployment_portfolio_summary.json`
- [post_deployment_state] = `02_implementation/post_deployment_state.json`
- [rebalance_actions] = `reports/rebalance_actions.csv`
- [rebalance_policy] = `reports/rebalance_policy.json`
- [risk_budget_analysis] = `06_institutional/risk_budget_analysis.csv`
- [risk_budget_by_position] = `03_expanded/risk_budget_by_position.csv`
- [risk_budget_summary] = `03_expanded/risk_budget_summary.json`
- [roim_sensitivity_summary] = `13_valuation/roim_sensitivity_summary.csv`
- [roim_summary] = `13_valuation/roim_summary.json`
- [roim_terminal_growth_sensitivity] = `13_valuation/roim_terminal_growth_sensitivity.csv`
- [roim_valuation] = `13_valuation/roim_valuation.csv`
- [roim_wacc_sensitivity] = `13_valuation/roim_wacc_sensitivity.csv`
- [sbic_eligibility] = `14_calibration/sbic_eligibility.csv`
- [sbic_summary] = `14_calibration/sbic_summary.json`
- [scyb_credit_stress] = `06_institutional/scyb_credit_stress.csv`
- [sector_return_attribution] = `03_expanded/sector_return_attribution.csv`
- [security_taxonomy_quality] = `06_institutional/security_taxonomy_quality.csv`
- [selected_portfolio] = `01_optimization_core/selected_portfolio.csv`
- [selection_decay_diagnostics] = `01_optimization_core/selection_decay_diagnostics.csv`
- [severe_stress_scenarios] = `06_institutional/severe_stress_scenarios.csv`
- [sleeve_risk_analysis] = `06_institutional/sleeve_risk_analysis.csv`
- [target_equity_portfolio] = `01_optimization_core/target_equity_portfolio.csv`
- [target_equity_portfolio_summary] = `01_optimization_core/target_equity_portfolio_summary.json`
- [thesis_alignment_context] = `reports/thesis_alignment_context.csv`
- [tracking_error_summary] = `06_institutional/tracking_error_summary.csv`
