def extract_requiredTroveData(**kwargs):
    ti = kwargs['ti']
    troveCRs = ti.xcom_pull(task_ids='fetch_troveData_task')

    results = {}

    for pool, troves in troveCRs.items():
        try:
            results[pool] = {
                trove_id: {
                    'trove_debt': trove_data[0],  # Debt
                    'trove_coll': trove_data[1],  # Collateral
                    'trove_rate': trove_data[6]   # Rate
                }
                for trove_id, trove_data in troves.items()
            }
        except Exception as e:
            print(f"Error extracting required trove data for pool {pool}: {e}")

    return results