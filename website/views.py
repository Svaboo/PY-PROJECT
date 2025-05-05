from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')  
        reps = request.form.get('reps')  
        weight = request.form.get('weight')

        if len(note) < 1:
            flash('Exercise name is too short!', category='error') 
        elif not reps or int(reps) < 1:
            flash('Reps must be a positive number!', category='error')
        elif not weight or float(weight) < 0:
            flash('Weight must be a non-negative number!', category='error')
        else:
            new_note = Note(data=note, reps=int(reps), weight=float(weight), user_id=current_user.id) 
            db.session.add(new_note)
            db.session.commit()
            flash('Exercise added!', category='success')

    return render_template("home.html", user=current_user)


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



