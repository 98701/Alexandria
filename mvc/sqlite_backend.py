import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import mvc_exceptions as mvc_exc

DB_name = 'myDB'

# connect to database, either in memory or .db file
def connect_to_db(db=None):
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB')
    else:
        mydb = f'{db}.db'
        print('New connection to SQLite DB')
    connection = sqlite3.connect(mydb)
    return connection

def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You are trying to disconnect from a wrong DB")
    if conn is not None:
        conn.close()

# decorator to test the connection when executing the other functions
def connect(func):
    def inner_func(conn, *args, **kwargs):
        try:
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(DB_name) # if it fails, it reopens the connection
        return func(conn, *args, **kwargs)
    return inner_func

# clean input string to prevent SQL injection
def scrub(input_string):
    return ''.join(k for k in input_string if k.isalnum())  

# create table statement
@connect
def create_table(conn, table_name):
    table_name = scrub(table_name)
    sql = f'CREATE TABLE {table_name} (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
        'name TEXT UNIQUE, price REAL, quantity INTEGER)'
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)     


# create
@connect 
def insert_one(conn, name, price, quantity, table_name):
    table_name = scrub(table_name)
    sql = f"INSERT INTO {table_name} ('name', 'price', 'quantity') VALUES (?, ?, ?)"
    try:
        conn.execute(sql, (name, price, quantity))
        conn.commit()
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            f'{e}: {name} already stored in table {table_name}')

@connect 
def insert_many(conn, items, table_name):
    table_name = scrub(table_name)
    sql = f"INSERT INTO {table_name} ('name', 'price', 'quantity') VALUES (?, ?, ?)"
    entries = []
    for x in items:
        entries.append((x['name'], x['price'], x['quantity']))
    try:
        conn.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in table "{}"'
              .format(e, [x['name'] for x in items], table_name))

# read
def tuple_to_dict(mytuple): # each query returns a tuple that must be converted to dict
    mydict = {}
    mydict['id'] = mytuple[0]
    mydict['name'] = mytuple[1]
    mydict['price'] = mytuple[2]
    mydict['quantity'] = mytuple[3]
    return mydict

@connect 
def select_one(conn, item_name, table_name):
    table_name = scrub(table_name)
    item_name = scrub(item_name)
    sql = f'SELECT * FROM {table_name} WHERE name="{item_name}"'
    c = conn.execute(sql)
    result = c.fetchone()
    if result is not None:
        return tuple_to_dict(result)
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t read {item_name} because it\'s not stored in table "{table_name}"')

@connect 
def select_all(conn, table_name):
    table_name = scrub(table_name)
    sql = f'SELECT * FROM {table_name}'
    c = conn.execute(sql)
    results = c.fetchall()
    return [tuple_to_dict(x) for x in results]

# update
@connect
def update_one(conn, name, price, quantity, table_name):
    table_name = scrub(table_name)
    sql_check = f'SELECT EXISTS(SELECT 1 FROM {table_name} WHERE name=? LIMIT 1)'
    sql_update = f'UPDATE {table_name} SET price=?, quantity=? WHERE name=?'
    c = conn.execute(sql_check, (name,))
    result = c.fetchone()
    if result[0]:
        c.execute(sql_update, (price, quantity, name))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t update "{name}" because it\'s not stored in table "{table_name}"')

# delete
@connect
def delete_one(conn, name, table_name):
    table_name = scrub(table_name)
    sql_check = f'SELECT EXISTS(SELECT 1 FROM {table_name} WHERE name=? LIMIT 1)'
    sql_delete = f'DELETE FROM {table_name} WHERE name=?'
    c = conn.execute(sql_check, (name,))
    result = c.fetchone()
    if result[0]:
        c.execute(sql_delete, (name,))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t delete "{name}" because it\'s not stored in table "{table_name}"')

# main function
def main():
    table_name = 'items'
    conn = connect_to_db() # in-memory database
    # conn = connect_to_tb(DB_name) # physical database

    create_table(conn, table_name)

    my_items = [
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'milk', 'price': 1.0, 'quantity': 10},
        {'name': 'wine', 'price': 10.0, 'quantity': 5},
    ]

    # CREATE
    insert_many(conn, my_items, table_name='items')
    insert_one(conn, 'beer', price=2.0, quantity=5, table_name='items')

    # READ
    print('SELECT milk')
    print(select_one(conn, 'milk', table_name='items'))
    print('SELECT all')
    print(select_all(conn, table_name='items'))

    # UPDATE
    print('UPDATE bread, SELECT bread')
    update_one(conn, 'bread', price=1.5, quantity=5, table_name='items')
    print(select_one(conn, 'bread', table_name='items'))

    # DELETE
    print('DELETE beer, SELECT all')
    delete_one(conn, 'beer', table_name='items')
    print(select_all(conn, table_name='items'))

    # save (commit) the changes
    # conn.commit()

    # close connection
    conn.close()

if __name__ == '__main__':
    main()    
