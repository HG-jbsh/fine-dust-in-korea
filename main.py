import requests
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate

class MetalMonitoringSystem:
    def __init__(self):
        # 기본 정보 설정
        self.api_key = "431d8a7111c92b687de7283810ab476b8d0c490dbf86be618cf4d2117ef89f9c"
        self.endpoint = "https://apis.data.go.kr/1480523/MetalMeasuringResultService/MetalService"
        self.admin = "1416현겸"
        
        # 측정소 및 항목 매핑
        self.stations = {
            "1": "수도권", "2": "백령도", "3": "호남권", "4": "중부권",
            "5": "제주권", "6": "영남권", "7": "경기권", "8": "충청권",
            "9": "전북권", "10": "강원권", "11": "충북권"
        }
        self.items = {
            "90303": "납(Pb)", "90304": "니켈(Ni)", "90305": "망간(Mn)",
            "90314": "아연(Zn)", "90319": "칼슘(Ca)", "90318": "칼륨(K)", "90325": "황(S)"
        }

    def print_banner(self):
        """시스템 시작 배너 출력"""
        border = "═" * 60
        print(f"\n{border}")
        print(f"║{' ':^58}║")
        print(f"║{'[ 미세먼지 금속성분 모니터링 시스템 ]':^50}║")
        print(f"║{'시스템 관리자: ' + self.admin:^52}║")
        print(f"║{' ':^58}║")
        print(f"{border}")

    def fetch_api_data(self, date_str, timecode="RH02"):
        """API 호출 및 데이터 정리"""
        params = {
            "ServiceKey": self.api_key,
            "pageNo": "1",
            "numOfRows": "100",
            "resultType": "JSON",
            "date": date_str.replace("-", ""),
            "timecode": timecode
        }

        print(f"\n[알림] {self.admin} 관리자 인증으로 데이터를 요청 중...")
        
        try:
            response = requests.get(self.endpoint, params=params, verify=True, timeout=15)
            res_json = response.json()
            
            raw_items = res_json.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            if not raw_items:
                return None

            # 데이터 가공
            parsed_list = []
            for row in raw_items:
                s_code = str(row.get('stationcode'))
                i_code = str(row.get('itemcode'))
                
                parsed_list.append({
                    "지역": self.stations.get(s_code, s_code),
                    "성분": self.items.get(i_code, i_code),
                    "농도(ng/m³)": row.get('value'),
                    "측정시간": row.get('sdate')
                })

            df = pd.DataFrame(parsed_list)
            # 표 형태로 변환 (피벗)
            return df.pivot(index='지역', columns='성분', values='농도(ng/m³)')

        except Exception as e:
            print(f"❌ 데이터 로드 실패: {e}")
            return None

    def run(self):
        self.print_banner()
        
        # 날짜 입력 (기본값 어제)
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        input_date = input(f"📅 조회 날짜 입력 (예: {yesterday}, 미입력시 어제): ").strip()
        target_date = input_date if input_date else yesterday

        result = self.fetch_api_data(target_date)

        if result is not None:
            print(f"\n✅ {target_date} 측정 데이터 리포트 (관리자: {self.admin})")
            print(tabulate(result, headers='keys', tablefmt='fancy_grid'))
            print(f"\n[출처] 환경부 국립환경과학원 | 시스템 운영자: {self.admin}")
        else:
            print(f"\n데이터가 없거나 호출에 실패했습니다. (입력일: {target_date})")

if __name__ == "__main__":
    system = MetalMonitoringSystem()
    system.run()
