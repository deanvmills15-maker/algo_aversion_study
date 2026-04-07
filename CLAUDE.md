# Algorithm Aversion Study — oTree Experiment

## Project Overview

An oTree 5.x experiment studying algorithm aversion in investment decisions.

**Design:** 2x2 between-subjects factorial
- **Factor 1 — Frame:** Gain vs. Loss
- **Factor 2 — Timing:** Pay-before-see vs. See-before-pay

**5-Asset Portfolio (used in Stage 2):**
1. T-Bills (risk-free)
2. Index Fund
3. REITs
4. Individual Stocks
5. Cryptocurrency

**Experiment Flow:** Stage 1 (Risk Elicitation) → Stage 2 (Portfolio Allocation) → Stage 3 (Results/Debrief)

---

## Stage 1 — Risk Elicitation (`risk_elicitation` app)

### Screen 1: Gamble Choice (Eckel-Grossman)

A 50/50 gamble table with 5 rows. Each gamble pays one of two amounts, each equally likely.

| Gamble | High Payoff (50%) | Low Payoff (50%) | Expected Value |
|--------|-------------------|------------------|----------------|
| 1 (Low Risk)  | $28 | $28 | $28.00 |
| 2              | $36 | $24 | $30.00 |
| 3              | $44 | $20 | $32.00 |
| 4              | $52 | $16 | $34.00 |
| 5 (High Risk) | $60 | $12 | $36.00 |

**UI Requirements:**
- Clean, professional table suitable for research poster screenshots
- Radio button per row for selection
- "Low Risk" / "High Risk" labels on rows 1 and 5
- 50/50 probability indicators above the table
- FinTech-themed aesthetic (Inter font, card layout, blue accent color)

**Data captured:** `gamble_choice` (integer 1–5)

---

## Tech Stack

- oTree 5.x (Python 3.11, Conda environment)
- Bootstrap (oTree default) + custom CSS overrides
- SQLite for local dev; Postgres for deployment
