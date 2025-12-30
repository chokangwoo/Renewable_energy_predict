#Weather bit information
API_KEY ="api-key"

#google chrome exe download information
#https://googlechromelabs.github.io/chrome-for-testing/


#기상청 information
USER_ID = 'your-id'
USER_PSD = 'your-password'


# PostgreSQL information

HOST = 'ip-address'      
PORT = 'port-number'
DBNAME = 'dbname'
USER = 'user'
PASSWORD = 'passward'


#Gen list information
GEN_DICT = {"동산 태양광":"dongsan", "솔라숲1호":"solar1"}

GEN = {"dongsan":"동산 태양광", "solar1":"솔라숲1호"}

GEN_CAP = {"dongsan":450, "solar1":500} #kW단위

PLANT_ID = {'dongsan': 1, "solar1": 2}




#동산태양광
DONG_LAT= #위도
DONG_LON= #경도

#솔라숲1호
SOLAR1_LAT = #위도
SOLAR1_LON = #경도

#다운로드 폴더 경로 지정
Temp = {
    'LDAPS': ""
}


#BackUp Path information
GEN_PATH = ""

FORECAST_PATH = ""

WEATHER_PATH = ""

RESULT_PATH = ""

DOWN_PATH = ""

CHROME_DRIVER_PATH = ""

LDAPS_PATH = ""

PREDICT_PARH = ""


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



