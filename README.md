# Liquity V2 Data Pipeline

This repository contains an Apache Airflow DAG for fetching, cleaning, and aggregating data related to Liquity V2 active pools, stability pools, and collateral prices.

## Current DAG

The current DAG performs the following tasks:
- Fetches data for active pools, stability pools, and price feeds.
- Cleans the fetched data.
- Aggregates the data by active pools into a nested dictionary structure.

Below is a screenshot of the current DAG for Liquity V2:
![Current DAG](images/dag_general.png)

Below is a screenshot of the current DAG for Liquity V2 Troves:
![Current DAG Troves](images/dag_troves.png)

Below is a screenshot of the current table for Liquity V2 (General):
![Current Database](images/db_general.png)
## Future Work

We plan to extend the pipeline with the following enhancements:
- **Troves DAG:**
  - Upload troves data to a cloud data warehouse for efficient storage and analysis.
- **Data Validation and Quality:**
  - Introduce validation checks to ensure data integrity.
  - Implement data quality monitoring for both DAGs.
- **Optimization:**
  - Improve the performance of existing DAGs by optimizing queries and task execution.
  - Refactor code for better scalability and maintainability.
