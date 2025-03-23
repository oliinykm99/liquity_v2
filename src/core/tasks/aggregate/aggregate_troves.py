def aggregate_troves(**kwargs):
    ti = kwargs['ti']
    
    troveOwners = ti.xcom_pull(task_ids='fetch_troveOwner_task')
    troveRequiredDatas = ti.xcom_pull(task_ids='clean_troveRequiredData_task')
    troveCRs = ti.xcom_pull(task_ids='clean_troveCR_task')

    results = {}

    for pool in troveOwners.keys():
        results[pool] = {}

        for trove_id in troveOwners.get(pool, {}):
            try:
                results[pool][trove_id] = {
                    'trove_id': trove_id,
                    'trove_owner': troveOwners[pool].get(trove_id, None),
                    'trove_debt': troveRequiredDatas[pool][trove_id]['trove_debt'],
                    'trove_coll': troveRequiredDatas[pool][trove_id]['trove_coll'],
                    'trove_rate': troveRequiredDatas[pool][trove_id]['trove_rate'],
                    'trove_cr': troveCRs[pool].get(trove_id, None)
                }
            except Exception as e:
                print(f"Error aggregating data for pool {pool}, trove {trove_id}: {e}")

    return results