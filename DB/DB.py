import sqlite3
from sqlite3 import Error


class DB:
    def __init__(self):
        self.path = "markt_pilot.sqlite.db"

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by self.path
        :return: Connection object or None
        """
        connection = None
        try:
            connection = sqlite3.connect(self.path)
        except Error as e:
            print(e)

        return connection

    def where_clause_builder(self, WHERE_DICT):
        where_clause_string = ''
        VALUES_LIST = []

        for key in WHERE_DICT:
            if where_clause_string != '':
                where_clause_string += ' AND '

            where_clause_string += ' {} LIKE ? '.format(str(key))
            VALUES_LIST.append('%{}%'.format(WHERE_DICT[key]))

        return where_clause_string, VALUES_LIST

    def where_clause_builder_split(self, WHERE_DICT, COLUMNS = None, delimeter='_'):
        where_clause_string = ''
        VALUES_LIST = []

        for key in WHERE_DICT:
            if COLUMNS != None:
                is_a_column = str(key) in COLUMNS
                if is_a_column == False:
                    continue

            if where_clause_string != '':
                where_clause_string += ' AND '

            search_strings = str(WHERE_DICT[key]).split(delimeter)

            if len(search_strings) == 1:
                where_clause_string += ' {} LIKE ? '.format(str(key))
                VALUES_LIST.append('%{}%'.format(WHERE_DICT[key]))
            else:
                param_string = ''
                for param in search_strings:
                    if param_string!= '':
                        param_string += ' OR '

                    param_string += ' {} LIKE ? '.format(str(key))
                    VALUES_LIST.append('%{}%'.format(param))

                where_clause_string += '( {} )'.format(param_string)

        return where_clause_string, VALUES_LIST
