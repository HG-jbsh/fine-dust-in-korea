from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET
from urllib.parse import unquote

app = Flask(__name__)

# 네 공공데이터 API 인증키 넣기
SERVICE_KEY = "431d8a7111c92b687de7283810ab476b8d0c490dbf86be618cf4d2117ef89f9c"

@app.route('/')
def home():
    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"

    params = {
        "serviceKey": SERVICE_KEY,
        "returnType": "xml",
        "numOfRows": "10",
        "pageNo": "1",
        "sidoName": "전북",
        "ver": "1.0"
    }

    response = requests.get(url, params=params)

    stations = []

    if response.status_code == 200:
        root = ET.fromstring(response.text)

        for item in root.findall(".//item"):
            station = {
                "name": item.findtext("stationName"),
                "pm10": item.findtext("pm10Value"),
                "pm25": item.findtext("pm25Value")
            }
            stations.append(station)

    return render_template("index.html", stations=stations)

if __name__ == "__main__":
    app.run(debug=True)
