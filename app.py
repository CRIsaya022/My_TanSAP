from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to use SQLite database
db = SQL("sqlite:///app.db")


# Ensure content is up-to-date and not served from cache
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# handle the administrator side home page
@app.route("/")
@login_required
def indexadm():
    # extract the current user's name from the database (for display on the navigation bar)
    username_db = db.execute(
        "SELECT username FROM users WHERE id = ?", session["user_id"]
    )
    username = username_db[0]["username"]
    return render_template("indexadm.html", username=username)


# handle the student side home page
@app.route("/std")
@login_required
def indexstd():
    # extract the current user's name from the database (for display on the navigation bar)
    username_db = db.execute(
        "SELECT username FROM users WHERE id = ?", session["user_id"]
    )
    username = username_db[0]["username"]
    return render_template("indexstd.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user ID's
    session.clear()
    # User is submitting a form via POST
    if request.method == "POST":
        # Query database for the username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        role_db = db.execute(
            "SELECT role FROM users WHERE username = ?", request.form.get("username")
        )


        # Ensure username exists
        if len(rows) != 1:
            flash("Invalid username")
            return render_template("login.html")

        # Ensure the password is correct
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]
        role = role_db[0]["role"]
        if role == "admin":
            return redirect("/")
        else:
            return redirect("/std")

        # Redirect the user to the home page

    # User reached via GET/clicking the link/ via redirect
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # check if method is GET
    if request.method == "GET":
        return render_template("register.html")

    # Query the database for the username
    rows = db.execute(
        "SELECT * FROM users WHERE username = ?", request.form.get("username")
    )

    # Check if the username exists
    if len(rows) >= 1:
        flash("Username already taken")
        return render_template("register.html")

    # Ensure confirmation password = original password
    if request.form.get("password") != request.form.get("confirmPassword"):
        flash("Passwords do not match")
        return render_template("register.html")

    # Insert the new user into the database and log users in automatically
    new_user_id = db.execute(
        "INSERT INTO users (username, hash, role) VALUES (:username, :hash, :role)",
        username=request.form.get("username"),
        hash=generate_password_hash(request.form.get("password")),
        role=request.form.get("role"),
    )
    session["user_id"] = new_user_id
    # redirect users to their respective homepage
    role = request.form.get("role")
    if role == "admin":
        return redirect("/")
    else:
        return redirect("/std")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user ID's
    session.clear()

    # Redirect the user to the login page
    return redirect("/login")


@app.route("/upload_essay", methods=["GET", "POST"])
def upload_essay():
    # upload essay review request from the form to the database
    if request.method == "POST":
        new_essay = db.execute(
            "INSERT INTO ESSAYS (student_name, essay_link, comments) VALUES (:student_name, :essay_link, :comments)",
            student_name=request.form.get("student_name"),
            essay_link=request.form.get("essay_link"),
            comments=request.form.get("comments"),
        )
        flash("Essay review request uploaded")
        return render_template("upload_essay.html")
    else:
        return render_template("upload_essay.html")


@app.route("/view_essays")
def view_essays():
    # extract essay review requests data from the database
    essay_data = db.execute("SELECT * FROM ESSAYS")
    # pass essay review request data to the display page
    return render_template("view_essays.html", essay_data=essay_data)


@app.route("/upload_week", methods=["GET", "POST"])
def upload_week():
    # upload weekly plan from the form to the database
    if request.method == "POST":
        new_week = db.execute(
            "INSERT INTO WEEK (monday, tuesday, wednesday, thursday, friday) VALUES (:monday, :tuesday, :wednesday, :thursday, :friday)",
            monday=request.form.get("monday"),
            tuesday=request.form.get("tuesday"),
            wednesday=request.form.get("wednesday"),
            thursday=request.form.get("thursday"),
            friday=request.form.get("friday"),
        )
        flash("Weekly Plan Uploaded")
        return render_template("upload_week.html")
    else:
        return render_template("upload_week.html")


@app.route("/view_week")
def view_week():
    # extract weekly schedule data from the database
    week_data = db.execute("SELECT * FROM WEEK")
    # pass weekly schedule data to the display page
    return render_template("week.html", week_data=week_data)


@app.route("/scores")
def scores():
    return render_template("scores.html")


@app.route("/upload_SAT", methods=["POST"])
def upload_SAT():
    # upload student SAT scores from the form to the database
    new_SATscore = db.execute(
        "INSERT INTO SAT (Student_name, Score, Date, Comments) VALUES (:Student_name, :Score, :Date, :Comments)",
        Student_name=request.form.get("satStudentName"),
        Score=request.form.get("satScore"),
        Date=request.form.get("satTestDate"),
        Comments=request.form.get("satComments"),
    )
    flash("SAT Score Uploaded")
    return render_template("scores.html")


@app.route("/upload_toefl", methods=["POST"])
def upload_toefl():
    # upload student TOEFL scores from the form to the database
    new_toeflscore = db.execute(
        "INSERT INTO TOEFL (Student_name, Score, Date, Comments) VALUES (:Student_name, :Score, :Date, :Comments)",
        Student_name=request.form.get("toeflStudentName"),
        Score=request.form.get("toeflScore"),
        Date=request.form.get("toeflTestDate"),
        Comments=request.form.get("toeflComments"),
    )
    flash("TOEFL Score Uploaded")
    return render_template("scores.html")


@app.route("/upload_announcement", methods=["GET", "POST"])
def upload_announcement():
    # upload announcements from the form to the database
    if request.method == "POST":
        new_announcement = db.execute(
            "INSERT INTO ANNOUNCEMENTS (title, message, date) VALUES (:title, :message, :date)",
            title=request.form.get("title"),
            message=request.form.get("message"),
            date=request.form.get("date"),
        )
        flash("Announcement Uploaded")
        return render_template("announcements.html")
    else:
        return render_template("announcements.html")


@app.route("/view_announcement")
def view_announcement():
    # extract annoucement data from the database
    announcement_data = db.execute("SELECT * FROM ANNOUNCEMENTS")
    # pass the announcement data to the display page
    return render_template(
        "view_announcement.html", announcement_data=announcement_data
    )


@app.route("/viewscores")
def viewscores():
    # get the username of the user in session/logged in
    user_name = session["user_name"]
    # extract user's test score data from the database
    sat_data = db.execute("SELECT * FROM SAT WHERE Student_name = ?", user_name)
    toefl_data = db.execute("SELECT * FROM TOEFL WHERE Student_name = ?", user_name)
    # pass the test score data to the page for display
    return render_template("viewscores.html", sat_data=sat_data, toefl_data=toefl_data)


if __name__ == "__main__":
    app.run(debug=True)
