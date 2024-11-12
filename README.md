이모지를 추가하여 `README.md`를 더 보기 쉽게 만들었습니다.

---

## 🌬️ 라즈베리파이용 실시간 센서 기반 창문 자동 제어 시스템

### 📝 개요

이 프로젝트는 라즈베리파이 4에서 실행되는 실시간 환경 모니터링 및 창문 자동 제어 시스템입니다. 온도, 습도, PM10, PM2.5, VOC, eCO₂ 등의 실내외 센서 데이터를 수집하여 공기질을 모니터링하고, 실내 공기질이 좋지 않을 경우 창문을 자동으로 열고 외부 오염이 심할 때 창문을 닫는 등의 제어를 수행합니다. 경량화된 PyTorch 모델과 반정밀도(FP16)를 사용하여 라즈베리파이에서 추론 성능을 최적화합니다.

---

### 🔑 주요 기능

- **🌡️ 실시간 센서 데이터 수집 및 시뮬레이션**: 한국 환경에 맞춘 데이터 시뮬레이터를 통해 실내외 온도, 습도, 미세먼지 등 데이터를 생성합니다.
- **🧠 Autoencoder 기반 이상 탐지**: PyTorch로 학습된 Autoencoder 모델을 통해 공기질 데이터의 이상치를 실시간으로 감지합니다.
- **🚪 급격한 변화 감지 및 창문 제어**: 실내외 급격한 오염 변화를 감지하고, 비트마스킹을 통해 창문 상태를 자동으로 제어합니다.
- **⚙️ 반정밀도(FP16) 최적화**: 라즈베리파이의 메모리와 연산 성능을 고려해 추론 시 모델과 입력 데이터를 FP16으로 변환하여 최적화합니다.

---

### 📥 설치 및 실행 방법

#### 1. 🛠️ 라즈베리파이 환경 설정

라즈베리파이에서 Python과 pip가 설치되어 있는지 확인합니다.

```bash
sudo apt update
sudo apt install python3-pip libatlas-base-dev
```

#### 2. 🐍 프로젝트 클론 및 Conda 환경 설정

```bash
git clone https://github.com/your-repo/raspberry-pi-window-control.git
cd raspberry-pi-window-control
```

#### 3. 🔥 PyTorch 설치

라즈베리파이에서 PyTorch를 설치하려면 ARM 아키텍처에 맞는 휠 파일을 사용해야 합니다. 아래는 PyTorch 1.9.0 설치 예시입니다. (필요에 따라 최신 버전을 선택할 수 있습니다)

```bash
pip3 install torch-1.9.0-cp37-cp37m-linux_armv7l.whl
```

#### 4. 📦 프로젝트 종속성 설치

프로젝트에 필요한 패키지를 설치합니다.

```bash
pip3 install -r requirements.txt
```

#### 5. 🏋️ Autoencoder 모델 학습

라즈베리파이의 성능 제한으로 학습은 다른 고성능 컴퓨터에서 수행한 후, 학습된 모델(`trained_autoencoder_korea.pth`)을 라즈베리파이로 전송합니다. 학습은 다음 명령으로 수행할 수 있습니다.

```bash
python3 train_autoencoder.py
```

#### 6. 🏠 실시간 창문 제어 시스템 실행

라즈베리파이에서 `main.py`를 실행하여 실시간 센서 데이터 감지 및 창문 제어 시스템을 시작합니다.

```bash
python3 main.py
```

---

### 🚀 사용법

1. **🧑‍🏫 모델 학습 및 추론 준비**: 학습된 `trained_autoencoder_korea.pth` 모델 파일을 라즈베리파이에 준비해 둡니다.
2. **🎛️ 시스템 실행**: `main.py`를 실행하면 라즈베리파이에서 실시간으로 센서 데이터를 모니터링하고, 공기질 상태에 따라 창문을 제어합니다.
3. **⚙️ 설정 변경**: `utils.py` 파일에서 센서 임계값 및 급격한 변화 임계값을 설정할 수 있습니다.

---

### 📂 파일 구조

- `autoencoder_model.py`: Autoencoder 모델 정의
- `train_autoencoder.py`: 학습 코드. 데이터 시뮬레이터를 사용하여 모델 학습을 수행합니다.
- `data_simulator.py`: 한국 환경에 맞춘 센서 데이터 시뮬레이터. 온도, 습도, 미세먼지 등 데이터를 생성합니다.
- `detect_anomalies.py`: 이상 탐지 함수. Autoencoder 모델로 이상치를 감지합니다.
- `live_anomaly_detection.py`: 실시간 센서 데이터 처리 및 창문 제어 함수.
- `utils.py`: 센서 임계값, 비트마스크 생성 및 급격한 변화 임계값 설정.
- `main.py`: 메인 실행 파일. 전체 기능을 통합하여 실행합니다.

---

### ⚙️ 주요 기술

- **💻 PyTorch 및 FP16 최적화**: PyTorch의 Autoencoder 모델을 사용하여 라즈베리파이에서 경량화된 추론을 수행하며, FP16 반정밀도 연산을 통해 메모리 사용량을 최적화했습니다.
- **🔢 비트마스킹 기반 창문 상태 유지**: 각 센서의 이상 상태를 비트마스크로 관리하여, 급격한 오염 변화를 실시간으로 감지하고 창문을 제어합니다.

---

### 🔔 참고 사항

- **라즈베리파이의 성능 제한**: 라즈베리파이는 CPU만 사용하기 때문에, 대규모 모델 학습은 고성능 PC나 클라우드 환경에서 수행하고, 라즈베리파이에서는 추론에만 사용해야 합니다.
- **데이터 최적화 필요**: 추론 성능을 높이기 위해 필요한 데이터 포맷이나 모델 최적화 방식을 고려해 사용할 수 있습니다.
  
---

### 📜 라이선스

MIT License