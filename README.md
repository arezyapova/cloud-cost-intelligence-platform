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

## Current status

- Business problem defined
- MVP analytical questions defined
- Initial data contract created
- Repository structure created
- Bronze ingestion notebook initialized

## Next session

Obtain or generate the sample cloud billing dataset, load it into Databricks,
add ingestion metadata and write the first Bronze Delta table.

## Pipeline status

✅ Synthetic cloud cost generation  
✅ Raw CSV ingestion  
✅ Explicit Spark schema  
✅ Bronze ingestion metadata  
✅ Basic data-quality validation  
✅ Bronze Delta table  

Next: Silver cleaning and standardization.