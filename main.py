from flask import Flask, render_template, jsonify, request
import requests
import json

app = Flask(__name__)

# 공공데이터포털 API 설정
API_KEY = "431d8a7111c92b687de7283810ab476b8d0c490dbf86be618cf4d2117ef89f9c"
BASE_URL = "http://apis.data.go.kr/1480523/MetalMeasuringResultService/MetalService"

# 측정소 정보
STATIONS = [
    ["1", "수도권"], ["2", "백령도"], ["3", "호남권"], ["4", "중부권"],
    ["5", "제주권"], ["6", "영남권"], ["7", "경기권"], ["8", "충청권"],
    ["9", "전북권"], ["10", "강원권"], ["11", "충북권"]
]

# 성분 정보
ITEMS = {
    "90303": "납(Pb)", "90304": "니켈(Ni)", "90305": "망간(Mn)",
    "90314": "아연(Zn)", "90319": "칼슘(Ca)", "90318": "칼륨(K)", "90325": "황(S)"
}

@app.route('/')
def index():
    # 메인 웹 페이지 렌더링
    return render_template('index.html')

@app.route('/fetch_data')
def fetch_data():
    search_date = request.args.get('date', '').replace('-', '')
    timecode = request.args.get('timecode', 'RH02')

    if not search_date:
        return jsonify({"error": "날짜를 선택해주세요."}), 400

    params = {
        'serviceKey': API_KEY,
        'pageNo': '1',
        'numOfRows': '100',
        'resultType': 'JSON',
        'date': search_date,
        'timecode': timecode
    }

    try:
        # 파이썬 서버에서 직접 API 호출 (CORS 문제 없음)
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # 공공데이터 API는 오류 시 XML을 반환하는 경우가 있으므로 예외 처리 필요
        try:
            data = response.json()
        except:
            return jsonify({"error": "API 응답 형식이 올바르지 않습니다. (JSON 파싱 실패)"}), 500

        # 데이터 구조 정규화 및 처리 로직
        raw_items = []
        if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
            items_content = data['response']['body']['items']
            if isinstance(items_content, dict) and 'item' in items_content:
                raw_items = items_content['item'] if isinstance(items_content['item'], list) else [items_content['item']]
            elif isinstance(items_content, list):
                raw_items = items_content

        # 가공된 데이터 반환
        processed_data = process_items(raw_items)
        return jsonify(processed_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_items(items):
    station_map = dict(STATIONS)
    result = {}
    
    for item in items:
        s_code = str(item.get('stationcode', item.get('stationCode', '')))
        i_code = str(item.get('itemcode', item.get('itemCode', '')))
        val = item.get('value', '자료 없음')
        s_date = str(item.get('sdate', ''))
        
        if s_code not in result:
            result[s_code] = {
                "station": station_map.get(s_code, f"코드 {s_code}"),
                "time": f"{s_date[:4]}-{s_date[4:6]}-{s_date[6:8]} {s_date[8:10]}:{s_date[10:12]}" if len(s_date) >= 12 else "시간 정보 없음",
                "values": {}
            }
        
        result[s_code]["values"][ITEMS.get(i_code, f"코드 {i_code}")] = val
        
    return list(result.values())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
