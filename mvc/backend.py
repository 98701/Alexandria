import mvc_exceptions as mvc_exc

items = []

# create
def create_items(app_items):
    global items
    items = app_items

def create_item(name, price, quantity):
    global items
    results = [x for x in items if x['name'] == name]
    if results:
        raise mvc_exc.ItemAlreadyStored(f'"{name}" already stored!')
    else:
        items.append({'name': name, 'price': price, 'quantity': quantity})


# read
def read_item(name):
    global items
    myitems = [x for x in items if x['name'] == name]
    if myitems:
        return myitems[0]
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t read "{name}" because it\'s not stored')
            
def read_items():
    global items
    return [item for item in items]


# update
def update_item(name, price, quantity):
    global items
    idxs_items = [x for x in enumerate(items) if x[1]['name'] == name]
    if idxs_items:
        i, item_to_update = idxs_items[0][0], idxs_items[0][1]
        items[i] = {'name': name, 'price': price, 'quantity': quantity}
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t update "{name}" because it\'s not stored')


# delete
def delete_item(name):
    global items
    idxs_items = [x for x in enumerate(items) if x[1]['name'] == name]
    if idxs_items:
        i, item_to_delete = idxs_items[0][0], idxs_items[0][1]
        del items[i]
    else:
        raise mvc_exc.ItemNotStored(
            f'Can\'t delete "{name}" because it\'s not stored')

def main():

    my_items = [
        {'name': 'bread', 'price': 0.5, 'quantity': 20},
        {'name': 'milk', 'price': 1.0, 'quantity': 10},
        {'name': 'wine', 'price': 10.0, 'quantity': 5}
    ]

    # CREATE
    create_items(my_items)
    create_item('beer', 3.0, 15)
    #create_item('beer', 3.0, 15)

    # READ
    print('READ items')
    print(read_items())
    #print(read_item('chocolate'))

    # UPDATE
    print("Update")
    update_item('wine', 5, 5)
    print(read_item('wine'))
    #update_item('water', 5, 5)

    # DELETE
    print("DELETE")
    delete_item('milk')
    print(read_items())
    delete_item('coffee')


if __name__ == '__main__':
    main()
