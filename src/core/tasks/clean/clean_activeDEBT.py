from config import activePools

def clean_activeDEBT(**kwargs):
    ti = kwargs['ti']
    activeDebt = ti.xcom_pull(task_ids='fetch_activeDEBT_task')

    results = {}
    for pool in activePools:
        try:
            results[pool] = activeDebt[pool] / 1e18
        except Exception as e:
            print(f"Error cleaning Active Debt for {pool}: {e}")
    return results