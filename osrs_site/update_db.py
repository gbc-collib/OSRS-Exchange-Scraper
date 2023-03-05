import requests
import sqlite3

"""Script to make call to the realtime API and save item info, 
this is a seperate file because lots of scripts want item ids, examine text etc. but not price data
since we are not saving price data we will never have to update this except when new items are added to the game.
"""


TABLE_PARAMETER = "{TABLE_PARAMETER}"
DROP_TABLE_SQL = f"DROP TABLE {TABLE_PARAMETER};"
GET_TABLES_SQL = "SELECT name FROM sqlite_schema WHERE type='table';"

class SqliteUtil:

    @staticmethod
    def delete_all_tables(con):
        tables = SqliteUtil.get_tables(con)
        SqliteUtil.delete_tables(con, tables)

    @staticmethod
    def get_tables(con):
        cur = con.cursor()
        cur.execute(GET_TABLES_SQL)
        tables = cur.fetchall()
        cur.close()
        return tables

    @staticmethod
    def delete_tables(con, tables):
        cur = con.cursor()
        for table, in tables:
            sql = DROP_TABLE_SQL.replace(TABLE_PARAMETER, table)
            cur.execute(sql)
        cur.close()


    @staticmethod
    def connect(data):
        columns = list(data[1].keys())  # Pull columns from json and remove unused ones
        columns.remove("lowalch")
        connection = sqlite3.connect("item_info.db")
        columns = ", ".join(columns)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS items_info (item_examine, item_id, item_members, item_limit, item_value, item_highalch, item_icon, item_name);")
        connection.commit()
        return connection


def populate_database(connection, data):
    columns = list(data[1].keys())  # Pull columns from json and remove useless ones
    columns.remove("lowalch")
    joined_columns = "item_" + ", item_".join(columns)
    placeholders = ", ".join("coalesce(:{}, 0)".format(col) for col in columns)
    # not concerned about sanitizing sql because this query will never come from user input
    query = 'INSERT INTO items_info (%s) VALUES (%s)' % (joined_columns, placeholders)
    for item_data in data:
        for key in columns:
            if key not in item_data:
                item_data[key] = None
        connection.execute(query, item_data)
        connection.commit()
    return connection


def main(args):
    item_url = 'http://prices.runescape.wiki/api/v1/osrs/mapping'
    headers = {
        'User-Agent': 'gbc_collib\'s amateur price tracker',
        'From': 'collinstasiak@gmail.com'
    }

    raw_data = requests.get(item_url, headers=headers, stream=True)
    data = raw_data.json()
    connection = SqliteUtil.connect(data)
    connection = populate_database(connection, data)
    cur = connection.cursor()
    cur.execute("PRAGMA database_list")
    rows = cur.fetchall()
    for row in rows:
        print(row[0], row[1], row[2])
    connection.close()

if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
