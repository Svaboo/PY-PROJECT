from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Workout
from . import db
import json
import requests

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    workout_name = None
    note = None
    reps = None
    weight = None
    workout_id = None
    
    if request.method == 'POST': 
        workout_name = request.form.get('workout')
        note = request.form.get('note')  
        reps = request.form.get('reps')  
        weight = request.form.get('weight')
        workout_id = request.form.get('workout_id')

    if workout_name:
        if len(workout_name) < 1:
            flash('Workout name is too short!', category='error')
        else:
            new_workout = Workout(data=workout_name, user_id=current_user.id)
            db.session.add(new_workout)
            db.session.commit()
            flash('Workout added!', category='success') 
            return redirect(url_for('views.home'))
                   
    elif note:
        if not workout_id or not Workout.query.get(workout_id):
            flash('Add a workout first!', category='error')
        elif len(note) < 1:
            flash('Exercise name is too short!', category='error') 
        elif not reps or int(reps) < 1 or int(reps) > 100:
            flash('Reps must be a number between 1 and 100!', category='error')
        elif not weight or float(weight) < 0:
            flash('Weight must be a non-negative number!', category='error')
        else:
            new_note = Note(data=note, reps=int(reps), weight=float(weight), user_id=current_user.id, workout_id=workout_id) 
            db.session.add(new_note)
            db.session.commit()
            flash('Exercise added!', category='success')
            return redirect(url_for('views.home'))
        
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, workouts=workouts)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/delete-workout', methods=['POST'])
def delete_workout():  
    workout = json.loads(request.data)
    workout_id = workout['workoutId']
    workout = Workout.query.get(workout_id)
    if workout:
        if  workout.user_id == current_user.id:
            db.session.delete(workout)
            db.session.commit()

    return jsonify({})

@views.route('/records', methods=['GET', 'POST'])
def records():
    notes = []
    if request.method == 'POST':
        search_query = request.form.get('records')
        if search_query:
            notes = Note.query.filter(
                Note.data.ilike(f"%{search_query}%"),
                Note.user_id == current_user.id
            ).all()
    return render_template("records.html", user=current_user, notes=notes)

@views.route('/profile', methods=['GET'])
@login_required
def profile():

    num_workouts = Workout.query.filter_by(user_id=current_user.id).count()
    num_exercises = Note.query.filter_by(user_id=current_user.id).count()
    username = current_user.first_name

    return render_template(
        "profile.html",
        user=current_user,
        num_workouts=num_workouts,
        num_exercises=num_exercises,
        username=username
    )