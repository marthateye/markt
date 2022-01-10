from DB.DB import DB


class ProductDBModelAdapter:
    def __init__(self):
        self.table_name = "Products"
        # create DB
        self.create_table()

    def table_columns(self):
        columns = ['Id',
                    'Store',
                    'Brand',
                    'Name',
                    'ShortName',
                    'Price',
                    'Currency',
                    'Composition',
                    'DeliveryTime',
                    'Size',
                    'Link',
                    'Image',
                    'Description',
                    'Keyword',
                    'CreatedAt',
                    'LastModified']
        return columns

    def create_table(self):
        try:
            db = DB()
            connection = db.create_connection()
            sql = '''CREATE TABLE {} (
                                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Store VARCHAR(255),
                                Brand TEXT,
                                Name TEXT,
                                ShortName VARCHAR(255),
                                Price DOUBLE,
                                Currency VARCHAR(20),
                                Composition TEXT,
                                DeliveryTime TEXT,
                                Size TEXT,
                                Link TEXT,
                                Image TEXT,
                                Description TEXT,
                                Keyword TEXT,
                                CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP,
                                LastModified TEXT DEFAULT CURRENT_TIMESTAMP
                            );
                        '''.format(self.table_name)

            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            connection.close()
        except Exception as e:
            print(e)
            return False

        return True

    def merge_products(self, product):

        try:

            db = DB()
            connection = db.create_connection()
            is_product_exists = self.try_find_product(connection, product)

            if is_product_exists == True:
                self.update_product(connection, product)
            else:
                self.insert_product(connection, product)

            connection.close()
        except Exception as e:
            print(e)
            return False

        return True

    def insert_product(self, sql_connection, product):

        try:
            COLUMNS = ''
            VALUES_STR = ''
            VALUES_LIST = []

            for key in product:
                if COLUMNS != '':
                    COLUMNS += ','
                    VALUES_STR += ','

                COLUMNS += str(key)
                VALUES_STR += '?'
                VALUES_LIST.append(product[key])

            VALUES = tuple(VALUES_LIST)

            connection = sql_connection
            cursor = connection.cursor()

            sql = 'INSERT INTO {} ({}) VALUES ({});'.format(self.table_name, COLUMNS, VALUES_STR)

            cursor.execute(sql, VALUES)
            connection.commit()
        except Exception as e:
            print(e)
            return False

        return True

    def try_find_product(self, sql_connection, product):
        store = product['Store']
        brand = product['Brand']
        name = product['Name']

        cursor = sql_connection.cursor()
        sql = 'SELECT * FROM {} WHERE Store=? AND Brand=? AND Name=?'.format(self.table_name)
        cursor.execute(sql, (store, brand, name))
        rows = cursor.fetchall()
        count_rows = len(rows)

        if count_rows == 0:
            return False

        return True

    def update_product(self, sql_connection, product):
        try:
            COLUMNS = ''
            SKIP = ['Store', 'Brand', 'Name']
            VALUES_LIST = []

            for key in product:

                if key not in SKIP:

                    if COLUMNS != '':
                        COLUMNS += ','

                    COLUMNS += " {}=? ".format(key)
                    VALUES_LIST.append(product[key])

            VALUES_LIST.append(product['Store'])
            VALUES_LIST.append(product['Brand'])
            VALUES_LIST.append(product['Name'])

            VALUES = tuple(VALUES_LIST)

            connection = sql_connection
            cursor = connection.cursor()

            sql = "UPDATE {} SET {}, LastModified=date('now') WHERE Store=? AND Brand=? AND Name=?".format(self.table_name, COLUMNS)

            cursor.execute(sql, VALUES)
            connection.commit()
        except Exception as e:
            print(e)
            return False

        return True

    def get_products(self, WHERE=None, Limit=None):

        try:
            columns = self.table_columns()
            db = DB()
            connection = db.create_connection()
            cursor = connection.cursor()
            sql = 'SELECT * FROM ' + self.table_name
            VALUES_LIST = []

            if WHERE != None:
                where_clause_response = db.where_clause_builder_split(WHERE, columns)
                VALUES_LIST = where_clause_response[1]
                if len(VALUES_LIST) > 0:
                    sql += ' WHERE {}'.format(where_clause_response[0])

                if WHERE.get('Sort') != None:
                    if str(WHERE.get('Sort')) in columns:
                        sql += ' ORDER BY {}'.format(WHERE.get('Sort'))

            if Limit != None:
                sql += ' LIMIT {}'.format(Limit)

            VALUES = tuple(VALUES_LIST)

            print(sql)

            cursor.execute(sql,VALUES)
            rows = cursor.fetchall()

            products = []
            for row in rows:
                products.append({
                    'Id': row[0],
                    'Store': row[1],
                    'Brand': row[2],
                    'Name': row[3],
                    'ShortName': row[4],
                    'Price': row[5],
                    'Currency': row[6],
                    'Composition': row[7],
                    'DeliveryTime': row[8],
                    'Size': row[9],
                    'Link': row[10],
                    'Image': row[11],
                    'Description': row[12],
                    'Keyword': row[13],
                    'CreatedAt': row[14],
                    'LastModified': row[15],
                })

            connection.close()
        except Exception as e:
            print(e)
            return None

        return products

    def get_unique(self, table_column='Store'):

        try:
            db = DB()
            connection = db.create_connection()
            cursor = connection.cursor()
            sql = 'SELECT DISTINCT {} FROM {}'.format(table_column,self.table_name)
            cursor.execute(sql)
            rows = cursor.fetchall()

            stores = []
            for row in rows:
                stores.append(row[0])

            connection.close()
        except Exception as e:
            print(e)
            return None

        return stores