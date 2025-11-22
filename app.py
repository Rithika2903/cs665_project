from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import check_password_hash
import sqlite3, os

app = Flask(__name__)

# Use env var in production; fallback random key for dev
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32))

DB_NAME = "car_rental.db"


# -------------------- DB UTILS --------------------
def get_conn():
    """Return a new SQLite connection with foreign keys enforced and row access by name."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        with open("schema.sql", "r", encoding="utf-8") as f:
            cur.executescript(f.read())
        with open("seed_data.sql", "r", encoding="utf-8") as f:
            cur.executescript(f.read())


def require_login():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return None


# -------------------- LOGIN / LOGOUT --------------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""

        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, password FROM users WHERE email = ?", (email,))
            user = cur.fetchone()

        if user:
            stored = user["password"] or ""
            # Backward-compatible: if it's a werkzeug hash, verify; otherwise compare plaintext
            ok = (stored.startswith("pbkdf2:") and check_password_hash(stored, password)) or (stored == password)
            if ok:
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                return redirect(url_for("dashboard"))

        error = "Invalid credentials"

    return render_template("login.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------- DASHBOARD --------------------
@app.route("/dashboard")
def dashboard():
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) AS c FROM cars")
        total_cars = cur.fetchone()["c"]

        cur.execute("SELECT COUNT(*) AS c FROM customers")
        total_customers = cur.fetchone()["c"]

        cur.execute("SELECT COUNT(*) AS c FROM rentals")
        total_rentals = cur.fetchone()["c"]

        cur.execute("SELECT COUNT(*) AS c FROM payments")
        total_payments = cur.fetchone()["c"]

    return render_template(
        "dashboard.html",
        total_cars=total_cars,
        total_customers=total_customers,
        total_rentals=total_rentals,
        total_payments=total_payments,
    )


# -------------------- CARS --------------------
@app.route("/cars")
def cars():
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cars")
        cars = cur.fetchall()

    return render_template("cars.html", cars=cars)


@app.route("/cars/add", methods=["GET", "POST"])
def add_car():
    guard = require_login()
    if guard:
        return guard

    if request.method == "POST":
        brand = (request.form.get("brand") or "").strip()
        model = (request.form.get("model") or "").strip()
        year = int(request.form.get("year") or 0)
        rate = float(request.form.get("rate") or 0)
        status = (request.form.get("status") or "").strip()

        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO cars (brand, model, year, rate, status) VALUES (?, ?, ?, ?, ?)",
                (brand, model, year, rate, status),
            )
        return redirect(url_for("cars"))

    return render_template("add_edit_car.html", car=None)


@app.route("/cars/edit/<int:car_id>", methods=["GET", "POST"])
def edit_car(car_id):
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
        car = cur.fetchone()
        if not car:
            abort(404)

        if request.method == "POST":
            brand = (request.form.get("brand") or "").strip()
            model = (request.form.get("model") or "").strip()
            year = int(request.form.get("year") or 0)
            rate = float(request.form.get("rate") or 0)
            status = (request.form.get("status") or "").strip()

            cur.execute(
                "UPDATE cars SET brand = ?, model = ?, year = ?, rate = ?, status = ? WHERE id = ?",
                (brand, model, year, rate, status, car_id),
            )
            return redirect(url_for("cars"))

    return render_template("add_edit_car.html", car=car)


@app.route("/cars/delete/<int:car_id>", methods=["POST"])
def delete_car(car_id):
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    return redirect(url_for("cars"))

# -------------------- CUSTOMERS --------------------
@app.route("/customers")
def customers():
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()

    return render_template("customers.html", customers=customers)


@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():
    guard = require_login()
    if guard:
        return guard

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        phone = (request.form.get("phone") or "").strip()

        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone),
            )

        return redirect(url_for("customers"))

    return render_template("add_edit_customer.html", customer=None)


@app.route("/customers/edit/<int:customer_id>", methods=["GET", "POST"])
def edit_customer(customer_id):
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = cur.fetchone()

        if not customer:
            abort(404)

        if request.method == "POST":
            name = (request.form.get("name") or "").strip()
            email = (request.form.get("email") or "").strip()
            phone = (request.form.get("phone") or "").strip()

            cur.execute(
                "UPDATE customers SET name = ?, email = ?, phone = ? WHERE id = ?",
                (name, email, phone, customer_id),
            )

            return redirect(url_for("customers"))

    return render_template("add_edit_customer.html", customer=customer)


@app.route("/customers/delete/<int:customer_id>", methods=["POST"])
def delete_customer(customer_id):
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE id = ?", (customer_id,))

    return redirect(url_for("customers"))
# -------------------- RENTALS --------------------
@app.route("/rentals")
def rentals():
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT rentals.id, "
            "       cars.brand || ' ' || cars.model AS car, "
            "       customers.name AS customer, "
            "       rentals.start_date, "
            "       rentals.end_date, "
            "       rentals.total_cost, "
            "       rentals.status "
            "FROM rentals "
            "JOIN cars ON rentals.car_id = cars.id "
            "JOIN customers ON rentals.customer_id = customers.id"
        )
        rentals = cur.fetchall()

    return render_template("rentals.html", rentals=rentals)


@app.route("/rentals/add", methods=["GET", "POST"])
def add_rental():
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()

        # For the form dropdowns
        cur.execute("SELECT * FROM cars")
        cars = cur.fetchall()

        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()

        if request.method == "POST":
            car_id = int(request.form.get("car_id") or 0)
            customer_id = int(request.form.get("customer_id") or 0)
            start = (request.form.get("start_date") or "").strip()
            end = (request.form.get("end_date") or "").strip()
            cost = float(request.form.get("total_cost") or 0)
            status = (request.form.get("status") or "").strip()

            cur.execute(
                "INSERT INTO rentals (car_id, customer_id, start_date, end_date, total_cost, status) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (car_id, customer_id, start, end, cost, status),
            )

            return redirect(url_for("rentals"))

    return render_template("add_edit_rental.html", rental=None, cars=cars, customers=customers)

@app.route("/rentals/edit/<int:rental_id>", methods=["GET", "POST"])
def edit_rental(rental_id):
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()

        # 1) Get existing rental row
        cur.execute("SELECT * FROM rentals WHERE id = ?", (rental_id,))
        rental = cur.fetchone()
        if not rental:
            abort(404)

        # 2) Get cars and customers for dropdowns
        cur.execute("SELECT * FROM cars")
        cars = cur.fetchall()

        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()

        # 3) If form submitted, update rental
        if request.method == "POST":
            car_id = int(request.form.get("car_id") or 0)
            customer_id = int(request.form.get("customer_id") or 0)
            start = (request.form.get("start_date") or "").strip()
            end = (request.form.get("end_date") or "").strip()
            cost = float(request.form.get("total_cost") or 0)
            status = (request.form.get("status") or "").strip()

            cur.execute(
                "UPDATE rentals "
                "SET car_id = ?, customer_id = ?, start_date = ?, end_date = ?, total_cost = ?, status = ? "
                "WHERE id = ?",
                (car_id, customer_id, start, end, cost, status, rental_id),
            )

            return redirect(url_for("rentals"))

    # 4) Show the same form as add_rental, but filled with existing data
    return render_template(
        "add_edit_rental.html",
        rental=rental,
        cars=cars,
        customers=customers,
    )
@app.route("/rentals/delete/<int:rental_id>", methods=["POST"])
def delete_rental(rental_id):
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM rentals WHERE id = ?", (rental_id,))

    return redirect(url_for("rentals"))


# -------------------- PAYMENTS --------------------
@app.route("/payments")
def payments():
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM payments")
        payments = cur.fetchall()

    return render_template("payments.html", payments=payments)


@app.route("/payments/add", methods=["GET", "POST"])
def add_payment():
    guard = require_login()
    if guard:
        return guard

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM rentals")
        rentals = cur.fetchall()

        if request.method == "POST":
            rental_id = int(request.form.get("rental_id") or 0)
            amount = float(request.form.get("amount") or 0)
            date = (request.form.get("date") or "").strip()

            cur.execute(
                "INSERT INTO payments (rental_id, amount, date) VALUES (?, ?, ?)",
                (rental_id, amount, date),
            )

            return redirect(url_for("payments"))

    return render_template("add_payment.html", rentals=rentals)


# -------------------- RUN --------------------
if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        init_db()

    # Use FLASK_DEBUG=1 in development; don't enable debug in production
    debug = bool(int(os.environ.get("FLASK_DEBUG", "1")))
    app.run(debug=debug)
# CS665 Car Rental Project - Created by Rithika
