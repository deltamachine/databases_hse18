import re

with open('table.txt', 'r', encoding='utf-8') as file:
	file = file.read()

table = re.sub('[А-Я]{2,}.*?\n', '', file)
table = re.sub('-', '0', table)
table = re.sub(',', '.', table)
table = table.strip('\n').split('\n')

with open('cleaned_table.txt', 'w', encoding='utf-8') as file:
	file.write('Продукт\tБелки\tЖиры\tУглеводы\tКкал\n')

	for i in range(0, len(table), 6):
		try:
			file.write('%s\t%s\t%s\t%s\t%s\n' % (table[i].lower(), table[i+2], table[i+3], table[i+4], table[i+5]))
		except:
			print(table[i])