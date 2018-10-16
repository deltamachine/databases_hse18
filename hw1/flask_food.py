import re
import sqlite3
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)


def prep_request(food):
    food = re.sub('\r', '', food)
    food = re.sub('\n', ' ', food)
    ings = food.split(';')[:-1]
    to_find = {}

    for elem in ings:
        elem = elem.split(': ')
        product = elem[0].strip(' ').lower()
        amount = re.sub(' .*?$', '', elem[1].strip(' '))
        to_find[product] = amount

    return to_find


def search_in_base(req):
    to_find = prep_request(req)
    not_found = []
    output = 0

    conn = sqlite3.connect('food.db')
    cur = conn.cursor()

    for key, value in to_find.items():
        words = key.split(' ')
        like = ''

        for word in words:
            like += "product like '%" + word + "%' AND "

        like = like.strip(' AND ')

        req = "SELECT kcal FROM ingredients WHERE %s;" % (like)
        cur.execute(req)
        res = cur.fetchall()

        if res == []:
            not_found.append(key)
        else:
            hun_kcal = res[0][0]
            tot_kcal = float(value) * hun_kcal / 100
            output += tot_kcal
    
    conn.close()

    return output, not_found


def return_products():
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()

    req = 'SELECT * FROM ingredients;'
    cur.execute(req)
    res = cur.fetchall()

    products = {elem[0]: elem[1] for elem in res}
    products = sorted(products.items(), key=lambda kv: kv[0], reverse=False) 

    conn.close()

    return products


def add(p, k):
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    req = "INSERT INTO ingredients (product, kcal) VALUES ('%s', %s);" % (p, float(k))
    cur.execute(req)    
    conn.commit()
    conn.close()


def delete(p):
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    req = "DELETE FROM ingredients WHERE product='%s';" % (p)
    cur.execute(req)    
    conn.commit()
    conn.close()


def edit(to_edit, p, k):
    conn = sqlite3.connect('food.db')
    cur = conn.cursor()
    req = "UPDATE ingredients SET product='%s', kcal=%s where product='%s';" % (p,float(k), to_edit)
    cur.execute(req)    
    conn.commit()
    conn.close()


@app.route('/')
def index():
    products = return_products()

    if request.args:
        food = request.args['food']
        output, not_found = search_in_base(food)
        len_nf = len(not_found)
        not_found = '"' + '", "'.join(not_found) + '"'

        return render_template('results.html', output=str(output),
                                               not_found=not_found,
                                               len_nf=len_nf)
    
    return render_template('index.html', products=products)


@app.route('/add', methods=['GET', 'POST'])
def add_object():
    products = return_products()

    if request.method == 'POST':
        p = request.form['pr']
        k = request.form['kc']
        add(p, k)

        return redirect(url_for('add_object'))

    return render_template('add_object.html', products=products)


@app.route('/delete', methods=['GET', 'POST'])
def delete_object():
    products = return_products()

    if request.method == 'POST':
        p = request.form['delete']
        delete(p)

        return redirect(url_for('delete_object'))

    return render_template('delete_object.html', products=products)


@app.route('/edit', methods=['GET', 'POST'])
def edit_object():
    products = return_products()

    if request.method == 'POST':
        to_edit = request.form['to_edit']
        p = request.form['pr']
        k = request.form['kc']
        
        edit(to_edit, p, k)

        return redirect(url_for('edit_object'))

    return render_template('edit_object.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
