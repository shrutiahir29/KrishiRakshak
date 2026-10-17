"""
SQLAlchemy ORM Database Models for KrishiRakshak
Covers users, farms, fields, weather, soil moisture, pest forecasts,
irrigation advisories, crop recommendations, and treatment guidance.
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Boolean
)
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(50), default="farmer") # farmer, agronomist, admin
    created_at = Column(DateTime, default=datetime.utcnow)

    farms = relationship("Farm", back_populates="owner")

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(150), nullable=False)
    location = Column(String(150), default="Flanders Research Station")
    total_area_hectares = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="farms")
    fields = relationship("Field", back_populates="farm")

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    field_code = Column(String(50), unique=True, index=True, default="FIELD-A1")
    crop = Column(String(100), default="prei") # vegetable / field crop
    soil_type = Column(String(50), default="Sdm") # loam / sandy loam / clay
    irrigation_method = Column(String(50), default="druppel") # druppel (drip) / haspel (sprinkler)
    sensor_id = Column(String(50), default="2F71D1") # TEROS 10 sensor module identifier
    area_hectares = Column(Float, default=1.5)
    planting_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="fields")
    soil_records = relationship("SoilMoistureRecord", back_populates="field")
    pest_predictions = relationship("PestPrediction", back_populates="field")
    irrigation_advisories = relationship("IrrigationAdvisory", back_populates="field")

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    location = Column(String(100), default="Kruisem")
    temperature = Column(Float, nullable=False) # °C
    humidity = Column(Float, nullable=False) # %
    rainfall = Column(Float, default=0.0) # mm
    wind_speed = Column(Float, default=3.5) # m/s
    weather_condition = Column(String(100), default="Partly Cloudy")
    data_source = Column(String(50), default="dataset") # 'dataset' or 'live_api'

class SoilMoistureRecord(Base):
    __tablename__ = "soil_moisture_records"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=True)
    sensor_id = Column(String(50), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    vwc_depth_15cm = Column(Float, nullable=False) # m3/m3 or %
    temperature = Column(Float, nullable=True) # °C
    pluvio = Column(Float, default=0.0) # mm
    data_source = Column(String(50), default="dataset") # 'dataset' or 'live_sensor'

    field = relationship("Field", back_populates="soil_records")

class PestPrediction(Base):
    __tablename__ = "pest_predictions"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    crop = Column(String(100), nullable=False)
    predicted_risk = Column(String(50), nullable=False) # LOW, MEDIUM, HIGH
    probability = Column(Float, nullable=False) # 0.0 - 1.0
    forecast_days = Column(String(20), default="3-5 days")
    input_features = Column(JSON, nullable=False) # {temperature, humidity, rainfall, etc.}
    shap_explanations = Column(JSON, nullable=False) # list of feature contributions
    model_version = Column(String(50), default="XGBoost-1.0")

    field = relationship("Field", back_populates="pest_predictions")

class IrrigationAdvisory(Base):
    __tablename__ = "irrigation_advisories"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    crop = Column(String(100), nullable=False)
    soil_moisture_vwc = Column(Float, nullable=False) # current reading
    field_capacity = Column(Float, default=0.28)
    wilting_point = Column(Float, default=0.08)
    eto = Column(Float, nullable=True) # mm/day
    etc = Column(Float, nullable=True) # mm/day
    forecast_rain_48h = Column(Float, default=0.0) # mm
    decision = Column(String(50), nullable=False) # IRRIGATE or WAIT
    intensity = Column(String(50), default="NONE") # NONE, LOW, MODERATE, HIGH
    water_amount_mm = Column(Float, default=0.0)
    reasoning = Column(Text, nullable=False)
    data_source = Column(String(50), default="dataset")

    field = relationship("Field", back_populates="irrigation_advisories")

class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    n_input = Column(Float, nullable=False)
    p_input = Column(Float, nullable=False)
    k_input = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    ph = Column(Float, nullable=False)
    rainfall = Column(Float, nullable=False)
    recommendations = Column(JSON, nullable=False) # list of {crop, score, reasons}

class TreatmentGuidance(Base):
    __tablename__ = "treatment_guidance"

    id = Column(Integer, primary_key=True, index=True)
    crop = Column(String(100), nullable=False, index=True)
    condition = Column(String(150), nullable=False, index=True)
    category = Column(String(50), default="pest") # pest, nutritional, weather_stress
    treatment = Column(Text, nullable=False)
    preventive_measure = Column(Text, nullable=False)
    precautions = Column(Text, nullable=False)
    timing = Column(String(100), default="Immediate upon early threshold")
