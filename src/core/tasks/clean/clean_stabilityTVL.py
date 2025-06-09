def clean_stabilityTVL(**kwargs):
    ti = kwargs['ti']
    stability = ti.xcom_pull(task_ids='fetch_stabilityTVL_task')

    results = {}
    for pool in stability.keys():
        try:
            results[pool] = stability[pool] / 1e18
        except Exception as e:
            print(f"Error cleaning TVL for {pool}: {e}")
    return results