from flask import Blueprint, request, redirect, render_template_string
from models.user import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import re


auth = Blueprint("auth", __name__)



login_html = """
<style>
body{
    font-family:Arial;
    background:#f2f4f7;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

.card{
    background:white;
    padding:40px;
    border-radius:10px;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    width:320px;
}

.toast{
    background:#ff4d4d;
    color:white;
    padding:8px;
    border-radius:6px;
    margin-bottom:10px;
    text-align:center;
}

input{
    width:100%;
    padding:10px;
    margin-top:10px;
    border-radius:6px;
    border:1px solid #ccc;
}

button{
    width:100%;
    padding:10px;
    margin-top:15px;
    border:none;
    border-radius:6px;
    background:#007bff;
    color:white;
}

a{
    display:block;
    margin-top:10px;
    text-align:center;
}
</style>

<div class="card">

{% if error %}
<div class="toast">{{error}}</div>
{% endif %}

<h2>Login</h2>

<form method="POST">
<input name="username" placeholder="Username" required>
<input name="password" type="password" placeholder="Password" required>
<button>Login</button>
</form>

<a href="/register">Create Account</a>

</div>
"""


@auth.route("/", methods=["GET","POST"])
@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            if user.role == "admin":
                return redirect("/admin")

            return redirect("/feedback")

        return render_template_string(login_html,
                                      error="Invalid username or password")

    return render_template_string(login_html, error=None)




register_html = """
<style>
body{
    font-family:Arial;
    background:#f2f4f7;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

.card{
    background:white;
    padding:40px;
    border-radius:10px;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    width:320px;
}

.toast{
    background:#ff4d4d;
    color:white;
    padding:8px;
    border-radius:6px;
    margin-bottom:10px;
    text-align:center;
}

input{
    width:100%;
    padding:10px;
    margin-top:10px;
    border-radius:6px;
    border:1px solid #ccc;
}

button{
    width:100%;
    padding:10px;
    margin-top:15px;
    border:none;
    border-radius:6px;
    background:#28a745;
    color:white;
}

a{
    display:block;
    margin-top:10px;
    text-align:center;
}
</style>

<div class="card">

{% if error %}
<div class="toast">{{error}}</div>
{% endif %}

<h2>Register</h2>

<form method="POST">
<input name="username" placeholder="Username" required>
<input name="password" type="password" placeholder="Password" required>
<button>Register</button>
</form>

<a href="/login">Back to Login</a>

</div>
"""


@auth.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Strong password
        pattern = r'^(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]{4,16}$'

        if not re.match(pattern, password):
            return render_template_string(
                register_html,
                error="Password must be 4-16 chars with a number & special character"
            )

        if User.query.filter_by(username=username).first():
            return render_template_string(
                register_html,
                error="User already exists"
            )

        hashed_password = generate_password_hash(password)

        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template_string(register_html, error=None)




@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
