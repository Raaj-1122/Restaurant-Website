from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = "restaurant_secret_key"
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route('/menu')
def menu():

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM food_items")
    foods = cursor.fetchall()

    conn.close()

    return render_template(
        "menu.html",
        foods=foods
    )

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']

        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO reservations
        (name,email,phone,date,time)
        VALUES (?,?,?,?,?)
        """, (name, email, phone, date, time))

        conn.commit()
        conn.close()

        return render_template(
            "reservation.html",
            success=True
        )

    return render_template(
        "reservation.html",
        success=False
    )

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":

            session['admin'] = True

            return redirect(url_for('admin'))

        return render_template(
            "admin_login.html",
            error="Invalid Username or Password"
        )

    return render_template("admin_login.html")

@app.route('/admin')
def admin():

    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservations")
    reservations = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        reservations=reservations
    )

@app.route('/logout')
def logout():

    session.pop('admin', None)

    return redirect('/')

@app.route('/food-management', methods=['GET', 'POST'])
def food_management():

    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']

        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT INTO food_items
                           (name, category, price)
                       VALUES (?, ?, ?)
                       """, (name, category, price))

        conn.commit()
        conn.close()
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM food_items")
        foods = cursor.fetchall()

        conn.close()

        return render_template(
            "food_management.html",
            foods=foods
        )

    return render_template("food_management.html")

@app.route('/order/<int:food_id>', methods=['GET', 'POST'])
def order(food_id):

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM food_items WHERE id=?",
        (food_id,)
    )

    food = cursor.fetchone()

    if request.method == 'POST':
        customer_name = request.form['customer_name']
        phone = request.form['phone']

        quantity = 1
        address = "Not Provided"

        cursor.execute("""
                       INSERT INTO orders
                           (food_name, customer_name, phone, quantity, address)
                       VALUES (?, ?, ?, ?, ?)
                       """,
                       (
                           food[1],
                           customer_name,
                           phone,
                           quantity,
                           address
                       ))

        conn.commit()
        conn.close()

        return render_template(
            "order.html",
            food=food,
            success=True
        )

    conn.close()

    return render_template(
        "order.html",
        food=food,
        success=False
    )

if __name__ == '__main__':
    app.run(debug=True)