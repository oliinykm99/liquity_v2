def clean_activeTVL(**kwargs):
    ti = kwargs['ti']
    activeTVL = ti.xcom_pull(task_ids='fetch_activeTVL_task')

    results = {}
    for pool in activeTVL.keys():
        try:
            results[pool] = activeTVL[pool] / 1e18
        except Exception as e:
            print(f"Error cleaning Active TVL for {pool}: {e}")
    return results