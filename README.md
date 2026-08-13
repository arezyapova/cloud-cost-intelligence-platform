# Cloud Cost Intelligence Data Platform

## Business problem

Cloud-cost data is often distributed across billing exports, accounts,
subscriptions, services and engineering teams. This makes it difficult for
finance and engineering leaders to understand what is driving expenditure,
identify unexpected changes and assign costs to accountable teams.

## Project goal

Build an end-to-end analytics platform that ingests simulated cloud billing
data, validates and transforms it through Bronze, Silver and Gold layers,
and exposes decision-ready cloud-cost metrics in Power BI.

## Target users

- FinOps analysts
- Engineering managers
- Finance business partners, CFO
- Technology leadership

## MVP analytical questions

1. What is the total cloud cost by month?
2. Which teams, projects and services generate the highest costs?
3. How does actual monthly cost compare with the previous month?
4. Which cost categories show unusually large increases?
5. What proportion of spending can be allocated to a team or project?

### Data quality

The pipeline currently validates:

- required field completeness
- duplicate removal
- categorical standardization
- allocation completeness
- Bronze/Silver row-count changes
- Silver-to-Gold cost reconciliation

## Pipeline status

✅ Synthetic cloud cost generation  
✅ Bronze ingestion and metadata  
✅ Silver cleaning and standardization  
✅ Duplicate and allocation handling  
✅ Gold monthly cost model  
✅ Silver-to-Gold cost reconciliation  
✅ Data quality framework  
⬜ dbt models and tests  
⬜ Power BI dashboard

