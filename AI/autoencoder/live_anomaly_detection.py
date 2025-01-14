import torch
import time
from detect_anomalies import detect_anomaly
from autoencoder_model import Autoencoder
from further_improved_train import ImprovedAutoencoder
from diff_train import DifferenceAutoencoder
from utils import sensor_thresholds, generate_bitmask, rapid_change_threshold, interpret_bitmask, standardized_thresholds
import os
from enums import WindowAction

DATA_PREPROCESSING_TYPE = "difference"


if DATA_PREPROCESSING_TYPE == "standard":
    THRESHOLD = standardized_thresholds
    # 모델 경로 설정 및 로드
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "..", "models", "further_improved_trained_autoencoder_korea.pth")
    model = ImprovedAutoencoder()
elif DATA_PREPROCESSING_TYPE == "difference":
    THRESHOLD = sensor_thresholds
    # 모델 경로 설정 및 로드
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "..", "models", "diff_trained_autoencoder_korea.pth")
    json_path = os.path.join(current_dir, "..", "models", "sensor_diff_means_stds.json")
    model = DifferenceAutoencoder()
else:
    THRESHOLD = sensor_thresholds
    # 모델 경로 설정 및 로드
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "..", "models", "trained_autoencoder_korea.pth")
    model = Autoencoder()

# 모델 로드 및 FP16 변환
# model = ImprovedAutoencoder()
model.load_state_dict(torch.load(model_path, weights_only=True))
model.eval()
model = model.half()  # 모델을 float16으로 변환

window_open = False
hold_mask_indoor = 0b0
hold_mask_outdoor = 0b0
indoor_origin_cause = False
previous_data = {"indoor": None, "outdoor": None}
previous_time = time.time()


# 학습 데이터에서 미리 계산한 평균 및 표준편차
sensor_means = {
    "temperature": 20,
    "humidity": 50,
    "pm10": 60,
    "pm25": 35,
    "voc": 100,
    "eco2": 600,
}

sensor_stds = {
    "temperature": 5,
    "humidity": 10,
    "pm10": 20,
    "pm25": 10,
    "voc": 50,
    "eco2": 100,
}

def standardize_real_time_data(data, means, stds):
    """실시간 데이터를 학습 시 사용한 평균 및 표준편차로 표준화"""
    standardized_data = {}
    for sensor, value in data.items():
        standardized_data[sensor] = (value - means[sensor]) / stds[sensor]
    return standardized_data

def calculate_difference(current_data, previous_data):
    """직전 데이터와 현재 데이터의 차이 계산"""
    return {sensor: current_data[sensor] - previous_data[sensor] for sensor in current_data}

def determine_window_action(indoor_anomaly_mask, outdoor_anomaly_mask, current_data, indoor_raw, outdoor_raw):
    global window_open, hold_mask_indoor, hold_mask_outdoor, indoor_origin_cause, previous_data, previous_time

    influencing_sensors = []
    action = "No action"
    current_time = time.time()
    time_diff = current_time - previous_time

    if previous_data["indoor"] is None or previous_data["outdoor"] is None:
        previous_data["indoor"] = current_data["indoor"]
        previous_data["outdoor"] = current_data["outdoor"]
        previous_time = current_time
        return window_open, action, influencing_sensors

    # 비트마스크 갱신
    updated_indoor_mask = 0
    updated_outdoor_mask = 0

    # 1. 실내/실외 간 각 센서는 검출 순서에 따른 우선순위가 있음
    # 2. 0b01 상태에서 0b11 상태가 검출되면, 우선순위는 반전될 수 있음
    # 3. 0b11 상태 간 우선순위는 검출 순서에 따라 유지
    # 4. 임계치 이하로 떨어지면 해당 센서 비트는 초기화

    for i in range(6):  # 각 센서를 순회하며 비트 업데이트
        indoor_bit = (indoor_anomaly_mask >> (i * 2)) & 0b11
        outdoor_bit = (outdoor_anomaly_mask >> (i * 2)) & 0b11
        hold_indoor_bit = (hold_mask_indoor >> (i * 2)) & 0b11
        hold_outdoor_bit = (hold_mask_outdoor >> (i * 2)) & 0b11

        # 임계치 이하로 떨어지면 상태 해제
        if indoor_bit == 0 and hold_indoor_bit > 0:
            hold_mask_indoor &= ~(0b11 << (i * 2))
        if outdoor_bit == 0 and hold_outdoor_bit > 0:
            hold_mask_outdoor &= ~(0b11 << (i * 2))

        # 상태 갱신 로직 (0b11 우선순위 및 검출 순서 반영)
        if indoor_bit == 0b11 and outdoor_bit != 0b11:
            updated_indoor_mask |= (indoor_bit << (i * 2))
            hold_mask_indoor |= (indoor_bit << (i * 2))
        elif outdoor_bit == 0b11 and indoor_bit != 0b11:
            updated_outdoor_mask |= (outdoor_bit << (i * 2))
            hold_mask_outdoor |= (outdoor_bit << (i * 2))
        elif indoor_bit == 0b01 and outdoor_bit == 0b01:
            # 같은 센서의 0b01 상태 발생 시, 초기 검출 우선
            if hold_mask_indoor & (0b11 << (i * 2)) == 0:
                updated_indoor_mask |= (indoor_bit << (i * 2))
                hold_mask_indoor |= (indoor_bit << (i * 2))
            else:
                updated_outdoor_mask |= (outdoor_bit << (i * 2))
                hold_mask_outdoor |= (outdoor_bit << (i * 2))
        elif indoor_bit == 0b01 and hold_outdoor_bit == 0:
            updated_indoor_mask |= (indoor_bit << (i * 2))
            hold_mask_indoor |= (indoor_bit << (i * 2))
        elif outdoor_bit == 0b01 and hold_indoor_bit == 0:
            updated_outdoor_mask |= (outdoor_bit << (i * 2))
            hold_mask_outdoor |= (outdoor_bit << (i * 2))

    # 0b11 상태 개수를 통해 창문 개폐 결정
    indoor_11_count = sum(((updated_indoor_mask >> (i * 2)) & 0b11) == 0b11 for i in range(6))
    outdoor_11_count = sum(((updated_outdoor_mask >> (i * 2)) & 0b11) == 0b11 for i in range(6))

    if indoor_11_count >= outdoor_11_count and (indoor_11_count+outdoor_11_count != 0):
        if not window_open:
            window_open = True
            action = "창문 열림 (실내 `0b11` 상태 우세)"
            influencing_sensors.append("실내 공기질 이상 상태 (0b11 다수)")

    elif outdoor_11_count > indoor_11_count:
        if window_open:
            window_open = False
            action = "창문 닫음 (실외 `0b11` 상태 우세)"
            influencing_sensors.append("실외 공기질 이상 상태 (0b11 다수)")

    # 최종 비트마스크 갱신
    previous_data["indoor"] = current_data["indoor"]
    previous_data["outdoor"] = current_data["outdoor"]
    previous_time = current_time

    # # 온도에따라 문열기
    # if hold_mask_outdoor == 0 and hold_mask_indoor == 0 and indoor_raw["temperature"] > 26:
    #     print("[ACCIDENT] SO HOT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     print(f"CURR_TEMP: {indoor_raw['temperature']}")
    #     window_open = True
    # elif hold_mask_outdoor == 0 and hold_mask_indoor == 0:
    #     print("[ACCIDENT] CONDITION IS GOOD!!!!!")
    #     window_open = False
    if hold_mask_outdoor == 0 and hold_mask_indoor == 0:
        print("CONDITION IS GOOD")
        window_open = False
    # print(f"[DEBUG] Window action: {action}, Influencing sensors: {influencing_sensors}")
    return window_open, action, influencing_sensors

import json
def load_means_and_stds(file_path="sensor_means_stds.json"):
    """저장된 평균 및 표준편차를 불러오기"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data["means"], data["stds"]


def check_and_actuate_window(indoor_data, outdoor_data, previous_data=None):
    # 각 센서 값 출력
    print("\n[현재 센서 수치]")
    print("실내 센서 수치:")

    if DATA_PREPROCESSING_TYPE == "standard":
        for sensor, value in indoor_data.items():
            print(f"  {sensor}: {value:.2f}")
        print("실외 센서 수치:")
        for sensor, value in outdoor_data.items():
            print(f"  {sensor}: {value:.2f}")
        indoor_data = standardize_real_time_data(indoor_data, sensor_means, sensor_stds)
        outdoor_data = standardize_real_time_data(outdoor_data, sensor_means, sensor_stds)
    elif DATA_PREPROCESSING_TYPE == "difference":
        for (sensor, value), (s2, v2) in zip(indoor_data.items(), previous_data["indoor"].items()):
            print(f"  {sensor}: {value:.2f}  {v2:.2f}")
        print("실외 센서 수치:")
        for (sensor, value), (s2, v2) in zip(outdoor_data.items(), previous_data["outdoor"].items()):
            print(f"  {sensor}: {value:.2f}  {v2:.2f}")
            # 추론 시 사용 예시
        means, stds = load_means_and_stds(json_path)
        
        indoor_raw = indoor_data
        outdoor_raw = outdoor_data
        indoor_data = standardize_real_time_data(indoor_data, means, stds)
        outdoor_data = standardize_real_time_data(outdoor_data, means, stds)
        indoor_data = calculate_difference(indoor_data, previous_data["indoor"])
        outdoor_data = calculate_difference(outdoor_data, previous_data["outdoor"])

    # 입력 데이터도 float16으로 변환
    indoor_data_fp16 = {k: torch.tensor(v, dtype=torch.float16) for k, v in indoor_data.items()}
    outdoor_data_fp16 = {k: torch.tensor(v, dtype=torch.float16) for k, v in outdoor_data.items()}

    indoor_anomalies = detect_anomaly(indoor_data_fp16, model, THRESHOLD)
    outdoor_anomalies = detect_anomaly(outdoor_data_fp16, model, THRESHOLD)

    if DATA_PREPROCESSING_TYPE == "difference":
        indoor_anomaly_mask = generate_bitmask(indoor_raw, indoor_anomalies, THRESHOLD, "in")
        outdoor_anomaly_mask = generate_bitmask(outdoor_raw, outdoor_anomalies, THRESHOLD, "out")
    else:
        indoor_anomaly_mask = generate_bitmask(indoor_data, indoor_anomalies, THRESHOLD, "in")
        outdoor_anomaly_mask = generate_bitmask(outdoor_data, outdoor_anomalies, THRESHOLD, "out")
    # print(f"{indoor_anomalies}    {outdoor_anomalies}")
    # print(f"{indoor_anomaly_mask}    {outdoor_anomaly_mask}")

    window_status, action, influencing_sensors = determine_window_action(indoor_anomaly_mask, outdoor_anomaly_mask, {"indoor": indoor_data, "outdoor": outdoor_data}, indoor_raw, outdoor_raw)
    print("\n창문 상태:", window_status)
    print("영향을 미친 센서들:", influencing_sensors)
    print(f"실내 비트마스크: {bin(indoor_anomaly_mask)}, 실외 비트마스크: {bin(outdoor_anomaly_mask)}")

    issues = interpret_bitmask(indoor_anomaly_mask, outdoor_anomaly_mask)
    print("Detected issues:", issues)

    window_status = WindowAction.OPEN if window_status else WindowAction.CLOSE

    return window_status, issues
