from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# 공공데이터 API 설정
API_KEY = '431d8a7111c92b687de7283810ab476b8d0c490dbf86be618cf4d2117ef89f9c'
API_URL = 'http://apis.data.go.kr/1483000/FinedustMetalInfoService/getMetalItemBssrInfo'

@app.route('/')
def index():
    # templates/index.html 파일을 읽어서 사용자 브라우저에 전달합니다.
    return render_template('index.html')

@app.route('/api/dust')
def get_dust_data():
    params = {
        'serviceKey': API_KEY,
        'pageNo': '1',
        'numOfRows': '10',
        'resultType': 'json',
        'date': '20260510',  # 실제 운영 시에는 라이브러리를 통해 오늘 날짜를 동적으로 넣어야 합니다.
        'stationCode': '1'    
    }
    
    try:
        # 서버에서 직접 API를 호출하므로 CORS 문제가 발생하지 않습니다.
        response = requests.get(API_URL, params=params)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 5000번 포트에서 서버 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
