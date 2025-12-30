#Weather bit information
API_KEY ="754cfb3ea2024857a046436a75d0cc8f"

#google chrome exe download information
#https://googlechromelabs.github.io/chrome-for-testing/


#기상청 information
USER_ID = 'ckw0529@naver.com'
USER_PSD = 'kangwoo1081@'


# PostgreSQL information

HOST = '103.218.163.71'      
PORT = '10001'
DBNAME = 'postgres'
USER = 'admin'
PASSWORD = 'admin'


#Gen list information
GEN_DICT = {"동산 태양광":"dongsan", "솔라숲1호":"solar1"}

GEN = {"dongsan":"동산 태양광", "solar1":"솔라숲1호"}

GEN_CAP = {"dongsan":450, "solar1":500} #kW단위

PLANT_ID = {'dongsan': 1, "solar1": 2}




#동산태양광
DONG_LAT=35.000594 #위도
DONG_LON=126.425218  #경도

#솔라숲1호
SOLAR1_LAT = 35.012121 #위도
SOLAR1_LON = 126.496680 #경도

#다운로드 폴더 경로 지정
Temp = {
    'LDAPS': "/Users/kangwoo/Desktop/down"
}


#BackUp Path information
GEN_PATH = "/Users/kangwoo/Desktop/gen_data"

FORECAST_PATH = "/Users/kangwoo/Desktop/forecast_data"

WEATHER_PATH = "/Users/kangwoo/Desktop/weather_data"

RESULT_PATH = '/Users/kangwoo/Desktop/result_data'

DOWN_PATH = "/Users/kangwoo/Desktop/LDAPS"

CHROME_DRIVER_PATH = "/Users/kangwoo/Desktop/driver/chromedriver"

LDAPS_PATH = "/Users/kangwoo/Desktop/LDAPS"

PREDICT_PARH = "/Users/kangwoo/Desktop/predict"


#기상데이터 URL
URL = {
    'ASOS': 'https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36',
    'AWS': 'https://data.kma.go.kr/data/grnd/selectAwsRltmList.do?pgmNo=56',
    'LDAPS': 'https://data.kma.go.kr/data/rmt/rmtList.do?code=340&pgmNo=65',
    'GDPS': 'https://data.kma.go.kr/data/rmt/rmtList.do?code=312&pgmNo=64'
}

LDPSColumn = ['target', 'issue', 
               'lat', 'lng',
               'temp(C)','dew_point(C)',
               'humidity(%)', 'pressure(hPa)',
               'visibility(km)', 'u_component_of_wind',
               'v_component_of_wind', 'clouds(%)',
               'ghi(W/m2)','precip(mm)',
               '1_5temp(C)', 'specific_humidity',
               'maxgust', 'low_cloud_cover',
               'medium_cloud_cover', 'high_cloud_cover',
            ]

LDPSColumn_update = ['target', 'issue', 
               'lat', 'lng',
               'temp(C)','dew_point(C)',
               'humidity(%)', 'pressure(hPa)',
               'visibility(km)', 
               'wind_speed(m/s)', 'wind_dir(deg)',  
               'clouds(%)',
               'ghi(W/m2)','precip(mm)',
               ]


