import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session , url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import ResourceClosedError

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
############################################################################################
@app.route('/')
def index():
    return redirect(url_for('login'))
############################################################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["user_type"] = rows[0]["user_type"]

        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html")
############################################################################################
@app.route('/dashboard')
def dashboard():

    if 'user_id' in session:
        user_type = db.execute(
        "SELECT user_type FROM users WHERE id = :user_id", user_id=session["user_id"]
        )[0]["user_type"]

        return render_template(f'{user_type}.html')
    return redirect(url_for('login'))
############################################################################################
@app.route("/stud_form", methods=["GET", "POST"])
@login_required
def stud_form():
    if request.method == "POST":
        sf_name = request.form.get("sf_name")
        sf_stream = request.form.get("sf_stream")
        sf_SCGPA = request.form.get("sf_SCGPA")
        sf_linkedin = request.form.get("sf_linkedin")

        if not sf_name or not sf_stream or not sf_SCGPA:
            return apology("Must provide Student Name / Stream / SCGPA")

        db.execute(
            "INSERT INTO applicant_table (user_id, stud_name, stud_sub, s_SCGPA, linkedin_link) VALUES (:user_id, :sf_name, :sf_stream, :sf_SCGPA, :sf_linkedin)",
            user_id=session["user_id"],
            sf_name=sf_name,
            sf_stream=sf_stream,
            sf_SCGPA=sf_SCGPA,
            sf_linkedin=sf_linkedin,
        )

        flash(f"Student {sf_name} data has successfully added to Applicant list")
        return redirect("/dashboard")

    else:
        return render_template("stud_form.html")
############################################################################################
@app.route("/stud_choose", methods=["GET", "POST"])
@login_required
def stud_choose():
    if request.method == "POST":
        sc_comp_choose = request.form.get("sc_comp_choose")

        if not sc_comp_choose :
            return apology("Please choose a company")

        db.execute(
            "INSERT INTO hire_request_table (user_id, company_name) VALUES (:user_id, :sc_comp_choose)",
            user_id=session["user_id"],
            sc_comp_choose = sc_comp_choose,
        )

        db.execute("DROP TABLE IF EXISTS applicant_company_request")

        try:
            db.execute("CREATE TABLE applicant_company_request AS SELECT a.applicant_id, a.stud_name, a.stud_sub, a.s_SCGPA, a.linkedin_link, h.company_name FROM applicant_table AS a INNER JOIN hire_request_table AS h ON a.user_id = h.user_id")
        except ResourceClosedError:
            pass  # Do nothing, since there are no rows to fetch

        rows= db.execute(
            "SELECT * FROM applicant_table WHERE user_id=:user_id", user_id=session["user_id"] )
        student_name = rows[0]["stud_name"]

        flash(f"Student {student_name} has successfully Choose a Company, & now, added to hire_request_table")
        return redirect("/dashboard")

    else:
        return render_template("stud_choose.html")
############################################################################################
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Both Password is not same", 400)

        elif not request.form.get("user_type"):
            return apology("Error with user type", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 0:
            return apology("Username already exists", 400)

        db.execute(
            "INSERT INTO users (username, hash, user_type) VALUES( ?, ?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
            request.form.get("user_type"),
        )

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["user_type"] = rows[0]["user_type"]

        return redirect(url_for('dashboard'))
    else:
        return render_template("register.html")
########################################################################################
@app.route('/stud_all')
@login_required
def stud_all():
    """ Show Company participating in On-campus recruitment """
    applicant_company_request = db.execute(
        "SELECT * FROM applicant_company_request ORDER BY applicant_id DESC",
    )
    return render_template("stud_all.html", applicant_company_request = applicant_company_request)
############################################################################################
@app.route('/stud_comp_list')
@login_required
def stud_comp_list():
    """ Show Company participating in On-campus recruitment """
    company_table = db.execute("SELECT * FROM company_table ORDER BY user_id DESC",)
    print(company_table)
    return render_template("stud_comp_list.html", company_table = company_table)
############################################################################################
@app.route('/comp_list')
@login_required
def comp_list():
    """ Show Company participating in On-campus recruitment """
    company_table = db.execute("SELECT * FROM company_table ORDER BY user_id DESC",)
    print(company_table)
    return render_template("comp_list.html", company_table = company_table)
############################################################################################
@app.route("/comp_form", methods=["GET", "POST"])
@login_required
def comp_form():
    if request.method == "POST":
        c_name = request.form.get("c_name")
        c_loc = request.form.get("c_loc")
        c_min_SCGPA = request.form.get("c_min_SCGPA")
        c_min_Sal = request.form.get("c_min_Sal")
        c_max_Sal = request.form.get("c_max_Sal")
        vacancies = request.form.get("vacancies")

        if not c_name or not c_loc or not c_min_SCGPA:
            return apology("Must provide Company Name / location / min SCGPA requirement")

        db.execute(
            "INSERT INTO company_table (user_id, c_name, c_loc, c_min_SCGPA, c_min_Sal, c_max_Sal, vacancies) VALUES (:user_id, :c_name, :c_loc, :c_min_SCGPA, :c_min_Sal, :c_max_Sal, :vacancies)",
            user_id=session["user_id"],
            c_name=c_name,
            c_loc=c_loc,
            c_min_SCGPA=c_min_SCGPA,
            c_min_Sal=c_min_Sal,
            c_max_Sal=c_max_Sal,
            vacancies=vacancies,
        )

        flash(f"Company {c_name} data has successfully added to Company list")
        return redirect("/dashboard")
    else:
        return render_template("comp_form.html")
##################################################################################################
@app.route('/Companies')
@login_required
def Companies():
    """ Show Company participating in On-campus recruitment """
    company_table = db.execute(
        "SELECT * FROM company_table ORDER BY user_id DESC",
        #"SELECT * FROM company_table ORDER BY id DESC",
    )
    return render_template("Companies.html", company_table=company_table)
##################################################################################################
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect(url_for('login'))

###################################################################################################
# To run this code you need to install :-

# 1) Install flask         ->  pip install Flask
# 2) Install cs50          ->  pip install cs50
# 3) Install Flask-Session ->  pip install Flask-Session

# And after all this just run,
#         flask run
