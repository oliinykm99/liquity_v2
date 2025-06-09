def clean_activeTVL_USD(**kwargs):
    ti = kwargs['ti']
    clean_activeTVL = ti.xcom_pull(task_ids='clean_activeTVL_task')
    clean_prices = ti.xcom_pull(task_ids='clean_prices_task')

    pool_to_price_feed = dict(zip(clean_activeTVL.keys(), clean_prices.keys()))

    results = {}
    for pool, priceFeed in pool_to_price_feed.items():
        try:
            results[pool] = clean_activeTVL[pool] * clean_prices[priceFeed]
        except Exception as e:
            print(f"Error cleaning Active TVL (in USD) for {pool}: {e}")
    return results