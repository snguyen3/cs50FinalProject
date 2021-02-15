import os
from datetime import datetime, date, timedelta
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
# base design and code taken from CS50 Finance

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///goals.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show mainpage"""
    if request.method == "GET":
        goals = db.execute("SELECT * FROM maingoals WHERE user_id = ? AND completed = ?", session["user_id"], "FALSE")
        goal_number = len(goals)
        subgoals = db.execute("SELECT * FROM subgoals WHERE user_id = ? AND completed = ?", session["user_id"], "FALSE")
        return render_template("index.html", goals=goals, subgoals=subgoals, goal_number=goal_number)

    # Differentiate between multiple post requests
    # Src: https://www.codegrepper.com/code-examples/python/multiple+flask+forms+in+one+page
    if request.method == "POST":
        form_name = request.form["choose"]
        if "Start Timer" in form_name:

            # get subgoal that user chooses
            subgoal_id = request.form.get("subgoal_id")

            # Returns error when there are no subgoals under the maingoal
            if not subgoal_id:
                flash('No subgoals have been added!', "warning")
                return redirect("/")
            subgoal = db.execute("SELECT subgoal, time_planned, maingoal_id FROM subgoals WHERE id = ?", subgoal_id)
            maingoal = db.execute("SELECT maingoal FROM maingoals WHERE id = ?", subgoal[0]["maingoal_id"])
            return render_template("timer.html", subgoal=subgoal, maingoal=maingoal, subgoal_id=subgoal_id)

        # Deletes subgoal
        elif "Delete Subgoal" in form_name:
            subgoal_id = request.form.get("list_subgoals")
            db.execute("DELETE FROM subgoals WHERE id = ?", subgoal_id)
            flash("Subgoal deleted", "success")
            return redirect("/")

        elif "Delete Maingoal" in form_name:
            maingoal_id = request.form.get("maingoal_selected")
            # Delete subgoals under the main goal
            db.execute("DELETE FROM subgoals WHERE maingoal_id = ? AND user_id = ?", maingoal_id, session["user_id"])
            # Delete maingoal

            db.execute("DELETE FROM maingoals WHERE id = ?", maingoal_id)
            flash("Main goal deleted", "success")
            return redirect("/")

        # Sets main goal finished to true and deletes subgoals that were remaining under it
        elif "Finished" in form_name:
            maingoal_id = request.form.get("maingoal_id")
            time = datetime.now()
            today = date.today()
            # Set the time_planned of the maingoal to be 1 (arbitrary value)
            db.execute("UPDATE maingoals SET completed = ?, datetime = ?, date = ? WHERE id = ?", "TRUE", time, today, maingoal_id)
            db.execute("DELETE FROM subgoals WHERE maingoal_id = ? AND completed = ?", maingoal_id, "FALSE")
            return redirect("/")


@app.route("/timer", methods=["POST"])
@login_required
def timer():

    # POST method: when the "Finish Task" button is pressed
    if request.method == "POST":
        time_spent = int(request.form.get("total_time"))
        subgoal_id = request.form.get("subgoal_id")
        subgoal_time_planned = db.execute("SELECT time_planned FROM subgoals WHERE id = ?", subgoal_id)[0]["time_planned"]

        # When users finish a subgoal, update the maingoals table
        main_id = db.execute("SELECT maingoal_id FROM subgoals WHERE id = ?", subgoal_id)[0]["maingoal_id"]
        main_time_spent = db.execute("SELECT time_spent FROM maingoals WHERE id = ?", main_id)[0]["time_spent"]
        main_time_planned = db.execute("SELECT time_planned FROM maingoals WHERE id = ?", main_id)[0]["time_planned"]

        main_time_spent += time_spent
        main_time_planned += subgoal_time_planned

        # Update the subgoal table and the maingoal table
        db.execute("UPDATE subgoals SET time_spent = ?, completed = ?, datetime = ?, date = ? WHERE id = ?",
                   time_spent, "TRUE", datetime.now(), date.today(), subgoal_id)
        db.execute("UPDATE maingoals SET time_spent = ?, time_planned = ? WHERE id = ?",
                   main_time_spent, main_time_planned, main_id)
        return redirect("/")


@app.route("/addgoal", methods=["GET", "POST"])
@login_required
def addgoal():
    """Add A Goal"""
    if request.method == "POST":

        # Store information
        maingoal = request.form.get("maingoal")
        subgoal = request.form.get("subgoal")
        subgoal_time = request.form.get("subgoal_time")
        maingoal_time = request.form.get("maingoal_time")

        # If users add a new maingoal
        if maingoal:
            db.execute("INSERT INTO maingoals (user_id, maingoal) VALUES (?, ?)", session["user_id"], maingoal)
            # Confirmation Alert
            flash("Success! Added \"%s\" into your goal list!" % maingoal, "success")

        # If users add a new subgoal
        elif subgoal and subgoal_time:
            # Get maingoal from the drop down list
            maingoal_selected = request.form.get("maingoals_selected")

            if maingoal_selected:
                # Get the name for the flash confirmation
                maingoal_name = db.execute("SELECT maingoal FROM maingoals WHERE id = ?", maingoal_selected)[0]["maingoal"]

            # Error condition
            else:
                flash("Select a maingoal", "warning")
                return redirect("/addgoal")

            # Insert subgoal into db if true
            db.execute("INSERT INTO subgoals (user_id, maingoal_id, subgoal, time_planned) VALUES (?, ?, ?, ?)",
                       session["user_id"], maingoal_selected, subgoal, subgoal_time)

            # Confirmation Alert
            flash("Success! Added \"%s\" under your maingoal: \"%s\"!" % (subgoal, maingoal_name), "success")
        # Error condition
        else:
            flash("Enter a maingoal/subgoal", "warning")
            return redirect("/addgoal")

        return redirect("/addgoal")

    if request.method == "GET":
        return render_template("addgoal.html", goals=db.execute("SELECT * FROM maingoals WHERE user_id = ? AND completed = ?", session["user_id"], "FALSE"))


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """ Editing Goals """
    if request.method == "POST":
        maingoal_id = request.form.get("maingoal")
        subgoal_id = request.form.get("subgoal")

        # If maingoal is being edited
        if maingoal_id:

            # Get both values for flash
            old_maingoal_name = db.execute("SELECT maingoal from maingoals WHERE id = ?", maingoal_id)[0]["maingoal"]
            new_maingoal_name = request.form.get("new_maingoal_name")

            # Error Condition
            if new_maingoal_name == "":
                flash("Cannot change maingoal name to a blank one", "warning")
                return redirect("/edit")

            # Update value and send confirmation
            else:
                db.execute("UPDATE maingoals SET maingoal = ? WHERE id = ?", new_maingoal_name, maingoal_id)
                flash("Success! Changed \"%s\" into: \"%s\"!" % (old_maingoal_name, new_maingoal_name), "success")
                return redirect("/")

        # If subgoal is being edited
        if subgoal_id:

            # Get both name and time planned for confirmation and errors
            old_subgoal_name = db.execute("SELECT subgoal from subgoals WHERE id = ?", subgoal_id)[0]["subgoal"]
            new_subgoal_name = request.form.get("new_subgoal_name")
            old_subgoal_time = db.execute("SELECT time_planned from subgoals WHERE id = ?", subgoal_id)[0]["time_planned"]
            new_subgoal_time = request.form.get("new_subgoal_time")

            # Time error condition
            if new_subgoal_time != "" and int(new_subgoal_time) < 1:
                flash("Cannot change time to values under 1", "warning")
                return redirect("/edit")

            # Actual updates
            if new_subgoal_name != "" and not new_subgoal_time:
                db.execute("UPDATE subgoals SET subgoal = ? WHERE id = ?", new_subgoal_name, subgoal_id)
                flash("Success! Changed \"%s\" into: \"%s\"!" % (old_subgoal_name, new_subgoal_name), "success")
                return redirect("/")

            # If only new_subgoal time is updated
            elif not new_subgoal_name and new_subgoal_time:
                db.execute("UPDATE subgoals SET time_planned = ? WHERE id = ?", new_subgoal_time, subgoal_id)
                flash("Success! Changed \"%s\" time from %s minutes to %s minutes!" %
                      (old_subgoal_name, old_subgoal_time, new_subgoal_time), "success")
                return redirect("/")

            # If both are updated
            elif new_subgoal_name != "" and new_subgoal_time:
                db.execute("UPDATE subgoals SET subgoal = ? WHERE id = ?", new_subgoal_name, subgoal_id)
                db.execute("UPDATE subgoals SET time_planned = ? WHERE id = ?", new_subgoal_time, subgoal_id)
                flash("Success! Changed \"%s\" into: \"%s\" and time from %s minutes to %s minutes!" %
                      (old_subgoal_name, new_subgoal_name, old_subgoal_time, new_subgoal_time), "success")
                return redirect("/")

            # Further Error Conditions
            elif new_subgoal_name == "":
                flash("Cannot leave the new name blank", "warning")
                return redirect("/edit")

            else:
                flash("Cannot leave both fields blank", "warning")
                return redirect("/edit")
        else:
            flash("Enter a maingoal/subgoal", "warning")
            return redirect("/edit")

    # Accessed via navbar
    if request.method == "GET":
        maingoals = db.execute("SELECT * from maingoals WHERE user_id = ? and completed = ?", session["user_id"], "FALSE")
        subgoals = db.execute("SELECT * from subgoals WHERE user_id = ? and completed = ?", session["user_id"], "FALSE")
        return render_template("edit.html", maingoals=maingoals, subgoals=subgoals)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of goals"""

    if request.method == "GET":
        # Pass an abitrary un-used time_range to the history page
        time_range = 0
        return render_template("history.html", time_range=time_range)

    if request.method == "POST":
        today = date.today()
        time_range = request.form.get("time_range")
        # Null condition
        if time_range == None:
            return redirect("/history")
        else:
            time_range = int(time_range)

            # Generate a range of dates: https://stackoverflow.com/questions/5868130/generating-all-dates-within-a-given-range-in-python/26583750
            date_list = []
            time_step = timedelta(1)
            from_date = today - timedelta(time_range)
            loop_date = from_date

            # Create a list of dates
            while loop_date <= today:
                date_list.append(loop_date)
                loop_date += time_step

            # Select all goals between time range; calculate the number of goals completed
            goal_num = len(db.execute("SELECT * FROM maingoals WHERE (date >= ? AND date <= ?) AND completed = ? AND user_id = ?",
                                      from_date, today, "TRUE", session["user_id"]))
            # No goals to show
            if goal_num == 0:
                return render_template("history.html", time_range=time_range)
            else:
                # Number of work days (days on which the user completed tasks)
                day_num = len(db.execute("SELECT * FROM maingoals WHERE (date >= ? AND date <= ?) AND completed = ? AND user_id = ? GROUP BY date",
                                         from_date, today, "TRUE", session["user_id"]))

                # Total time spent and total time planned
                total_tp = db.execute("SELECT SUM(time_planned) FROM maingoals WHERE (date >= ? AND date <= ?) AND completed = ? AND user_id = ?",
                                      from_date, today, "TRUE", session["user_id"])[0]["SUM(time_planned)"]
                total_ts = db.execute("SELECT SUM(time_spent) FROM maingoals WHERE (date >= ? AND date <= ?) AND completed = ? AND user_id = ?",
                                      from_date, today, "TRUE", session["user_id"])[0]["SUM(time_spent)"]

                # Min difference, difference in percent, average time difference, and average percent per work day
                time_diff = abs(total_tp - total_ts)
                percent_diff = round(time_diff * 100 / total_tp)
                avg_time_diff = round(time_diff / day_num)
                avg_percent = round(time_diff * 100 / (total_tp * day_num))

                # Summary dict
                summary = {}
                summary["day_num"] = day_num
                summary["total_tp"] = total_tp
                summary["total_ts"] = total_ts
                summary["time_diff"] = time_diff
                summary["percent_diff"] = percent_diff
                summary["avg_time_diff"] = avg_time_diff
                summary["avg_percent"] = avg_percent
                summary["goal_num"] = goal_num

                # Initiate datasets for graphing
                tp_list = []
                ts_list = []

                # Loop through
                for one_date in date_list:
                    # Fill time_spent dataset
                    sum_ts = db.execute("SELECT SUM(time_spent) FROM maingoals WHERE date = ? AND completed = ? AND user_id = ?",
                                        one_date, "TRUE", session["user_id"])[0]["SUM(time_spent)"]
                    if sum_ts is None:
                        ts_list.append(0)
                    else:
                        ts_list.append(sum_ts)
                    # Fill time_planned dataset
                    sum_tp = db.execute("SELECT SUM(time_planned) FROM maingoals WHERE date = ? AND completed = ? AND user_id = ?",
                                        one_date, "TRUE", session["user_id"])[0]["SUM(time_planned)"]
                    if sum_tp is None:
                        tp_list.append(0)
                    else:
                        tp_list.append(sum_tp)

                # Convert all dates in date_list to presentable strings
                for i in range(len(date_list)):
                    formatted_date = date_list[i].isoformat()
                    date_list[i] = formatted_date

                return render_template("week_month.html", summary=summary, time_range=time_range, date_list=date_list, tp_list=tp_list, ts_list=ts_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Invalid username and/or password", "warning")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Add time user logged into into table
        db.execute("INSERT into loginlogs (user_id, datetime) VALUES (?, ?)", session["user_id"], datetime.now())
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Gets values from forms
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Checks if username is unique
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Checks if all fields were filled out and correctly
        if not username:
            flash("Must enter username", "warning")
            return redirect("/register")
        elif len(rows) != 0:
            flash("Username has already been taken", "warning")
            return render_template("register.html")
        elif not password or not confirmation:
            flash("Must enter and/or confirm password", "warning")
            return redirect("/register")
        # Checks if password matches confirmed password
        if password != confirmation:
            flash("Passwords do not match", "warning")
            return redirect("/register")
        # Inputs the user info into the database
        else:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, generate_password_hash(password))
            flash("Account successfully created!", "success")
            return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def change_pw():
    # Change user's password
    if request.method == "POST":
        old_pw = request.form.get("old_password")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure password was submitted
        if not old_pw or not password or not confirmation:
            flash("must fill in all fields", "warning")
            return redirect("/changepw")

        # Checks if old password is correct
        check = db.execute("SELECT * FROM users WHERE user_id=?", session["user_id"])
        if not check_password_hash(check[0]["password"], old_pw):
            flash("incorrect old password", "warning")
            return redirect("/changepw")
        elif password != confirmation:
            flash("new password does not match confirmation", "warning")
            return redirect("/changepw")
        # Changes user's password
        else:
            db.execute("UPDATE users SET password=? WHERE user_id=?", generate_password_hash(
                password), session["user_id"])
            flash("Password successfully changed!", "success")
            return redirect("/")
    else:
        return render_template("changepw.html")


@app.route("/clockout", methods=["GET", "POST"])
@login_required
def clockout():
    """End scene of website"""
    # End result = https://i.imgur.com/8uHLsst.png
    if request.method == "GET":
        # Current time - type datetime
        curr_time = datetime.now()
        # Convert curr_time into a str to compare with sql
        curr_time = datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
        # Find the current session and time that user logged in - type str
        raw_time_logged_in = db.execute(
            "SELECT datetime FROM loginlogs WHERE user_id = ? ORDER BY datetime DESC LIMIT 1", session["user_id"])[0]["datetime"]

        # Get maingoals and subgoals completed
        maingoals = db.execute("SELECT * FROM maingoals WHERE user_id = ?", session["user_id"])
        subgoals = db.execute("SELECT * FROM subgoals WHERE user_id = ? AND completed = ? AND datetime <= ? AND datetime >= ?",
                              session["user_id"], "TRUE", curr_time, raw_time_logged_in)

        # Initialize number of goals completed and time spent
        time_spent = 0
        num_of_goals = 0
        total_tp = 0

        # Get subgoal statistics
        for subgoal in subgoals:
            subgoal_tp = subgoal["time_planned"]
            subgoal_ts = subgoal["time_spent"]
            # Update total vals
            total_tp += subgoal_tp
            time_spent += subgoal_ts
            num_of_goals = num_of_goals + 1

        return render_template("clockout.html", total_tp=total_tp,  time_spent=time_spent, num_of_goals=num_of_goals, maingoals=maingoals, subgoals=subgoals)
        
    # If button is pressed, log them out.
    if request.method == "POST":
        return redirect("/logout")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
