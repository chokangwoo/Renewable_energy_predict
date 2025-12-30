"""
데이터 베이스에서 데이터를 가져와서 학습하고 예측하는 파일
"""

import pandas as pd
import numpy as np

import requests
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
'''
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
'''
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from xgboost import XGBRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression

import tensorflow as tf
import time
import random
import platform
import os

import param as pa


# DB 연결 정보
DB_CONFIG = {
    "host": pa.HOST,
    "port": pa.PORT,
    "dbname": pa.DBNAME,
    "user": pa.USER,
    "password": pa.PASSWORD
}

# DB engine
def get_engine():
    url = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    return create_engine(url)


# 날씨 데이터 불러오기
def load_weather_data(gen_name):
    table_name = "weather_data_weatherdata"

    try:
        # 1) 딕셔너리에서 발전소 이름 → plant_id 매핑
        plant = pa.PLANT_ID 
        if gen_name not in plant:
            print(f"[ERROR] '{gen_name}'은 유효한 발전소 이름이 아닙니다.")
            return None

        plant_id = plant[gen_name]

        # 2) DB에서 해당 plant_id의 데이터만 조회
        engine = get_engine()
        with engine.connect() as conn:
            query = f"""
                SELECT *
                FROM {table_name}
                WHERE plant_id = %s
                ORDER BY datetime
            """
            df = pd.read_sql_query(query, conn, params=(plant_id,))
            print(f"[DB 로드 완료] {gen_name} (plant_id={plant_id})에 해당하는 날씨 데이터 {len(df)}행 불러옴")
            return df

    except Exception as e:
        print(f"[DB ERROR] 데이터 불러오기 중 오류 발생: {e}")
        return None


# 발전량 데이터 불러오기
def load_solar_data(gen_name):
    table_name = "generation_solargeneration"

    try:
        # 1) 딕셔너리에서 발전소 이름 → plant_id 매핑
        plant = pa.PLANT_ID 
        if gen_name not in plant:
            print(f"[ERROR] '{gen_name}'은 유효한 발전소 이름이 아닙니다.")
            return None

        plant_id = plant[gen_name]

        # 2) DB에서 해당 plant_id의 데이터만 조회
        engine = get_engine()
        with engine.connect() as conn:
            query = f"""
                SELECT *
                FROM {table_name}
                WHERE plant_id = %s
                ORDER BY datetime
            """
            df = pd.read_sql_query(query, conn, params=(plant_id,))
            print(f"[DB 로드 완료] {gen_name} (plant_id={plant_id})에 해당하는 날씨 데이터 {len(df)}행 불러옴")
            return df

    except Exception as e:
        print(f"[DB ERROR] 데이터 불러오기 중 오류 발생: {e}")
        return None
    

# 예보 데이터 불러오기
def load_forecast_data(gen_name):
    table_name = "weather_data_forecastdata"

    try:
        # 1) 딕셔너리에서 발전소 이름 → plant_id 매핑
        plant = pa.PLANT_ID 
        if gen_name not in plant:
            print(f"[ERROR] '{gen_name}'은 유효한 발전소 이름이 아닙니다.")
            return None

        plant_id = plant[gen_name]

        # 2) DB에서 해당 plant_id의 데이터만 조회
        engine = get_engine()
        with engine.connect() as conn:
            query = f"""
                SELECT *
                FROM {table_name}
                WHERE plant_id = %s
                ORDER BY datetime
            """
            df = pd.read_sql_query(query, conn, params=(plant_id,))
            print(f"[DB 로드 완료] {gen_name} (plant_id={plant_id})에 해당하는 날씨 데이터 {len(df)}행 불러옴")
            return df

    except Exception as e:
        print(f"[DB ERROR] 데이터 불러오기 중 오류 발생: {e}")
        return None


# 예측 데이터 불러오기
def load_predict_data(gen_name):
    table_name = "generation_predictedgeneration"

    try:
        # 1) 딕셔너리에서 발전소 이름 → plant_id 매핑
        plant = pa.PLANT_ID 
        if gen_name not in plant:
            print(f"[ERROR] '{gen_name}'은 유효한 발전소 이름이 아닙니다.")
            return None

        plant_id = plant[gen_name]

        # 2) DB에서 해당 plant_id의 데이터만 조회
        engine = get_engine()
        with engine.connect() as conn:
            query = f"""
                SELECT *
                FROM {table_name}
                WHERE plant_id = %s
                ORDER BY datetime
            """
            df = pd.read_sql_query(query, conn, params=(plant_id,))
            print(f"[DB 로드 완료] {gen_name} (plant_id={plant_id})에 해당하는 날씨 데이터 {len(df)}행 불러옴")
            return df

    except Exception as e:
        print(f"[DB ERROR] 데이터 불러오기 중 오류 발생: {e}")
        return None


#앙상블 모델 예측 함수
def stacking_predict(GEN_DICT, GEN_CAP):
    ##########1. 데이터 로드 및 전처리##########
    설비용량_kW = GEN_CAP
    Gen = GEN_DICT

    solar    = load_solar_data(Gen)
    weather  = load_weather_data(Gen)
    forecast = load_forecast_data(Gen)

    solar["datetime"] = pd.to_datetime(solar["datetime"])
    solar.rename(columns={"kwh": "Target"}, inplace=True)
    solar["Target"] = solar["Target"].astype(float)
    solar.drop(columns=['id', 'created_at', 'plant_id'], inplace=True)
    weather["datetime"] = pd.to_datetime(weather["datetime"])
    weather.drop(columns=['id', 'created_at', 'plant_id'], inplace=True)

    # 병합 및 파생변수 생성
    merged_df = (
        pd.merge(solar, weather, on="datetime", how="inner")
        .query("Target <= @설비용량_kW")
    )
    # 다시 한번 컬럼명 확인
    merged_df.columns = [str(c) for c in merged_df.columns]

    #시계열 특성 추가
    merged_df["hour"]      = merged_df["datetime"].dt.hour
    merged_df["month"]     = merged_df["datetime"].dt.month
    merged_df["dayofyear"] = merged_df["datetime"].dt.dayofyear
    merged_df = merged_df.dropna()

    # 시간 주기성 추가
    merged_df["hour_sin"] = np.sin(2 * np.pi * merged_df["hour"] / 24)
    merged_df["hour_cos"] = np.cos(2 * np.pi * merged_df["hour"] / 24)

    # 월 주기성 추가
    merged_df["mon_sin"]  = np.sin(2 * np.pi * merged_df["month"] / 12)
    merged_df["mon_cos"]  = np.cos(2 * np.pi * merged_df["month"] / 12)

    # 연중 주기성 추가
    merged_df["doy_sin"]  = np.sin(2 * np.pi * merged_df["dayofyear"] / 365)
    merged_df["doy_cos"]  = np.cos(2 * np.pi * merged_df["dayofyear"] / 365)

    features = [c for c in merged_df.columns if c not in ["datetime", "Target"]]

    # datetime 순으로 정렬하고 인덱스 리셋
    merged_df = merged_df.sort_values("datetime").reset_index(drop=True)

    # train셋 
    train = merged_df.copy()  

    X_train = train[features].copy()
    Y_train = train["Target"].copy()

    ##########2. 베이스 모델 정의##########
    rf  = RandomForestRegressor(
        n_estimators=1000,
        criterion="squared_error",
        max_depth=50,
        min_samples_split=3 * 2,
        min_samples_leaf=3,
        n_jobs=-1,
        max_features='sqrt',  # 'sqrt' auto None 1.0
        max_samples=None,  # 1.0, 0.5, 0.5 None
        bootstrap=True,  # Must True
        random_state=random.randint(0, 1000),
        verbose=0)

    gb  = XGBRegressor(
        n_estimators=900,
        learning_rate=0.007,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.7,
        reg_alpha=0.0,
        reg_lambda=1.0,
        n_jobs=-1,
        verbosity=0,
        random_state=42
    )

    svr = SVR(
        kernel='rbf',       # 또는 'linear', 'poly'
        C=10,               # 규제 강도
        epsilon=0.1,        # ε-튜브
        gamma='scale',      # 또는 0.01, 0.1
        degree=3            # poly 커널 사용할 때만 의미
    )

    lr = LinearRegression()

    ##########3. 앙상블 모델 정의 및 학습##########
    stacking_model = StackingRegressor(
    estimators=[
        ('rf',  rf),
        ('lr', lr),
        ('gb', gb),
        ('svr', svr)
    ],
    final_estimator=Ridge(alpha=1.0),
    passthrough=False, 
    cv=5,
    n_jobs=-1
    )
    stacking_model.fit(X_train, Y_train)

    
    #########4. 예보 데이터 로드 및 전처리##########
    df_sel = forecast.copy()

    df_sel["datetime"] = pd.to_datetime(df_sel["datetime"])
    df_sel.drop(columns=['id', 'created_at', 'plant_id'], inplace=True)

    # 여기서 내일 데이터만 필터링
    KST = ZoneInfo("Asia/Seoul")
    now_kst  = datetime.now(KST)
    tomorrow = (now_kst + timedelta(days=1)).date()
    df_sel = df_sel[
        (df_sel["datetime"].dt.date >= tomorrow)
    ].copy()

    df_fcst = df_sel

    df_fcst["hour"]      = df_fcst["datetime"].dt.hour
    df_fcst["month"]     = df_fcst["datetime"].dt.month
    df_fcst["dayofyear"] = df_fcst["datetime"].dt.dayofyear

    df_fcst["hour_sin"] = np.sin(2 * np.pi * df_fcst["hour"] / 24)
    df_fcst["hour_cos"] = np.cos(2 * np.pi * df_fcst["hour"] / 24)


    df_fcst["mon_sin"] = np.sin(2 * np.pi * df_fcst["month"] / 12)
    df_fcst["mon_cos"] = np.cos(2 * np.pi * df_fcst["month"] / 12)

    df_fcst["doy_sin"]   = np.sin(2 * np.pi * df_fcst["dayofyear"] / 365)
    df_fcst["doy_cos"]   = np.cos(2 * np.pi * df_fcst["dayofyear"] / 365)

    fcst_datetime = df_fcst["datetime"].copy()
    df_fcst1  = df_fcst.drop(columns=["datetime"])


    #########5. 예측 ##########
    pred_df = stacking_model.predict(df_fcst1)

    # 결과 DataFrame
    preds_df = pd.DataFrame({
        "datetime": fcst_datetime,
        "kwh": pred_df
    })

    ########## PostgreSQL 저장##########
    try:
        engine = get_engine()

        # 데이터베이스에 기존 데이터 불러와 중복 제거
        table_name = f"{GEN_DICT}_Predict"
        with engine.connect() as conn:
            try:
                existing_db_df = pd.read_sql_table(table_name, conn)
                preds_df = pd.concat([existing_db_df, preds_df], ignore_index=True)
                preds_df = preds_df.drop_duplicates(subset='datetime')
            except Exception as e:
                print(f"[INFO] 테이블이 존재하지 않거나 새로 생성됨: {e}")

        preds_df.to_sql(table_name, engine, index=False, if_exists='replace')
        print(f"[DB 저장 완료] {table_name} 테이블")

    except Exception as e:
        print(f"[DB ERROR] PostgreSQL 저장 중 오류 발생: {e}")

    print(preds_df)
    


if __name__ == "__main__":
    stacking_predict(pa.GEN_DICT["동산 태양광"], pa.GEN_CAP['dongsan'])
    #time.sleep(1)
    #stacking_predict(pa.GEN_DICT["솔라숲1호"], pa.GEN_CAP["solar1"])


