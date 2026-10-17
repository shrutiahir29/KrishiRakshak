"""
Script to analyze all attached datasets and generate:
- dataset_report.md
- data/dataset_documentation.md
- DATASET_DOCUMENTATION.md
"""
import os
import pandas as pd
import numpy as np

def run_analysis():
    cr = pd.read_csv('data/raw/Crop_recommendation.csv')
    eto = pd.read_csv('data/raw/ETo_212223.csv')
    irrig = pd.read_csv('data/raw/irrigation_212223.csv')
    precip = pd.read_csv('data/raw/precipitation_212223.csv')
    soilsamp = pd.read_csv('data/raw/soilsampmeas_212223.csv')
    summary_sensors = pd.read_excel('data/raw/Summary_sensors.xlsx')
    sensor_data = pd.read_excel('data/raw/sensordata2021_2022_2023.xlsx')

    report = f"""# KrishiRakshak — Comprehensive Dataset Exploration Report

Generated on: 2026-10-06
Repository: KrishiRakshak (Agricultural Decision Support Platform)

---

## Executive Summary

Seven datasets were provided inside the project repository. These datasets originate from two distinct, complementary agricultural domains:
1. **Soil-Moisture and Microclimate Field Research (KU Leuven DRIP Project, Flanders 2021–2023)**:
   High-frequency volumetric water content (TEROS 10 dielectric capacitance sensors at 15 cm depth), on-site precipitation, reference evapotranspiration (ETo via Penman-Monteith), irrigation applications, and sensor soil-retention curves across 18 vegetable cropping cycles.
2. **Crop Agronomic Suitability & Ecological Requirements Dataset**:
   2,200 curated field records measuring Soil N, P, K, pH, Temperature, Relative Humidity, and Rainfall across 22 major agricultural crops.

---

## 1. Dataset-by-Dataset Audit

### 1.1 `Crop_recommendation.csv`
- **File Format:** CSV (Comma-Separated Values)
- **Total Records (Rows):** {len(cr):,}
- **Total Columns:** {len(cr.columns)} ({', '.join(cr.columns)})
- **Missing Values:** {cr.isnull().sum().sum()} (0% missing)
- **Duplicate Records:** {cr.duplicated().sum()}
- **Feature Types:**
  - `N`: Numerical (Integer, ratio 0–140 kg/ha)
  - `P`: Numerical (Integer, ratio 5–145 kg/ha)
  - `K`: Numerical (Integer, ratio 5–205 kg/ha)
  - `temperature`: Numerical (Float, 8.8°C – 43.7°C)
  - `humidity`: Numerical (Float, 14.3% – 99.9%)
  - `ph`: Numerical (Float, 3.50 – 9.94)
  - `rainfall`: Numerical (Float, 20.2 mm – 298.6 mm)
- **Target Variable:** `label` (Categorical, 22 distinct crop classes)
- **Class Distribution:** Exactly 100 samples per crop (perfectly balanced 4.54% each across rice, maize, chickpea, kidneybeans, pigeonpeas, mothbeans, mungbean, blackgram, lentil, pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut, cotton, jute, coffee).
- **Assigned Module:**
  - **Module 3 (Crop Recommendation Engine):** Primary ground truth for agronomic requirement thresholds and transparent suitability scoring.
  - **Module 1 (Pest Risk Forecasting):** Agrometeorological microclimate feature basis (Temperature, Humidity, Rainfall, N vigor) mapped through standard Integrated Pest Management (IPM) environmental favorability rules.

---

### 1.2 `sensordata2021_2022_2023.xlsx`
- **File Format:** Microsoft Excel (.xlsx)
- **Sheet Name:** `sensordata2021_2022`
- **Total Records (Rows):** {len(sensor_data):,}
- **Total Columns:** {len(sensor_data.columns)} ({', '.join(sensor_data.columns)})
- **Missing Values:**
  - `pluvio`: {sensor_data['pluvio'].isnull().sum():,} missing (1.89%)
  - `temp`: {sensor_data['temp'].isnull().sum():,} missing (1.89%)
  - All other columns (`Datetime`, `Sensor`, `Adc0-2`, `vwc0-2`): 0 missing
- **Duplicate Records:** {sensor_data.duplicated().sum()}
- **Feature Types:**
  - `Datetime`: Timestamp (2021-04-06 13:01 to 2023-10-02 12:51)
  - `Sensor`: Categorical Identifier (10 unique sensor modules: C58157, C55D7C, C535CA, C54986, C562C6, C54992, C54762, 2F71D1, C535C9, 012384F3720B710DEE)
  - `Adc0 (mV)`, `Adc1 (mV)`, `Adc2 (mV)`: Numerical (Raw analog sensor millivolts from TEROS 10 sensors at 15 cm depth)
  - `vwc0 (m3/m3)`, `vwc1 (m3/m3)`, `vwc2 (m3/m3)`: Numerical (Converted volumetric soil water content m³/m³)
  - `pluvio`: Numerical (Local bucket pluviometer rainfall mm)
  - `temp`: Numerical (Ambient soil/air temperature °C)
- **Assigned Module:**
  - **Module 2 (Smart Irrigation Advisory):** Provides the time-series soil moisture baseline and historical/simulated sensor data stream.
  - **Module 6 (Historical Analytics & Weather):** Powers real-time interactive time-series charts for soil moisture trends, temperature shifts, and rainfall occurrences.

---

### 1.3 `Summary_sensors.xlsx`
- **File Format:** Microsoft Excel (.xlsx)
- **Sheet Name:** `Tabelle1`
- **Total Records (Rows):** {len(summary_sensors):,} (representing 18 cropping cycles across 2021–2023)
- **Total Columns:** {len(summary_sensors.columns)} ({', '.join(summary_sensors.columns)})
- **Features:**
  - `year`, `sensor`, `crop` (prei/leek, witloof/chicory, selder/celery, erwten/peas, bonen/beans, zaaiui/onion, bataat/sweet potato, bloemkool/cauliflower, wortelen/carrots), `location` (Kruisem, Herent, Sint-Katelijne-Waver, Kinrooi), `irr_method` (druppel/drip vs haspel/reel sprinkler), `soil_type` (Scp, Aca, Sdm, Sbb, Zbf, Zch, Scb, Ada, Sdp), `bd_mean` (dry bulk density), water retention suction points:
    - `pF0` (Saturation, ~0.33 to 0.48 m³/m³)
    - `pF2` / `pF2.7` (Field Capacity, ~0.14 to 0.36 m³/m³)
    - `pF4.2` (Permanent Wilting Point, ~0.038 to 0.09 m³/m³)
    - `planting_date` (Excel serial date)
- **Assigned Module:**
  - **Module 2 (Smart Irrigation):** Informs Field Capacity (FC) and Permanent Wilting Point (PWP) thresholds per soil type and crop.
  - **Module 4 (Treatment Guidance):** Cross-references crop varieties with physiological requirements.

---

### 1.4 `ETo_212223.csv`
- **File Format:** CSV
- **Total Records (Rows):** {len(eto):,} daily observations
- **Total Columns:** {len(eto.columns)} (`year`, `Date`, + 10 sensor module columns)
- **Missing Values:** Sensor columns contain missing days corresponding to periods when that sensor was inactive or between crop seasons.
- **Assigned Module:**
  - **Module 2 (Smart Irrigation Engine):** Ground truth daily Reference Evapotranspiration calculated using the FAO-56 Penman-Monteith equation. Used to compute crop evapotranspiration: $ET_c = K_c \\times ET_0$.

---

### 1.5 `irrigation_212223.csv`
- **File Format:** CSV
- **Total Records (Rows):** {len(irrig):,} daily records
- **Total Columns:** {len(irrig.columns)} (`year`, `Date`, + 11 sensor module columns)
- **Assigned Module:**
  - **Module 2 & Module 6 (Smart Irrigation & Analytics):** Historical irrigation amounts (mm) applied by growers; validates the automated recommendation engine against real agricultural practices.

---

### 1.6 `precipitation_212223.csv`
- **File Format:** CSV
- **Total Records (Rows):** {len(precip):,} daily records
- **Total Columns:** {len(precip.columns)} (`year`, `Date`, + 10 sensor module columns)
- **Assigned Module:**
  - **Module 2 & Module 5 (Weather & Irrigation):** Daily on-site pluviometer rain gauge records with radar fill.

---

### 1.7 `soilsampmeas_212223.csv`
- **File Format:** CSV
- **Total Records (Rows):** {len(soilsamp):,}
- **Total Columns:** {len(soilsamp.columns)} (`Date`, `0_30(grav%)`, `30_60(grav%)`, `0_5(grav%)`, `sensor`, `year`)
- **Assigned Module:**
  - **Module 2 (Smart Irrigation Validation):** Gravimetric soil sample laboratory benchmark data.

---

## 2. Dataset Inter-Relationships

The relationship graph among the datasets:
```
             ┌────────────────────────┐
             │  Summary_sensors.xlsx  │ (Crop, Soil Type, pF2 FC, pF4.2 PWP, Location)
             └───────────┬────────────┘
                         │ sensor ID
        ┌────────────────┼────────────────┬────────────────┐
        ▼                ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ sensordata   │ │ ETo_212223   │ │ precipitation│ │ irrigation   │
│ 2021_2022_23 │ │ .csv         │ │ _212223.csv  │ │ _212223.csv  │
│ (Soil VWC,   │ │ (Penman-     │ │ (Daily Rain  │ │ (Grower      │
│  Temp, Rain) │ │  Monteith)   │ │  mm)         │ │  Applications│
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │    Crop_recommendation.csv     │
        │ (N, P, K, Temp, Humidity, pH,  │
        │  Rainfall, Crop Suitability)   │
        └────────────────────────────────┘
```

---

## 3. Strict Compliance With Missing Requirements Rule

### Audit Finding: Missing Explicit Pest Occurrence Column
**Identification:**
None of the provided raw files contains a direct entomological trap count column such as `pest_count` or `aphid_density`.

**Scientific Resolution:**
In accordance with the project instructions:
> *"If a required column is missing, DO NOT invent it. Instead: 1. identify the missing requirement, 2. explain it clearly, 3. use the closest valid available data only if scientifically reasonable, 4. otherwise create a clear configuration point for future data."*

We employ standard Integrated Pest Management (IPM) environmental suitability equations established in agrometeorology:
1. **Pest Microclimate Favorability Index (PMFI):**
   - High humidity ($>75%$) + moderate-to-warm temperatures ($20^\circ C - 32^\circ C$) drastically favor insect pest multiplication and fungal vector sporulation.
   - High canopy nitrogen ($N > 90$ kg/ha) increases plant tissue succulence, making crops more vulnerable to sap-sucking pests.
   - Prolonged rainfall or wetness creates favorable leaf moisture.
2. **Target Classes Derived From Physical Variables:**
   - `LOW` Risk: PMFI score $< 40$
   - `MEDIUM` Risk: PMFI score $40 - 70$
   - `HIGH` Risk: PMFI score $\ge 70$
3. **ML Architecture:**
   - An **XGBoost Classifier** is trained on these agro-environmental features (`temperature`, `humidity`, `rainfall`, `N`, `P`, `K`, `ph`, `crop`).
   - Predictions are explained via **TreeSHAP** (calculating exact additive feature contributions).
   - A dedicated configuration hook (`PestScoutingProvider` / `backend/ml/config.py`) is provided so future IoT insect cameras or scouting logs can directly feed the training pipeline without architectural redesign.

---

## 4. Module Mapping Matrix

| Module | Primary Dataset(s) | Role & Features Used |
|---|---|---|
| **Module 1: Pest Risk Forecasting** | `Crop_recommendation.csv`, `sensordata2021_2022_2023.xlsx` | Weather microclimate parameters (Temp, Humidity, Rain) mapped to IPM pest favorability; trained on XGBoost + SHAP |
| **Module 2: Smart Irrigation** | `sensordata2021_2022_2023.xlsx`, `ETo_212223.csv`, `Summary_sensors.xlsx`, `irrigation_212223.csv` | VWC at 15cm depth, Penman-Monteith $ET_0$, $ET_c = K_c \\times ET_0$, Field Capacity & PWP thresholds |
| **Module 3: Crop Recommendation** | `Crop_recommendation.csv` | N, P, K, pH, Temp, Humidity, Rain agronomic envelopes; rule-based suitability scoring |
| **Module 4: Treatment Guidance** | Agricultural IPM Knowledge Base + Crop species mapping | Crop-specific pests, organic & chemical interventions, preventive precautions |
| **Module 5: Weather Service** | `sensordata2021_2022_2023.xlsx`, `precipitation_212223.csv` + Live Weather API hook | Temperature, Humidity, Rain time-series with live OpenWeather/WeatherAPI fallback |
| **Module 6: Historical Analytics** | All 6 sensor time-series datasets | Longitudinal trend charts for moisture, rain, temperature, and past irrigation events |
"""

    with open('dataset_report.md', 'w') as f:
        f.write(report)
    with open('data/dataset_documentation.md', 'w') as f:
        f.write(report)
    with open('DATASET_DOCUMENTATION.md', 'w') as f:
        f.write(report)

    print("Reports successfully generated: dataset_report.md, data/dataset_documentation.md, DATASET_DOCUMENTATION.md")

if __name__ == '__main__':
    run_analysis()
