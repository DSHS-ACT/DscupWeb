from flask import Flask, request, jsonify, render_template, send_from_directory
import csv
import os

app = Flask(__name__)
votes_db = {}
players_db = {}
def load_players():
    with open('static/player.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            player_number = row['number']
            players_db[player_number] = {
                'name': row['name'],
                'leader': row['leader'],
                'height': row['height'],
                'weight': row['weight'],
                'position': row['position'],
                'main_foot': row['main_foot'],
                'votes': int(row['votes']) if 'votes' in row else 0
            }
@app.route('/main')
def main():
    return render_template('main.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    player_number = data.get('player_number')
    device_id = data.get('device_id')

    if not device_id:
        return jsonify({'error': '기기 식별자가 필요합니다'}), 400
    if player_number not in players_db:
        return jsonify({'error': '유효하지 않은 선수 번호입니다'}), 400
    if device_id in votes_db:
        return jsonify({'error': '이미 투표하셨습니다'}), 403

    votes_db[device_id] = player_number
    players_db[player_number]['votes'] += 1
    return jsonify({'message': '투표가 성공적으로 기록되었습니다'})

@app.route('/players', methods=['GET'])
def players():
    return jsonify(players_db)

if __name__ == '__main__':
    load_players()
    app.run(port=8000, debug=True)