from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Workout
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://m13:d00d00br41n@localhost:5433/strength_training'
db.init_app(app)

with app.app_context():
    db.create_all()

exercises = ["SQUAT", "BENCH PRESS", "DEADLIFT", "OVERHEAD PRESS", "PULLUPS"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        exercise = request.form['exercise']
        reps = int(request.form['reps'])
        weight = float(request.form['weight'])
        notes = request.form['notes']

        workout = Workout(date=date, exercise=exercise, reps=reps, weight=weight, notes=notes)
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('index'))

    today = datetime.date.today()
    previous_workouts = Workout.query.filter_by(date=today).all()
    return render_template('index.html', today=today, exercises=exercises, previous_workouts=previous_workouts)

@app.route('/edit/<int:workout_id>', methods=['GET', 'POST'])  # New route
def edit_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if request.method == 'POST':
        workout.exercise = request.form['exercise']
        workout.reps = int(request.form['reps'])  # Make sure 'reps' is in your form
        workout.weight = float(request.form['weight'])
        workout.notes = request.form['notes']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', workout=workout, exercises=exercises)  # New template

if __name__ == '__main__':
    app.run(debug=True)