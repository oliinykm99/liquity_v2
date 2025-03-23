def clean_troveRequiredData(**kwargs):
    ti = kwargs['ti']
    troveRequiredData = ti.xcom_pull(task_ids='extract_requiredTroveData_task')

    results = {}

    for pool, troves in troveRequiredData.items():
        try:
            results[pool] = {
                trove_id: {
                    'trove_debt': trove_data['trove_debt'] / 1e18,
                    'trove_coll': trove_data['trove_coll'] / 1e18,
                    'trove_rate': trove_data['trove_rate'] / 1e18
                }
                for trove_id, trove_data in troves.items()
            }
        except Exception as e:
            print(f"Error cleaning trove data for pool {pool}: {e}")

    return results