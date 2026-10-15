# G.R.A.C.E. (Engineering Consulting Project)
Developed with PLC Automation as industry partner.

### Overview:
This project is a consulting framework designed to help PLC Automation, a supplier of obsolete and hard-to-find PLC spare parts, measure and communicate the value it creates for clients. We moved the company's value proposition from implied benefits to quantified impact.

Instead of describing services ("we source obsolete parts"), the framework uses five measurable pillars, **G**ratification, **R**ecycling, **A**ccountability, **C**ost & downtime savings and **E**xperience, to show outcomes. At its core is a transparent, scenario-based model that converts *days of downtime avoided* into *financial exposure avoided* for clients of different plant sizes.

### Problem Statement:
> *How might PLC Automation systematically capture and quantify the sustainability impact of its asset life-extension and component reuse practices, and communicate this value credibly to customers and stakeholders, without disrupting its fast-paced, demand-driven supply chain operations?*

### Approach: Why replacing the part beats replacing the machine
When a PLC or control component fails or becomes obsolete, a plant can either replace the entire system through the OEM or replace only the failed part. We framed the comparison around three specific problems:

<img width="1280" alt="Downtime comparison" src="visuals/downtime-comparison.png" />

| The Problem (Full OEM Replacement) | The Solution (PLC Spare-Part Replacement) |
| :--- | :--- |
| **Long Downtime:** Replacing the whole system is modelled at **14 days** of full plant shutdown. | **Targeted Repair:** Only the failed component is replaced, modelled at **1–7 days**, often with a system-specific (partial) shutdown.* |
| **Full Restart & Higher Risk:** The whole plant must restart, increasing operational risk. | **Partial Restart:** Only the affected system restarts, lowering operational risk.* |
| **Unquantified Value:** PLC Automation's impact sat across fragmented spreadsheets and was never measured or shown to clients. | **G.R.A.C.E. Metrics:** A single master sheet and a cost model turn each order into measurable time and cost savings that can be reported. |

*\*Partial shutdown depends on plant architecture, redundancy and safety isolation. See [assumptions](docs/assumptions-and-limitations.md).*

### The G.R.A.C.E. Framework
| Pillar | What it measures | Example metrics |
| :--- | :--- | :--- |
| **Gratification** | Client and employee trust and satisfaction | Customer / employee satisfaction %, repeat purchase rate |
| **Recycling** | Material recovery and waste avoided | Recovery rate (% of parts salvaged instead of discarded) |
| **Accountability** | Product quality and responsiveness | Warranty claim rate, improvement rate, complaint resolution rate |
| **Cost & Downtime Savings** | Time and money clients avoid losing | Downtime avoided (days / hours), exposure avoided ($) |
| **Experience** | How the impact is communicated | Website impact dashboard, downloadable reports, social media |

Full detail: [docs/grace-framework.md](docs/grace-framework.md)

### Cost Conversion Model (My Lead Contribution)
```
ΔD           = D_OEM − D_PLC                  # downtime avoided (days)
D_reduction  = ΔD / D_OEM × 100%              # downtime reduction (%)
C_savings    = ΔD × C_day                     # exposure avoided ($)
C_day        = breakdown cost per hour × 24
```
- **D_OEM** = 14 days (fixed reference)
- **D_PLC** = 3 days (fast case) and 7 days (slow case)
- **Breakdown cost per hour** = lower end of each plant-size range (Small $10k, Medium $50k, Large $200k), to stay conservative

Full derivation and worked examples: [docs/methodology.md](docs/methodology.md)

### Tools & Methods
- Modelling: formula-based scenario analysis (downtime avoided → financial exposure avoided)
- Data: centralised "downtime master sheet" design (Excel) linking parts → customers → time saved → cost saved
- Reproduction: Python + Matplotlib ([analysis/scenario_model.py](analysis/scenario_model.py))
- Communication: website dashboard redesign, downloadable impact report and social-media concepts

### Result & Validation:
In the modelled cases, spare-part replacement reduces downtime by **50–79% per incident**. Because the model is linear, exposure avoided grows in direct proportion to plant scale and days avoided.

| Plant Scale | Breakdown Cost Used | Fast Case (3 days)<br>ΔD = 11 days, −78.6% | Slow Case (7 days)<br>ΔD = 7 days, −50% |
| :--- | :--- | :--- | :--- |
| Small (10–49 staff) | $10,000 / hr | **$2.64M** | **$1.68M** |
| Medium (50–249 staff) | $50,000 / hr | **$13.2M** | **$8.4M** |
| Large (250+ staff) | $200,000 / hr | **$52.8M** | **$33.6M** |

<img width="1280" alt="Exposure avoided by plant scale" src="visuals/exposure-by-plant-scale.png" />

For a large plant, the gap between the fast and slow cases alone is **$19.2M per incident**. At that scale, shorter downtime is capital protection, not just operational efficiency.

To keep the model easy to check, every figure can be reproduced from the stated assumptions with `python analysis/scenario_model.py`. These are **modelled exposure-avoided estimates, not realised savings**. See [docs/assumptions-and-limitations.md](docs/assumptions-and-limitations.md).

### Implementation Roadmap
| Phase | Timing | What happens |
| :--- | :--- | :--- |
| **1. ESG Data Collection (Pilot)** | First 2 weeks | Pilot on ~4 client datasets; calculate downtime and cost savings in Excel |
| **2. Data Capture SOP** | Next 2 weeks | Standardise capture; integrate ESG metrics into the website dashboard |
| **3. Larger-Scale Implementation** | Next 4 weeks | Expand to ~10 client datasets; compute mean / median savings; find gaps |
| **4. Full Rollout** | Thereafter | All clients captured; collate data every 2 weeks; update dashboard monthly |

### My Role
**Team Leader; Cost Quantification & Modelling Lead** (Team 1: Min Xi, Jia Qi, Shrujan, Asyhiddiq, Guru)
- Coordinated the project's direction and shaped how the service's value was framed for stakeholders.
- Built the calculation logic linking downtime avoided to financial exposure avoided (ΔD, D_reduction, C_savings).
- Structured the small, medium and large plant scenarios and the fast vs slow replacement cases.
- Turned the calculations into presentation-ready charts and impact statements, with explicit assumptions for a non-technical audience.

### Future Recommendation
To turn this framework from illustrative scenarios into a production reporting tool, the following upgrades are recommended:
1. **Validation with Real Client Data:** Run the Phase 1 pilot on actual order and downtime records so plant-specific costs replace benchmark ranges, and report results as measured savings rather than modelled exposure.
2. **Nonlinear Cost Modelling:** Extend the constant cost-per-hour model to account for shift patterns (non-24/7 plants), restart losses, expedited logistics, scrap and contractual penalties, and recoverable production.
3. **Engineering Sign-off on Shutdown Scope:** Confirm with engineers, case by case, when a spare-part replacement allows a partial rather than full shutdown, so the downtime assumptions stay defensible.
4. **Automated Impact Dashboard:** Connect the master sheet directly to the website dashboard and client reports so metrics update automatically on the collation schedule instead of by hand.

### Repository Structure
```text
G.R.A.C.E/
├── README.md
├── docs/
│   ├── grace-framework.md              # all five pillars and their metrics
│   ├── methodology.md                  # cost/downtime model, worked examples
│   └── assumptions-and-limitations.md  # what the numbers do and don't mean
├── analysis/
│   ├── scenario_model.py               # reproduces every figure and chart
│   └── scenario_results.csv            # model output
└── visuals/
    ├── downtime-comparison.png
    └── exposure-by-plant-scale.png
```

*Academic consulting project. All financial figures are illustrative scenario outputs and not an official statement by PLC Automation.*
