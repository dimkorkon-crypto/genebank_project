# Genetic Material Bank

This project is a **web application** for managing a **Genetic Material Bank**.  
It is built with **Flask (Python)** and **MySQL** and provides functionality for storing, searching, and managing genetic material samples.

---

## 🚀 Features
- User authentication (login/logout)  
- Search samples by species, accession code, etc.  
- Add new samples with details (origin, storage, notes)  
- View sample details, traits, and storage conditions  
- Relational database schema with multiple related tables  

---

## 🗄️ Database Schema
The system uses a **MySQL relational database** with the following tables:
- `Species`
- `Samples`
- `Genetic_Traits`
- `Improvement_Goals`
- `Storage_Conditions`
- `Users`

📌 See `schema.sql` for full table definitions.

---

## 📂 Project Structure
genebank_project/
│
├── app.py # Flask application
├── create_user.py # Utility script for creating new users
├── requirements.txt # Python dependencies
├── schema.sql # Database schema
├── README.md # Project documentation
├── .gitignore # Git ignore rules
│
├── templates/ # HTML templates (Flask Jinja2)
│ 	├── base.html
│ 	├── index.html
│	├── login.html
│ 	├── search.html
│ 	├── details.html
│ 	└── add_sample.html
│
└── static/
	├── css/style.css
	└── images/
	├── banner.png
	├── logo.png
	└── genetic_bank.png


---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/genebank_project.git
cd genebank_project

2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root:
DB_HOST=localhost
DB_USER=root
DB_PASS=yourpassword
DB_NAME=genebank
SECRET_KEY=YourSecretKey

5. Set up the database

Run the SQL schema:
mysql -u root -p < schema.sql

6. Run the application
python app.py
Then open http://localhost:5000 in your browser.

👥 Contributors
[Korkontzilas Dimitrios] – Developer

📜 License
This project is for academic and research purposes. All rights reserved.