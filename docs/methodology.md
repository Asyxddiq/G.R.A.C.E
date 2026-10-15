# Methodology: Cost & Downtime Conversion Model

This model turns the difference in downtime between a full OEM replacement and a PLC spare-part replacement into an estimate of financial exposure avoided per incident.

## 1. Downtime comparison framework

**Formula 1: Downtime avoided**

```
ΔD = D_OEM − D_PLC
```

| Symbol | Meaning |
|---|---|
| ΔD | Downtime avoided (days) |
| D_OEM | Average downtime for a full OEM replacement |
| D_PLC | Average downtime using a PLC spare-part service |

**Formula 2: Downtime reduction**

```
D_reduction = (ΔD / D_OEM) × 100%
```

## 2. Cost conversion model

**Formula 3: Exposure avoided**

```
C_savings = ΔD × C_day
C_day     = estimated breakdown cost per hour × 24
```

| Symbol | Meaning |
|---|---|
| C_savings | Estimated economic exposure avoided by using a PLC spare part |
| ΔD | Downtime avoided (from Formula 1) |
| C_day | Estimated cost of economic loss per day of full production shutdown |

### Breakdown cost assumptions by plant size

| Plant size | Employees | Estimated breakdown cost | Value used |
|---|---|---|---|
| Small | 10–49 | $10,000 – $50,000 / hour | $10,000 / hour |
| Medium | 50–249 | $50,000 – $150,000 / hour | $50,000 / hour |
| Large | 250+ | $200,000 – $1M+ / hour | $200,000 / hour |

The **lower end** of each range was used on purpose, so the results lean conservative on cost. The ranges were presented as modelling averages based on industry downtime benchmarks (cited in the deck as Siemens 2024 and the ABB Reliability Report). See the note on sources in [assumptions-and-limitations.md](assumptions-and-limitations.md).

## 3. Scenarios

| Input | Value |
|---|---|
| D_OEM | 14 days (fixed) |
| D_PLC, fast case | 3 days |
| D_PLC, slow case | 7 days |

### Scenario A: Small manufacturing plant ($10,000 / hour)

| Step | Fast case (3 days) | Slow case (7 days) |
|---|---|---|
| ΔD | 14 − 3 = **11 days** | 14 − 7 = **7 days** |
| D_reduction | 11/14 × 100% = **78.6%** | 7/14 × 100% = **50%** |
| C_savings | 11 × $10,000 × 24 = **$2.64M** | 7 × $10,000 × 24 = **$1.68M** |

### Scenario B: Large manufacturing plant ($200,000 / hour)

| Step | Fast case (3 days) | Slow case (7 days) |
|---|---|---|
| ΔD | **11 days** | **7 days** |
| D_reduction | **78.6%** | **50%** |
| C_savings | 11 × $200,000 × 24 = **$52.8M** | 7 × $200,000 × 24 = **$33.6M** |

The gap between the fast and slow cases for a large plant is **$19.2M per incident**. Each extra day of PLC downtime costs a large plant $4.8M of avoided exposure.

### Scaling across plant sizes

| Plant | Fast case (3 days) | Slow case (7 days) |
|---|---|---|
| Small | $2.64M | $1.68M |
| Medium | $13.2M | $8.4M |
| Large | $52.8M | $33.6M |

Because the model is linear, exposure avoided scales directly with (a) the hourly breakdown cost (plant scale) and (b) the days of downtime avoided.

## 4. Operationalising: from scenarios to real client data

The scenarios above are illustrative. To produce real figures, the proposal was a single **downtime master sheet**:

| Column | Purpose |
|---|---|
| Part no. | The component supplied |
| Customer | Who received it |
| Impact level | High / medium / low value flag |
| Time savings (hours) | Downtime avoided for that order |
| Total time savings | Roll-up across orders / period |
| Time savings by customer | Per-customer roll-up |
| Industry downtime cost | $/hour for that customer's sector |
| Attributed cost savings | Time savings × industry downtime cost |

*Worked example:* a part supplied to a customer that avoids 150 hours of downtime, at $100,000/hour, is ≈ **$15M** of downtime exposure avoided.

The same sheet can then answer questions like "total impact this month", "impact by industry" and "top parts by value", and it feeds the website dashboard and client reports.

## 5. Reproducing the numbers

```bash
python analysis/scenario_model.py
```

This prints the scenario table, writes `analysis/scenario_results.csv`, and regenerates the charts in `visuals/`. Change the inputs at the top of the script to test other assumptions.
