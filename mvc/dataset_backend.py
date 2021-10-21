import dataset
from sqlalchemy.exc import NoSuchTableError, IntegrityError
import mvc_exceptions as mvc_exc

conn = dataset.connect('sqlite:///:memory:') # FUNKTIONIERT SO NOCH NICHT!

def create_table(conn, table_name):
    try: 
        conn.load_table(table_name)
        print(f'loaded table {table_name}')
    except NoSuchTableError as e:
        print(f'Table {table_name} does not exist. It will be created now')
        conn.get_table(table_name, primary_id='name', primary_type='String')
        print(f'Created table {table_name}')

def insert_one(conn, name, price, quanitity, table_name):
    table = conn.load_table(table_name)
    try:
        table.insert(dict(name=name, price=price, quanitity=quanitity))
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            f'"{name}" already stored in table "{table.table.name}"')

def insert_many(conn, items, table_name):
    table = conn.load_table(table_name)
    try:
        for x in items:
            table.insert(dict(
                name=x['name'], price=x['price'], quantity=x['quantity']))
    except IntegrityError as e:
        print('At least one in {} was already stored in table "{}".\nOriginal '
              'Exception raised: {}'
              .format([x['name'] for x in items], table.table.name, e))

def select_one(conn, name, table_name):
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        return dict(row)
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t read "{name}" because it\'s not stored in table "{table.table.name}"')

def select_all(conn, table_name):
    table = conn.load_table(table_name)
    rows = table.all()
    return list(map(lambda x: dict(x), rows))

def update_one(conn, name, price, quantity, table_name):
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        item = {'name': name, 'price': price, 'quantity': quantity}
        table.update(item, keys=['name'])
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t update "{name}" because it\'s not stored in table "{table.table.name}"')

def delete_one(conn, name, table_name):
    table = conn.load_table(table_name)
    row = table.find_one(name=name)
    if row is not None:
        table.delete(name=name)
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t delete "{name}" because it\'s not stored in table "{table.table.name}"')

# main function
def main():
    table_name = 'items'
    conn = dataset.connect('sqlite:///:memory:')

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