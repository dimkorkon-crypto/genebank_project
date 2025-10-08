from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_bcrypt import Bcrypt
from functools import wraps
import os 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")  
bcrypt = Bcrypt(app)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        charset='utf8mb4'
    )


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Πρέπει να συνδεθείτε πρώτα.", "auth")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------
# Routes
# -------------------------

@app.route('/')
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username=%s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash("Λάθος όνομα χρήστη ή κωδικός.", "auth")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Αποσυνδεθήκατε.", "auth")
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = (request.form.get("query") or "").strip()
        if not query:
            return render_template("search.html", error="Παρακαλώ εισάγετε είδος φυτού.")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                sm.sample_id,
                sp.name AS species_name,
                sp.common_name,
                sm.accession_code,
                sm.collection_date,
                sm.origin
            FROM Samples sm
            JOIN Species sp ON sm.species_id = sp.species_id
            WHERE sp.name LIKE %s
              OR sp.common_name LIKE %s
              OR sm.accession_code LIKE %s
              OR sm.origin LIKE %s
            ORDER BY sm.collection_date DESC
            LIMIT 500
        """
        qparam = f"%{query}%"
        cursor.execute(sql, (qparam, qparam, qparam, qparam))
        results = cursor.fetchall()
        conn.close()

        return render_template("results.html", results=results, query=query)

    return render_template("search.html")

@app.route('/add-sample', methods=['GET', 'POST'])
@login_required
def add_sample():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT species_id, name FROM Species ORDER BY name ASC")
    species_list = cursor.fetchall()

    if request.method == 'POST':
        species_id = request.form.get('species_id')
        accession_code = request.form.get('accession_code', '').strip()
        collection_date = request.form.get('collection_date')
        origin = request.form.get('origin', '').strip()
        storage_location = request.form.get('storage_location', '').strip()
        notes = request.form.get('notes', '').strip()

        if not species_id or not accession_code:
            flash("Το είδος και ο accession code είναι υποχρεωτικά.", "danger")
            return render_template('add_sample.html', species_list=species_list)

        try:
            cursor.execute("""
                INSERT INTO Samples (species_id, accession_code, collection_date, origin, storage_location, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (species_id, accession_code, collection_date, origin, storage_location, notes))
            conn.commit()
            flash("Το δείγμα καταχωρήθηκε επιτυχώς!", "success")
            return redirect(url_for('search'))
        except mysql.connector.Error as e:
            flash(f"Σφάλμα: {e}", "danger")
            conn.rollback()
        finally:
            conn.close()

    return render_template('add_sample.html', species_list=species_list)

@app.route('/sample/<int:sample_id>')
@login_required
def sample_details(sample_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            sm.sample_id,
            sp.name AS species_name,
            sp.common_name,
            sp.family,
            sm.accession_code,
            sm.collection_date,
            sm.origin,
            sm.storage_location,
            sm.notes
        FROM Samples sm
        JOIN Species sp ON sm.species_id = sp.species_id
        WHERE sm.sample_id = %s
    """, (sample_id,))
    sample = cursor.fetchone()

    cursor.execute("SELECT trait_name, description FROM Genetic_Traits WHERE sample_id=%s", (sample_id,))
    traits = cursor.fetchall()

    cursor.execute("SELECT temperature, humidity, duration_years, notes FROM Storage_Conditions WHERE sample_id=%s", (sample_id,))
    storage = cursor.fetchall()

    conn.close()

    return render_template("details.html", sample=sample, traits=traits, storage=storage)

if __name__ == "__main__":
    app.run(debug=True)

