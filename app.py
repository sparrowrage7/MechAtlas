
import os
import sqlite3

from flask import Flask, render_template, request
from ai_generator import generate_manual
import markdown
import bleach


app = Flask(__name__)


# =====================================
# DATABASE CONNECTION
# =====================================

def get_db():

    # Local Windows database
    if os.environ.get("VERCEL"):
        db_path = "/tmp/mechatlas.db"

    # Vercel temporary database
    else:
        db_path = "database.db"

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn


# =====================================
# CREATE DATABASE TABLE
# =====================================

def create_table():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_name TEXT NOT NULL,
            manufacturer TEXT,
            model_number TEXT,
            purpose TEXT NOT NULL,
            working_principle TEXT,
            components TEXT,
            safety TEXT
        )
    """)

    conn.commit()
    conn.close()


# =====================================
# HOMEPAGE
# =====================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================
# MACHINE INFORMATION FORM
# =====================================

@app.route("/create")
def create():

    return render_template("machine_form.html")


# =====================================
# GENERATE TECHNICAL MANUAL
# =====================================

@app.route("/generate", methods=["POST"])
def generate():

    # Get information from the form

    machine_name = request.form.get(
        "machine_name", ""
    ).strip()

    manufacturer = request.form.get(
        "manufacturer", ""
    ).strip()

    model_number = request.form.get(
        "model_number", ""
    ).strip()

    purpose = request.form.get(
        "purpose", ""
    ).strip()

    working_principle = request.form.get(
        "working_principle", ""
    ).strip()

    components = request.form.get(
        "components", ""
    ).strip()

    safety = request.form.get(
        "safety", ""
    ).strip()


    # Check required machine name

    if not machine_name:

        return render_template(
            "machine_form.html",
            error="Please enter a machine name."
        ), 400


    # Prepare information for AI

    machine_details = f"""
Machine Name: {machine_name}
Manufacturer: {manufacturer or "Not provided"}
Model Number: {model_number or "Not provided"}
Purpose: {purpose or "Not provided"}
Working Principle: {working_principle or "Not provided"}
Components: {components or "Not provided"}
Safety Information: {safety or "Not provided"}
"""


    # Generate manual using Gemini AI

    try:

        print("MechAtlas: Connecting to Gemini AI...")

        ai_manual = generate_manual(machine_details)

        if not ai_manual:
            raise ValueError("AI returned an empty manual.")

        print("MechAtlas: Manual generated successfully.")

    except Exception as error:

        print("AI Generation Error:", error)

        return render_template(
            "machine_form.html",
            error="Manual generation failed. Please try again."
        ), 500


    # =====================================
    # CONVERT MARKDOWN INTO HTML
    # =====================================

    ai_manual_html = markdown.markdown(
        ai_manual,
        extensions=[
            "extra",
            "sane_lists"
        ]
    )


    # =====================================
    # SANITIZE GENERATED HTML
    # =====================================

    allowed_tags = [
        "h1", "h2", "h3", "h4", "h5",
        "p", "br", "hr",
        "strong", "b", "em", "i",
        "ul", "ol", "li",
        "blockquote",
        "pre", "code",
        "table", "thead", "tbody",
        "tr", "th", "td"
    ]

    ai_manual_html = bleach.clean(
        ai_manual_html,
        tags=allowed_tags,
        attributes={},
        strip=True
    )


    # =====================================
    # SAVE MACHINE INFORMATION TO DATABASE
    # =====================================

    conn = None

    try:

        conn = get_db()

        cursor = conn.execute("""
            INSERT INTO machines (
                machine_name,
                manufacturer,
                model_number,
                purpose,
                working_principle,
                components,
                safety
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            machine_name,
            manufacturer,
            model_number,
            purpose,
            working_principle,
            components,
            safety
        ))

        machine_id = cursor.lastrowid

        conn.commit()

    except sqlite3.Error as error:

        print("Database Error:", error)

        if conn:
            conn.rollback()

        return (
            "Manual generated, but database saving failed. "
            "Please try again."
        ), 500

    finally:

        if conn:
            conn.close()


    # =====================================
    # DISPLAY FORMATTED MANUAL
    # =====================================

    return render_template(
        "manual.html",

        machine_id=machine_id,
        machine_name=machine_name,
        manufacturer=manufacturer,
        model_number=model_number,
        purpose=purpose,
        working_principle=working_principle,
        components=components,
        safety=safety,

        ai_manual=ai_manual,
        ai_manual_html=ai_manual_html
    )


# =====================================
# RUN MECHATLAS
# =====================================

create_table()

if __name__ == "__main__":
    app.run(debug=True)
