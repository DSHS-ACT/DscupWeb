from flask import Flask, request, jsonify, render_template, Response
import json

# Flask에서 필요한 모듈들을 임포트. / request: 클라이언트의 요청 데이터 처리
# json: Python을 JSON 문자열로 변환 / jsonify: JSON 응답 생성
# render_template: HTML 템플릿 렌더링하기. /  Response: HTTP 응답 생성

app = Flask(__name__)  # Flask 애플리케이션 인스턴스를 생성.

# 선수 목록을 저장할 리스트 초기화.
players = []  # 선수 이름을 저장하는 리스트
votes = {}  # 선수 이름을 key로, 그 선수의 투표 수를 value으로 저장

@app.route('/')
def index():
    # 사용자가 "/" (route 'URL')에 접근할 때 실행되는 함수.
    # templates 폴더에 있는 index.html 파일을 렌더링하여 반환.
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_player():
    
    player_name = request.form['name']  
    # 클라이언트로부터 전송된 폼 데이터에서 'name' 필드를 가져옴.
    
    if player_name not in players:
        # 등록된 선수가 아닌 경우
        players.append(player_name)
        # 선수를 players 리스트에 추가.
        votes[player_name] = 0
        # 해당 선수의 투표 수를 0으로 초기화하여 votes 딕셔너리에 추가.
        
        # 성공 메시지를 JSON 형식으로 생성하여 클라이언트에게 반환.
        response = Response(
            json.dumps({"message": f"{player_name} 등록됨."}, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
            #utf-8 -> 한국어 패치
        )
        return response, 200  # 200 상태 코드와 함께 응답을 반환.
    else:
        # 등록된 선수인 경우
        response = Response(
            json.dumps({"message": f"{player_name} 이미 등록됨."}, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )
        return response, 400  # 400 상태 코드와 함께 오류 메시지를 반환.

@app.route('/vote', methods=['POST'])
def vote_player():
    # 누군가가 투표를 할 때 POST 요청을 처리.
    
    player_name = request.form['name']
    # 클라이언트로부터 전송된 데이터에서 'name' 필드를 가져오기.
    
    if player_name in players:
        # 입력된 이름이 등록된 선수인 경우
        votes[player_name] += 1
        # 해당 선수의 투표 수를 1 증가시킴ㅁ.
        
        response = Response(
            json.dumps({"message": f"{player_name}에게 투표됨."}, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )
        return response, 200  # 200 OK 상태 코드와 함께 응답을 반환.
    else:
        # 입력된 이름이 등록되지 않은 선수인 경우
        response = Response(
            json.dumps({"message": f"{player_name}은(는) 등록되지 않음."}, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )
        return response, 400  # 400 상태 코드와 함께 오류 메시지를 반환.

@app.route('/results', methods=['GET'])
def show_results():
    # 클라이언트가 투표 결과를 요청 -> GET 요청을 처리.
    
    sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)
    # votes 항목을 투표 수(item[1])에 따라 내림차순 정렬.
    # 정렬된 결과는 리스트 형태로 반환.
    
    response = Response(
        json.dumps(sorted_votes, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )
    return response, 200  # 200 상태 코드와 함께 정렬된 투표 결과를 JSON 형식으로 반환.

if __name__ == '__main__':
    # Flask 개발 서버를 시작합니다.
    app.run(debug=True, port=5001)
    # 개발 중 발생하는 오류 디버깅.
    # 서버는 포트 5001번에서 실행.
