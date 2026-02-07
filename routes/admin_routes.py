from flask import Blueprint, redirect, request, render_template_string
from flask_login import login_required, current_user
from models.feedback import Feedback
from models.user import User
from extensions import db


admin_bp = Blueprint("admin", __name__)



@admin_bp.route("/admin")
@login_required
def admin():

    if current_user.role != "admin":
        return "Access denied"

    
    feedbacks = db.session.query(Feedback)\
        .filter_by(is_deleted=False)\
        .order_by(Feedback.id.desc()).all()

    rows = ""

    for f in feedbacks:
        user = db.session.get(User, f.user_id)

        rows += f"""
        <tr>
            <td>{user.username}</td>
            <td>{f.text[:50]}...</td>

            <td>
                <a class="view" href="/view/{f.id}">View</a>
                <a class="edit" href="/edit/{f.id}">Edit</a>
                <a class="delete"
                   onclick="return confirm('Delete this feedback?')"
                   href="/delete/{f.id}">
                   Delete
                </a>
            </td>
        </tr>
        """

    return f"""
    <style>
        body {{
            font-family:Arial;
            background:#eef1f5;
            margin:0;
        }}

        .navbar {{
            background:#007bff;
            color:white;
            padding:15px 30px;
            display:flex;
            justify-content:space-between;
            align-items:center;
        }}

        .logout {{
            background:#dc3545;
            padding:8px 14px;
            border-radius:6px;
            color:white;
            text-decoration:none;
        }}

        .container {{
            padding:40px;
        }}

        table {{
            width:100%;
            border-collapse:collapse;
            background:white;
            box-shadow:0 4px 10px rgba(0,0,0,0.08);
        }}

        th, td {{
            padding:14px;
            border-bottom:1px solid #ddd;
        }}

        th {{
            background:#007bff;
            color:white;
        }}

        tr:hover {{
            background:#f5f7fa;
        }}

        a {{
            padding:6px 10px;
            border-radius:5px;
            color:white;
            text-decoration:none;
            margin-right:5px;
        }}

        .view {{ background:#17a2b8; }}
        .edit {{ background:#ffc107; color:black; }}
        .delete {{ background:#dc3545; }}

    </style>

    <div class="navbar">
        <h2>Admin Dashboard</h2>
        <a class="logout" href="/logout">Logout</a>
    </div>

    <div class="container">

        <table>
            <tr>
                <th>User</th>
                <th>Feedback</th>
                <th>Actions</th>
            </tr>

            {rows}

        </table>

    </div>
    """
    


@admin_bp.route("/view/<int:id>")
@login_required
def view_feedback(id):

    if current_user.role != "admin":
        return "Access denied"

    fb = db.session.get(Feedback, id)

    if not fb or fb.is_deleted:
        return "Feedback not found"

    user = db.session.get(User, fb.user_id)

    return f"""
    <div style="font-family:Arial; padding:40px;">

        <div style="display:flex; justify-content:space-between;">
            <h2>Feedback Detail</h2>

            <a href="/admin" style="
                background:#007bff;
                color:white;
                padding:8px 12px;
                border-radius:6px;
                text-decoration:none;">
                Back to Dashboard
            </a>
        </div>

        <br>

        <b>User:</b> {user.username}

        <br><br>

        <div style="
            background:#f4f6f8;
            padding:20px;
            border-radius:8px;
            font-size:16px;
        ">
            {fb.text}
        </div>

    </div>
    """



@admin_bp.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit_feedback(id):

    if current_user.role != "admin":
        return "Access denied"

    fb = db.session.get(Feedback, id)

    if not fb or fb.is_deleted:
        return "Feedback not found"

    if request.method == "POST":

        fb.text = request.form["text"]
        db.session.commit()

        return redirect("/admin")

    return render_template_string(f"""
    <div style="font-family:Arial; padding:40px;">

        <div style="display:flex; justify-content:space-between;">
            <h2>Edit Feedback</h2>

            <a href="/admin" style="
                background:#007bff;
                color:white;
                padding:8px 12px;
                border-radius:6px;
                text-decoration:none;">
                Back to Dashboard
            </a>
        </div>

        <br>

        <form method="POST">

            <textarea name="text"
                style="width:100%; height:150px; padding:10px;">{fb.text}</textarea>

            <br><br>

            <button style="
                background:#28a745;
                color:white;
                padding:10px 18px;
                border:none;
                border-radius:6px;
                cursor:pointer;">
                Update Feedback
            </button>

        </form>

    </div>
    """)



@admin_bp.route("/delete/<int:id>")
@login_required
def delete(id):

    if current_user.role != "admin":
        return "Access denied"

    fb = db.session.get(Feedback, id)

    if fb:
        fb.is_deleted = True
        db.session.commit()

    return redirect("/admin")
