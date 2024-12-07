from flask import Flask, render_template, request, redirect, jsonify
from utils.db import db
from models.ipl_player import *  # Ensure this matches your file structure

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IPL.db'  # Updated database for IPL players
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    players = IPLPlayer.query.all()
    return render_template('index.html', content=players)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        message = request.form.get('message').strip()

        # Validate the inputs
        if not name or not email or not message:
            return jsonify({"status": "error", "message": "All fields are required."}), 400

        # Save the data to the database
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        try:
            db.session.commit()
            return jsonify({"status": "success", "message": "Thank you for contacting us!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": "An error occurred while saving your data."}), 500

    # Render the contact form for GET request
    return render_template('contact.html')





@app.route('/matches')
def matches():
    matches = Matches.query.all()
    return render_template('matches.html', matches=matches)


@app.route('/matches')
def matches_page():
    return render_template('matches.html')






@app.route('/players')
def players():
    players = IPLPlayer.query.all()
    return render_template('players_list.html', players=players)




@app.route('/submit', methods=['POST'])
def submit():
    player = IPLPlayer(
        player_id=request.form['player_id'],
        player_name=request.form['player_name'],
        team=request.form['team'],
        matches_played=request.form['matches_played'],
        runs_scored=request.form.get('runs_scored', 0),
        wickets_taken=request.form.get('wickets_taken', 0),
    )
    db.session.add(player)
    db.session.commit()
    return redirect('/players')



@app.route('/update/<int:player_id>', methods=['POST'])
def update_player(player_id):
    player = IPLPlayer.query.get_or_404(player_id)
    player.player_name = request.form['player_name']
    player.team = request.form['team']
    player.matches_played = request.form['matches_played']
    player.runs_scored = request.form['runs_scored']
    player.wickets_taken = request.form['wickets_taken']
    db.session.commit()
    return jsonify({'message': 'Player updated successfully'})


@app.route('/delete/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = IPLPlayer.query.get(player_id)
    if not player:
        return jsonify({'message': 'Player not found'}), 404
    try:
        db.session.delete(player)
        db.session.commit()
        return jsonify({'message': 'Player deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {e}'}),500


@app.route('/teams', methods=['GET'])
def view_teams():
    teams = Teams.query.all()
    return render_template('teams.html', teams=teams)

@app.route('/submit_team', methods=['POST'])
def submit_team():
    team = Teams(
        team_name=request.form['team_name'],
        team_captain=request.form['team_captain'],
        championships_won=request.form['championships_won']
    )
    db.session.add(team)
    db.session.commit()
    return redirect('/teams')

@app.route('/update_team/<int:team_id>', methods=['POST'])
def update_team(team_id):
    team = Teams.query.get_or_404(team_id)
    team.team_name = request.form['team_name']
    team.team_captain = request.form['team_captain']
    team.championships_won = request.form['championships_won']
    db.session.commit()
    return jsonify({'message': 'Team updated successfully'})

@app.route('/delete_team/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = Teams.query.get(team_id)
    if not team:
        return jsonify({'message': 'Team not found'}), 404
    try:
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Team deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {e}'}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003,debug=True)
