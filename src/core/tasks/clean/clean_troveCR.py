def clean_troveCR(**kwargs):
    ti = kwargs['ti']
    troveCRs = ti.xcom_pull(task_ids='fetch_troveCR_task')

    results = {}
    for pool, troves in troveCRs.items():
        try:
            results[pool] = {trove_id: cr / 1e18 for trove_id, cr in troves.items()}
        except Exception as e:
            print(f"Error cleaning troveCR for pool {pool}: {e}")

    return results