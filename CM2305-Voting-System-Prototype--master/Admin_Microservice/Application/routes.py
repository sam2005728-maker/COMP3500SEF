import os
import uuid
import hashlib
from flask import render_template, url_for, request, redirect, flash, session
from sqlalchemy.orm import load_only
from werkzeug.security import generate_password_hash, check_password_hash
from Application import app, db
from flask_login import login_user, current_user, logout_user, login_required
from Application.forms import Officials_Registration, loginForm, CreateElectionForm
from Application.models import Official, Election, Candidates, PoliticalParty
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

@app.route("/")
@app.route("/home")
@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template('officials_home.html', title="Online Vote System")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = Official.query.filter_by(Email=form.email.data).first()
        if user is not None and user.PwdHash == hashlib.sha256(form.password.data.encode()).hexdigest():
            login_user(user)
            flash("Login Successful", 'success')
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password!", 'danger')
            return redirect(url_for('login'))
    return render_template('officials_login.html', title="Online Vote - Login", form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = Officials_Registration()
    if form.validate_on_submit():
        password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
        user = Official(
            OfficialUId=str(uuid.uuid4()),
            FirstName=form.firstname.data,
            Surname=form.lastname.data,
            Email=form.email.data,
            PwdHash=password_hash
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('officials_register.html', title="Register as an Official", form=form)

@app.route("/create_election", methods=['GET', 'POST'])
def create_election():
    form = CreateElectionForm()
    if form.validate_on_submit():
        date_str = str(form.election_date.data)
        
        start_str = str(form.start_time.data).strip()
        if ":" not in start_str:
            start_str = f"{int(start_str):02d}:00"
            
        end_str = str(form.end_time.data).strip()
        if ":" not in end_str:
            end_str = f"{int(end_str):02d}:00"

        start_dt = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")

        new_election = Election(
            Name=form.title.data,
            StartDate=start_dt,
            EndDate=end_dt
        )
        db.session.add(new_election)
        db.session.commit()
        flash("Successfully Created Election!", "success")
        return redirect(url_for('index'))
    return render_template("create_election.html", title="Create Election", form=form)

@app.route('/view_election')
def view_election():
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Election")
    data = cursor.fetchall()
    return render_template('view_election.html', title='View Election', data=data)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/results", methods=['GET', 'POST'])
def results():
    return render_template("results.html", title="Election Results", url="/../static/images/results_plot.png")

@app.route("/add_candidate", methods=['GET', 'POST'])
@login_required
def add_candidate():
    if request.method == 'POST':
        cabinet_name = request.form.get('cabinet_name')
        if cabinet_name:
            new_cabinet = PoliticalParty(UId=str(uuid.uuid4()), Name=cabinet_name)
            db.session.add(new_cabinet)
            db.session.commit()
            flash("Student Union Cabinet added successfully!", "success")
            return redirect(url_for('add_candidate'))
        cabinets = sorted(
        PoliticalParty.query.all(),
        key=lambda p: (1 if 'abstain' in p.Name.lower() else 0, p.Name)
    )

    return render_template("add_candidate.html", title="Add Student Union Cabinet", cabinets=cabinets)

@app.route("/delete_candidate/<uid>", methods=['POST'])
@login_required
def delete_candidate(uid):
    cabinet = PoliticalParty.query.get(uid)
    if cabinet:
        db.session.delete(cabinet)
        db.session.commit()
        flash("Cabinet deleted!", "success")
    return redirect(url_for('add_candidate'))

