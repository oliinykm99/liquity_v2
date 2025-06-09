def clean_prices(**kwargs):
    ti = kwargs['ti']
    prices = ti.xcom_pull(task_ids='fetch_price_task')

    results = {}
    for pool in prices.keys():
        try:
            results[pool] = prices[pool] / 1e18
        except Exception as e:
            print(f"Error cleaning prices for {pool}: {e}")
    return results