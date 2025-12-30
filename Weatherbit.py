import requests
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime, timedelta



#하루 날씨 데이터 가져오는 함수 
def fetch_weatherbit_day(api_key, lat, lon, date):
    url = "https://api.weatherbit.io/v2.0/history/hourly"
    start_date = date.strftime('%Y-%m-%d')
    end_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')
    
    params = {
        'lat': lat,
        'lon': lon,
        'start_date': start_date,
        'end_date': end_date,
        'tz': 'local',
        'key': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"[ERROR] {start_date} 요청 실패: {response.status_code}")
        return pd.DataFrame()

    data = response.json()
    if 'data' not in data or not data['data']:
        print(f"[WARN] {start_date} 데이터 없음")
        return pd.DataFrame()

    records = []
    for item in data['data']:
        records.append({
            'datetime': item.get('timestamp_local'),
            'temp(C)': item.get('temp'),
            'dew_point(C)': item.get('dewpt'),
            'humidity(%)': item.get('rh'),
            'pressure(hPa)': item.get('pres'),
            'visibility(km)': item.get('vis'),
            'wind_speed(m/s)': item.get('wind_spd'),
            'wind_dir(deg)': item.get('wind_dir'),
            'clouds(%)': item.get('clouds'),
            'solar_rad(W/m2)': item.get('solar_rad'),
            'ghi(W/m2)': item.get('ghi'),
            'dhi(W/m2)': item.get('dhi'),
            'dni(W/m2)': item.get('dni'),
            'precip(mm)': item.get('precip')
        })

    df = pd.DataFrame(records)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.rename(columns={
    'temp(C)'         : 'temp',
    'dew_point(C)'    : 'dew_point',
    'humidity(%)'     : 'humidity',
    'pressure(hPa)'   : 'pressure',
    'visibility(km)'  : 'visibility',
    'wind_speed(m/s)' : 'wind_speed',
    'wind_dir(deg)'   : 'wind_dir',
    'clouds(%)'       : 'clouds',
    'solar_rad(W/m2)' : 'solar_rad',
    'ghi(W/m2)'       : 'ghi',
    'dhi(W/m2)'       : 'dhi',
    'dni(W/m2)'       : 'dni',
    'precip(mm)'      : 'precip'
    }, inplace=True)
    
    # 컬럼 순서: datetime, created_at, real
    df = df[['datetime','temp','dew_point','humidity','pressure','visibility','wind_speed',
                         'wind_dir','clouds','solar_rad','ghi','dhi','dni','precip']]  

    return df



#범위 날씨 데이터 저장 함수(csv) - Api키, 위도, 경도, 시작날짜, 마지막날짜
def fetch_weatherbit_range(api_key, lat, lon, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    full_df = pd.DataFrame()

    while start_date <= end_date:
        print(f"수집 중: {start_date.strftime('%Y-%m-%d')}")
        daily_df = fetch_weatherbit_day(api_key, lat, lon, start_date)
        if not daily_df.empty:
            full_df = pd.concat([full_df, daily_df], ignore_index=True)
        start_date += timedelta(days=1)


    full_df.to_csv(f"weather_data.csv", index=False)
    print(f"weather_data.csv 다운완료")



if __name__ == "__main__":
    api_key ="" # weatherbit API입력

    fetch_weatherbit_range(api_key, 35.000594, 126.425218, "2025-05-11", "2025-05-13") 





