from flask import Flask, render_template
import requests
import urllib.parse

app = Flask(__name__)

# 공공데이터포털에서 발급받은 'Decoding' 인증키를 입력하세요
API_KEY = '431d8a7111c92b687de7283810ab476b8d0c490dbf86be618cf4d2117ef89f9c'

@app.route('/')
def get_air_quality():
    # 1. API URL 설정 (시도별 실시간 측정정보 조회)
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
    
    # 2. 요청 파라미터 설정
    params = {
        'serviceKey': urllib.parse.unquote(API_KEY), # 인증키 디코딩 처리
        'returnType': 'json',
        'numOfRows': '100',
        'pageNo': '1',
        'sidoName': '전국', # '전국', '서울', '전북' 등 지정 가능
        'ver': '1.0'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # 데이터 추출 (결과 코드 및 항목 확인)
        items = data['response']['body']['items']
        return render_template('index.html', items=items)
        
    except Exception as e:
        return f"데이터를 불러오는 중 오류가 발생했습니다: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
