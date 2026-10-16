import math
import os
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from db import init_db, insert_lead, get_lead, get_lead_heavy

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise ValueError("No SECRET_KEY set for Flask application")

RATES = {
    "mowing":   {"per_acre": 60, "minimum": 40},
    "mulching": {"per_acre": 90, "minimum": 60},
    "cleanup":  {"per_acre": 120, "minimum": 80},
}

CONDITIONS = {
    "maintained": (1.0, 1.15),
    "somewhat":   (1.25, 1.5),
    "heavy":      None,
}

MIN_ACRES = 0.1
MAX_ACRES = 5


def parse_acreage(raw):
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value):
        return None
    return value


def validate(email, service, condition, acreage):
    local, _, domain = email.partition("@")
    if not local or "." not in domain:
        return "Please enter a valid email address."
    if service not in RATES:
        return "Please choose an available service."
    if condition not in CONDITIONS:
        return "Please choose a yard condition."
    if acreage is None:
        return "Acreage must be a number."
    if acreage < MIN_ACRES or acreage > MAX_ACRES:
        return f"Acreage must be between {MIN_ACRES} and {MAX_ACRES}. For larger properties, please contact us directly."
    return None


def calculate_estimate(service, acreage, condition):
    multipliers = CONDITIONS[condition]
    if multipliers is None:
        return None
    rate = RATES[service]
    base = max(acreage * rate["per_acre"], rate["minimum"])
    low_mult, high_mult = multipliers
    return round(base * low_mult), round(base * high_mult)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/estimate", methods=["POST"])
def estimate():
    email = request.form.get("email", "").strip().lower()
    service = request.form.get("service", "").strip()
    condition = request.form.get("condition", "").strip()
    acreage = parse_acreage(request.form.get("acreage", "").strip())

    error = validate(email, service, condition, acreage)
    if error:
        flash(error)
        return redirect(url_for("home"))
    result = calculate_estimate(service, acreage, condition)
    if result is None:
        flag = insert_lead(email,service,condition,acreage, None, None)
        if flag:
            flash("Thanks! Your yard needs a quick look first. We'll reach out to schedule a free visit.")
    else:
        low, high = result
        flag = insert_lead(email,service,condition,acreage, low, high)
        if flag:
            flash(f"Your estimate is ${low} to ${high}.")
    print(get_lead(email))
    print(f"Heavy: {get_lead_heavy()}")
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
