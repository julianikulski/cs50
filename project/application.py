import os
import re
from flask import Flask, jsonify, render_template, request

# Configure application
app = Flask(__name__)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""

    inputs = ["abstandwaende", "winkel", "sitzhoehe", "gewicht"]
    placeholders = ["Abstand", "Winkel", "Sitzhöhe", "Gewicht"]
    results = []

    for item in range(len(inputs)):
        if not request.form.get(inputs[item]):
            results.append(placeholders[item])
        else:
            results.append(request.form.get(inputs[item]))

    return render_template("index.html", waende=results[0], winkel=results[1], hoehe=results[2], gewicht=results[3])

