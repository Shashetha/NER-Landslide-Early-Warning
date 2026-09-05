import random
import string
from datetime import datetime
from schemas.prediction import EnvironmentalFeatures, PredictionResponse


class MockPredictionService:
    def __init__(self):
        self.model_name = "landslide-model-mock"
        self.model_version = "1.0.0"
    
    def generate_prediction_id(self) -> str:
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"pred_{random_str}"
    
    def get_mock_environmental_data(self, latitude: float, longitude: float) -> EnvironmentalFeatures:
        rainfall = round(random.uniform(50, 250), 2)
        slope = round(random.uniform(10, 50), 2)
        elevation = round(random.uniform(500, 2500), 2)
        soil_moisture = round(random.uniform(30, 80), 2)
        temperature = round(random.uniform(10, 25), 2)
        
        return EnvironmentalFeatures(
            rainfall=rainfall,
            slope=slope,
            elevation=elevation,
            soil_moisture=soil_moisture,
            temperature=temperature
        )
    
    def calculate_risk_level(self, probability: float) -> str:
        if probability >= 0.85:
            return "CRITICAL"
        elif probability >= 0.7:
            return "HIGH"
        elif probability >= 0.5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_explanation(self, risk_level: str, features: EnvironmentalFeatures) -> str:
        explanations = {
            "LOW": "Current environmental conditions indicate stable terrain with minimal landslide risk. Continue regular monitoring.",
            "MEDIUM": f"Moderate risk detected. Rainfall of {features.rainfall}mm with {features.slope}° slope requires close monitoring over the next 24-48 hours.",
            "HIGH": f"High rainfall ({features.rainfall}mm) combined with steep terrain ({features.slope}°) and elevated soil moisture ({features.soil_moisture}%) is increasing landslide probability. Enhanced monitoring recommended.",
            "CRITICAL": f"CRITICAL RISK DETECTED. Multiple environmental factors indicate imminent landslide danger: heavy rainfall ({features.rainfall}mm), steep slope ({features.slope}°), and saturated soil ({features.soil_moisture}%). Immediate evacuation procedures should be considered."
        }
        return explanations.get(risk_level, "Risk assessment completed.")
    
    async def predict_landslide_risk(
        self,
        latitude: float,
        longitude: float
    ) -> PredictionResponse:
        features = self.get_mock_environmental_data(latitude, longitude)
        
        base_probability = random.uniform(0.3, 0.95)
        if features.rainfall > 150 and features.slope > 30:
            base_probability = min(base_probability + 0.15, 0.99)
        if features.soil_moisture > 70:
            base_probability = min(base_probability + 0.10, 0.99)
        
        probability = round(base_probability, 2)
        confidence = round(random.uniform(0.80, 0.95), 2)
        risk_level = self.calculate_risk_level(probability)
        explanation = self.generate_explanation(risk_level, features)
        
        return PredictionResponse(
            prediction_id=self.generate_prediction_id(),
            latitude=latitude,
            longitude=longitude,
            risk_level=risk_level,
            probability=probability,
            confidence=confidence,
            features=features,
            explanation=explanation,
            model_name=self.model_name,
            model_version=self.model_version,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )


prediction_service = MockPredictionService()
