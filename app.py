from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "cloudclass-secret"

# ---------- CONFIG ----------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# store evaluation info (simple version)
evaluation_data = {}   # {filename: {"marks": 90, "feedback": "..."}}


# ---------- HOME ----------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return redirect(url_for("home"))
    return render_template("contact.html")


# ---------- AUTH ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    return redirect(url_for("login"))


# ---------- DASHBOARD ----------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------- COURSES ----------

@app.route("/courses")
def courses():
    course_list = [
        "Cloud Computing",
        "Web Technologies",
        "Database Management Systems"
    ]
    return render_template("courses.html", courses=course_list)


# ---------- QUICK ACTIONS ----------

@app.route("/actions")
def actions():
    return render_template("actions.html")


# ---------- STUDENT PROJECTS ----------

@app.route("/student-projects", methods=["GET", "POST"])
def student_projects():

    upload_folder = app.config["UPLOAD_FOLDER"]
    projects = os.listdir(upload_folder)

    if request.method == "POST":
        file = request.files.get("project_file")

        if file and file.filename:
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)

            return redirect(url_for("student_projects"))

    return render_template("student_projects.html", projects=projects)


# ---------- EVALUATIONS ----------

@app.route("/evaluations", methods=["GET", "POST"])
def evaluations():

    upload_folder = app.config["UPLOAD_FOLDER"]
    projects = os.listdir(upload_folder)

    success_msg = None

    # handle marks + feedback submit
    if request.method == "POST":

        project = request.form.get("project")
        marks = request.form.get("marks")
        feedback = request.form.get("feedback")

        if project:
            evaluation_data[project] = {
                "marks": marks,
                "feedback": feedback
            }

            success_msg = "Evaluation submitted successfully!"

    return render_template(
        "evaluations.html",
        projects=projects,
        evaluation_data=evaluation_data,
        success_msg=success_msg
    )


# ---------- RUN ----------

if __name__ == "__main__":
    app.run(debug=True)
