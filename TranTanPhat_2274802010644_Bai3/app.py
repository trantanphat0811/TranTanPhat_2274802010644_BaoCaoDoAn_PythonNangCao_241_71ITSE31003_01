from flask import Flask, redirect, url_for, render_template, session, request, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
app.config["SECRET_KEY"] = "phattan112"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=2)

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(250))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/home")
@app.route("/")
def home():
    
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    
    if "user" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("home"))
    
    users = User.query.all()
    return render_template("dashboard.html", users=users)

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if "user" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if name and email:
            try:
                new_user = User(name=name, email=email)
                db.session.add(new_user)
                db.session.commit()
                flash("User added successfully!", "info")
                return redirect(url_for("dashboard"))
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding user: {e}", "danger")
    return render_template("add_user.html")

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if "user" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("home"))

    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.name = request.form.get("name")
        user.email = request.form.get("email")
        try:
            db.session.commit()
            flash("User details updated successfully!", "info")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating user: {e}", "danger")
    return render_template("edit_user.html", user=user)

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    if "user" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("home"))

    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting user: {e}", "danger")
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form.get("name")
        user_email = request.form.get("email")
        session.permanent = True

        if user_name and user_email:
            session["user"] = user_name
            session["email"] = user_email
            found_user = User.query.filter_by(name=user_name).first()
            
            if found_user:
                found_user.email = user_email  
                flash("User already exists, email updated.", "info")
            else:
                try:
                    user = User(name=user_name, email=user_email)
                    db.session.add(user)
                    db.session.commit()
                    flash("New user added successfully.", "info")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error logging in or creating user: {e}", "danger")
            return redirect(url_for("dashboard"))
    return render_template("home.html")

@app.route("/user")
def user():
    if "user" in session:
        name = session["user"]
        email = session.get("email", "No email entered")
        return render_template("user.html", user=name, email=email)
    else:
        flash("Please log in first.", "info")
        return redirect(url_for("login"))

@app.route("/logout")
def log_out():
    session.pop("user", None)
    session.pop("email", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))

@app.route("/delete_current_user")
def delete_current_user():
    if "user" in session:
        user_name = session["user"]
        user = User.query.filter_by(name=user_name).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                flash(f"User {user_name} deleted successfully", "info")
            except Exception as e:
                db.session.rollback()
                flash(f"Error deleting current user: {e}", "danger")
        session.pop("user", None)
        session.pop("email", None)
        return redirect(url_for("login"))
    else:
        flash("Please log in first.", "info")
        return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        if not path.exists("database.db"):
            db.create_all()
            print("Created database!")
    app.run()
