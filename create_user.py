from flask_bcrypt import Bcrypt
import mysql.connector

bcrypt = Bcrypt()

# Ζητάμε από τον χρήστη στοιχεία
username = input("Username: ")
password = input("Password: ")

# Δημιουργούμε hash για τον κωδικό
password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# Σύνδεση με τη βάση
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Panagiotis@97",
    database="genebank"
)
cursor = conn.cursor()
cursor.execute("INSERT INTO Users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
conn.commit()
conn.close()

print(f"User {username} created successfully!")
