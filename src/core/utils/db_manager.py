import psycopg2


class DBManager:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(self.db_url)
        self.cursor = self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS LiquityV2 (
            active_pool TEXT,
            TVL NUMERIC,
            TVL_USD NUMERIC,
            debt NUMERIC,
            stabilityTVL NUMERIC,
            price NUMERIC,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY (active_pool, timestamp)  -- Ensures one entry per active_pool per timestamp
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def create_trove_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS LiquityTroveData (
            trove_manager TEXT,
            trove_id TEXT,
            trove_owner TEXT,
            trove_coll NUMERIC,
            trove_cr NUMERIC,
            trove_debt NUMERIC,
            trove_rate NUMERIC,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY (trove_manager, trove_id, timestamp)
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def store_liquity_data(self, data):
        query = """
        INSERT INTO LiquityV2 (active_pool, TVL, TVL_USD, debt, stabilityTVL, price, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, NOW());
        """
        
        for active_pool, values in data.items():
            self.cursor.execute(
                query,
                (
                    active_pool,
                    values['TVL'],
                    values['TVL_USD'],
                    values['debt'],
                    values['stabilityTVL'],
                    values['price']
                )
            )
        self.connection.commit()

    def store_trove_data(self, data):
        query = """
        INSERT INTO LiquityTroveData (trove_manager, trove_id, trove_owner, trove_coll, trove_cr, trove_debt, trove_rate, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (trove_manager, trove_id, timestamp) DO NOTHING;
        """

        for trove_manager, troves in data.items():
            for trove_id, values in troves.items():
                self.cursor.execute(
                    query,
                    (
                        trove_manager,
                        trove_id,
                        values['trove_owner'],
                        values['trove_coll'],
                        values['trove_cr'],
                        values['trove_debt'],
                        values['trove_rate']
                    )
                )
        self.connection.commit()
