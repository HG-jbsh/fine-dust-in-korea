import requests
import pandas as pd
import plotly.express as px
import urllib.parse

# 1. API 데이터 가져오기
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

response = requests.get(url, params=params)
items = response.json()['response']['body']['items']

# 2. Pandas로 데이터 정리
df = pd.DataFrame(items)
# 수치형 데이터로 변환 (결측치는 0으로 처리)
df['pm10Value'] = pd.to_numeric(df['pm10Value'], errors='coerce').fillna(0)

# 3. Plotly로 시각화 (인터랙티브 그래프)
fig = px.bar(df, x='stationName', y='pm10Value', 
             color='pm10Value', 
             title='전국 미세먼지(PM10) 현황',
             labels={'stationName': '측정소', 'pm10Value': '미세먼지 농도'})

# 4. HTML 파일로 저장 (핵심!)
# 이 index.html 파일을 GitHub에 올리면 됩니다.
fig.write_html("index.html")

print("index.html 파일이 생성되었습니다. 이제 GitHub에 업로드하세요!")
