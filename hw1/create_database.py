import sqlite3

with open('stuff/cleaned_table.txt', 'r', encoding='utf-8') as file:
	ingredients = file.read().strip('\n').split('\n')

conn = sqlite3.connect('food.db')
cur = conn.cursor()

cur.execute('CREATE TABLE ingredients (product text, kсal real)')

for ing in ingredients[1:]:
	ing = ing.split('\t')
	request = 'INSERT INTO ingredients VALUES (\'%s\', %s)' % (ing[0], float(ing[4]))

	cur.execute(request)

conn.commit()
conn.close()
