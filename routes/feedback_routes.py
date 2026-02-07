from flask import Blueprint, request, redirect, render_template_string
from flask_login import login_required, current_user
from models.feedback import Feedback
from extensions import db


feedback_bp = Blueprint("feedback", __name__)




@feedback_bp.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():

    

    if request.method == "POST":

        text = request.form.get("text", "").strip()
        update_id = request.form.get("update_id")

        # Prevent empty feedback
        if not text:
            return redirect("/feedback")

        # UPDATE
        if update_id:

            fb = db.session.get(Feedback, int(update_id))

            # Ownership protection 
            if fb and fb.user_id == current_user.id:
                fb.text = text
                db.session.commit()

            # ALWAYS redirect
            return redirect("/feedback")

        # NEW FEEDBACK
        new_feedback = Feedback(
            text=text,
            user_id=current_user.id
        )

        db.session.add(new_feedback)
        db.session.commit()

        return redirect("/feedback")


    

    feedbacks = db.session.query(Feedback)\
        .filter_by(
            user_id=current_user.id,
            is_deleted=False
        )\
        .order_by(Feedback.id.desc())\
        .all()


   

    feedback_cards = ""

    for f in feedbacks:
        feedback_cards += f"""
        <div class='card'>
            <form method="POST">

                <textarea name="text">{f.text}</textarea>

                <input type="hidden"
                       name="update_id"
                       value="{f.id}">

                <button class="update">
                    Update Feedback
                </button>

            </form>
        </div>
        """


    

    return render_template_string(f"""

<style>

body{{
    font-family:Arial;
    background:#eef1f5;
    margin:0;
}}

.navbar{{
    background:#007bff;
    color:white;
    padding:15px 30px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}}

.logout{{
    background:#dc3545;
    padding:8px 14px;
    border-radius:6px;
    color:white;
    text-decoration:none;
}}

.container{{
    width:500px;
    margin:40px auto;
}}

.card{{
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0 4px 12px rgba(0,0,0,0.1);
    margin-top:10px;
}}

textarea{{
    width:100%;
    padding:10px;
    border-radius:6px;
    border:1px solid #ccc;
}}

button{{
    padding:8px 14px;
    border:none;
    border-radius:6px;
    background:#28a745;
    color:white;
    margin-top:6px;
    cursor:pointer;
}}

.update{{
    background:#ffc107;
    color:black;
}}

</style>


<div class="navbar">
    <h2>User Dashboard</h2>
    <a class="logout" href="/logout">Logout</a>
</div>


<div class="container">

    <div class="card">

        <h3>Submit Feedback</h3>

        <form method="POST">

            <textarea name="text"
                      placeholder="Write your feedback..."
                      required></textarea>

            <button>
                Submit Feedback
            </button>

        </form>

    </div>


    <h3>Your Previous Feedback</h3>

    {feedback_cards}

</div>

""")
