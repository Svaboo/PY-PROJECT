from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Workout
from . import db
import json

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
                   
    elif note:
        if not workout_id or not Workout.query.get(workout_id):
            flash('Add a workout first!', category='error')
        elif len(note) < 1:
            flash('Exercise name is too short!', category='error') 
        elif not reps or int(reps) < 1:
            flash('Reps must be a positive number!', category='error')
        elif not weight or float(weight) < 0:
            flash('Weight must be a non-negative number!', category='error')
        else:
            new_note = Note(data=note, reps=int(reps), weight=float(weight), user_id=current_user.id, workout_id=workout_id) 
            db.session.add(new_note)
            db.session.commit()
            flash('Exercise added!', category='success')

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


