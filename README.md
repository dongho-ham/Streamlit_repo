<img width="1831" height="745" alt="image" src="https://github.com/user-attachments/assets/f9b22dd7-7866-43fa-bbf9-ab8827f48bf9" />

# Battery Anomaly Detection Dashboard

NASA PCoE 배터리 데이터셋 기반 배터리 이상 탐지 및 분석 대시보드

## 실행 방법
streamlit run main.py

## 기술 스택

- Python 3.13+
- Streamlit
- Pandas, NumPy
- Scipy (LOWESS smoothing)
- Plotly/Matplotlib

## 프로젝트 구조
```
├── utils
│   ├── __init__.py
│   ├── dataloader.py # S3 데이터 호출                 
├── tabs/
│   ├── tab1.py       # Data Overview
│   ├── tab2.py       # Anomaly Scores
│   ├── tab3.py       # Feature importance
│   ├── tab4.py       # Health Indicato
|   ├── tab5.py       # Correlation Analysis
├── requirements.txt                      
├── main.py           # Streamlit 메인 앱
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
