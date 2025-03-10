from config import activePools
from config import priceFeeds
from config import stabilityPools

def aggregate_pools(**kwargs):
    ti = kwargs['ti']
    
    clean_activeTVL = ti.xcom_pull(task_ids='clean_activeTVL_task')
    clean_prices = ti.xcom_pull(task_ids='clean_prices_task')
    clean_activeTVL_USD = ti.xcom_pull(task_ids='clean_activeTVL_USD_task')
    clean_activeDebt = ti.xcom_pull(task_ids='clean_activeDEBT_task')
    clean_stabilityTVL = ti.xcom_pull(task_ids='clean_stabilityTVL_task')

    pool_to_stability_pool = dict(zip(activePools, stabilityPools))
    pool_to_price_feed = dict(zip(activePools, priceFeeds))

    results = {}
    for activePool in activePools:
        try:
            stabilityPool = pool_to_stability_pool[activePool]
            priceFeed = pool_to_price_feed[activePool]

            results[activePool] = {
                'TVL': clean_activeTVL.get(activePool, 0),
                'TVL_USD': clean_activeTVL_USD.get(activePool, 0),
                'debt': clean_activeDebt.get(activePool, 0),
                'stabilityTVL': clean_stabilityTVL.get(stabilityPool, 0),
                'price': clean_prices.get(priceFeed, 0)
            }
        except Exception as e:
            print(f"Error processing data for {activePool}: {e}")

    return results