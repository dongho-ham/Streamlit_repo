<img width="1831" height="745" alt="image" src="https://github.com/user-attachments/assets/f9b22dd7-7866-43fa-bbf9-ab8827f48bf9" />

# Battery Anomaly Detection Dashboard

NASA PCoE 배터리 데이터셋 기반 배터리 이상 탐지 및 분석 대시보드

## 실행 방법
streamlit run main.py

## 기술 스택

- Python 3.9+
- Streamlit
- PyTorch
- Pandas, NumPy
- Scipy (LOWESS smoothing)
- Plotly/Matplotlib

## 프로젝트 구조
```
├── app.py                      # Streamlit 메인 앱
├── modules/
│   ├── data_loader.py         # 데이터 로드 모듈
│   ├── preprocessing.py       # LOWESS smoothing 전처리
│   ├── visualization.py       # 시각화 함수
│   └── anomaly_detection.py   # 이상 탐지 로직
├── dataset/                       # NASA PCoE 데이터셋
├── main.py
└── README.md
```

## 주요 기능

### 탭 구성
1. **Data Overview**: 배터리 방전 데이터 탐색
2. **Anomaly Scores**: 이상 탐지 결과
3. **Feature importance**: 변수 별 중요도 분석 결과
4. **Health Indicator**: 건강 지표 변화 추이
5. **Correlation Analysis**: 상관관계 분석 결과

### 데이터 전처리
- LOWESS (Locally Weighted Scatterplot Smoothing) 적용
- 방전 곡선 노이즈 제거
- 용량 열화 추세 추출

## 데이터셋

**NASA PCoE Battery Dataset**
- 출처: NASA Prognostics Center of Excellence
- 구성: 리튬이온 배터리 충방전 사이클 데이터
- 측정 항목: Voltage, Current, Temperature, Capacity
