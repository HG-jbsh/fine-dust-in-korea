import requests
import pandas as pd
import plotly.express as px
import urllib.parse
from datetime import datetime

def build_website():
    # 1. API 설정 (에어코리아 전국 미세먼지)
    API_KEY = '431d8a7111c92b687de7283810ab476b8d0c490dbf86be618cf4d2117ef89f9c'
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
    
    params = {
        'serviceKey': urllib.parse.unquote(API_KEY),
        'returnType': 'json',
        'numOfRows': '100',
        'pageNo': '1',
        'sidoName': '전국',
        'ver': '1.0'
    }

    try:
        # 2. 데이터 수집 및 가공
        response = requests.get(url, params=params)
        items = response.json()['response']['body']['items']
        df = pd.DataFrame(items)
        
        # 수치 데이터 변환
        df['pm10Value'] = pd.to_numeric(df['pm10Value'], errors='coerce').fillna(0)
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 3. 시각화 (Plotly 활용)
        fig = px.bar(df, x='stationName', y='pm10Value', color='pm10Value',
                     title=f'전국 미세먼지 현황 (최근 업데이트: {update_time})',
                     labels={'stationName': '측정소', 'pm10Value': '미세먼지(PM10)'})
        
        # 4. HTML 파일 저장 (GitHub Pages가 인식할 파일)
        fig.write_html("index.html", include_plotlyjs='cdn')
        print("index.html 생성 완료")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    build_website()
