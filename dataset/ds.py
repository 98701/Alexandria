import sqlite3
import dataset

# CONNECT TO DB (CREATE IF NOT EXISTS)
connection = sqlite3.connect("users.db")
db = dataset.connect('sqlite:///users.db')

# CREATE (IF NOT EXISTS)
table = db['users']

# ADD DATA
#table.insert({'name': 'TEST', 'newcolumn': 'blabla'})  # unknown columns are created

# READ
users = table.find()
daniel = table.find(name='Daniel')
young = table.find(table.table.columns.age < 100)
young = db.query('SELECT * FROM users WHERE AGE < 100')

# UPDATE
#table.update({'name': 'Daniel', 'password': 'hexagon'}, ['name'])

# DELETE
table.delete(name=['TEST', 'Björn'])

#print([x for x in result])
# for row in users:
#     if row['name'] == 'Daniel':
#         print(row['name'], row['age'])
print([x['name'] for x in table.distinct('name')])

