# Assumptions and Limitations

All figures in this repository are **illustrative scenario outputs, not verified savings or guaranteed customer outcomes**.

## Model assumptions

- **Reference OEM replacement downtime:** 14 days, treated as a full plant shutdown.
- **PLC replacement downtime:** 3-day (fast) and 7-day (slow) cases, within the stated 1–7 day service range.
- **Breakdown cost per hour:** lower end of each plant-size range (Small $10k, Medium $50k, Large $200k), converted to a daily cost × 24 hours.
- **Constant cost per hour:** the model assumes every hour of downtime costs the same and that the plant would otherwise run 24 hours a day.

## Limitations

1. **Linear, constant-cost model.** Real downtime costs are often nonlinear. They can include lost production, idle labour, expedited logistics, scrap, restart losses, and contractual penalties. Some lost production can also be recovered later, which the model ignores.
2. **24/7 operation assumed.** Plants running one or two shifts would have proportionally lower daily exposure.
3. **Partial shutdown is not guaranteed.** Having a spare part does not by itself mean only part of the plant has to stop. Shutdown scope depends on system architecture, redundancy, isolation requirements, safety procedures and the specific failed component. This needs confirming with engineers for each site.
4. **Exposure avoided ≠ realised savings.** The model estimates financial exposure, not cash saved. It does not prove root cause or a reliability improvement.
5. **Benchmark sources.** The deck attributed the breakdown-cost ranges to industry benchmarks (Siemens 2024; ABB Reliability Report). These citations should be checked against the original publications and fully referenced before the ranges are reused.
6. **Illustrative marketing figures.** Numbers shown in the website, report and social-media mockups (e.g. impact tiles) were design placeholders, not measured results.

## Notes on terminology (changed from the original deck)

- **"Conservative" vs "High" case labels.** The original slides labelled the 3-day case "Conservative" and the 7-day case "High". The 3-day case actually gives the *larger* savings, so this repo uses **Fast replacement (3-day)** and **Slow replacement (7-day)** to avoid confusion. The numbers are unchanged.
- **"Up to 50%" headline.** The slides said PLC "reduces downtime exposure by up to 50%". In the modelled cases, 50% is the *minimum* reduction (the 7-day case); the 3-day case gives 78.6%. This repo reports the range as **50–79%**.

## Disclosure

- Client names in the source data were masked and are left out here.
- Internal part numbers, order volumes and spreadsheets are not included.
- Get PLC Automation's permission before publishing any slides, logos, internal data or mentor feedback.
