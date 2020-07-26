from flask import Flask, render_template, url_for, redirect, request, session, g

import sqlite3

app = Flask(__name__)
app.secret_key = "stay secret to keep my todo items safe"


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

    g.db = sqlite3.connect("assignments_tracker.db")


@app.route("/", methods=["GET", "POST"])
def tasks():
    if g.user is None:
        return redirect(url_for("login"))
    cursor = g.db.cursor()
    if request.method == "POST":
        if request.form["submit_button"] == "Add Task":
            cursor.execute("INSERT INTO tasks VALUES(NULL, '{}', '{}' )".format(g.user, request.form["new_task"]))
            g.db.commit()
            cursor.close()
            return redirect(url_for("tasks"))
        elif request.form["submit_button"] == "Delete":
            cursor.execute("DELETE FROM tasks WHERE id={}".format(request.form["task_id"]))
            g.db.commit()
            cursor.close()
            return redirect(url_for("tasks"))
    cursor.execute("SELECT * FROM tasks WHERE task_user = '{}'".format(g.user))
    task_data = cursor.fetchall()
    cursor.close()
    return render_template("tasks.html", username=g.user, tasks=reversed(task_data))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session.pop("user", None)
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        cursor = g.db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '{}'".format(attempted_username))
        if cursor.fetchone() is not None:
            return render_template("register.html", error="Error: Username Taken")
        else:
            cursor.execute("INSERT INTO users VALUES(NULL, '{}', '{}')".format(attempted_username, attempted_password))
            g.db.commit()
            cursor.close()
            return redirect(url_for("login"))
    return render_template("register.html", error="")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("user", None)
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        cursor = g.db.cursor()
        cursor.execute("SELECT password FROM users WHERE username = '{}'".format(attempted_username))
        password = cursor.fetchone()
        cursor.close()
        if password is None:
            return render_template("login.html", error="Error: User does not exist")
        elif password[0] != attempted_password:
            return render_template("login.html", error="Error: Invalid Password")
        elif password[0] == attempted_password:
            session['user'] = attempted_username
            return redirect(url_for("tasks"))
        else:
            return render_template("login.html", error="Unknown Error")
    return render_template("login.html", error="")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        session.pop("user", None)
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        cursor = g.db.cursor()
        cursor.execute("SELECT password FROM users WHERE username = '{}'".format(attempted_username))
        password = cursor.fetchone()
        if password is None:
            return render_template("delete_account.html", error="Error: User does not exist")
        elif password[0] != attempted_password:
            return render_template("delete_account.html", error="Error: Invalid Password")
        elif password[0] == attempted_password:
            cursor.execute("DELETE FROM tasks WHERE task_user='{}'".format(request.form['username']))
            cursor.execute("DELETE FROM users WHERE username='{}'".format(request.form['username']))
            g.db.commit()
            cursor.close()
            return redirect(url_for("register"))
        else:
            return render_template("delete_account.html", error="Unknown Error")
    return render_template("delete_account.html", error="")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")