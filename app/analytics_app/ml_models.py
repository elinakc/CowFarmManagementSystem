from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from django.db.models import Avg
import pandas as pd
import numpy as np
import joblib

from app.animal_records.models import AnimalRecords
from app.milk_records.models import MilkRecord

class MilkYieldPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.label_encoders = {
            'breed': LabelEncoder(),
            'lactation_cycle': LabelEncoder()
        }
    
    def prepare_training_data(self):
        """Prepare training data from existing records"""
        # Get all records
        animals = AnimalRecords.objects.all().prefetch_related('milk_records')
        
        training_data = []
        for animal in animals:
            # Normalize breed and lactation cycle
            breed = str(animal.breed).lower().strip()
            lactation_cycle = str(animal.lactation_cycle).lower().strip()
            
            # Calculate average daily milk yield
            milk_yield = animal.milk_records.aggregate(
                avg_yield=Avg('morning_milk_quantity') + 
                         Avg('afternoon_milk_quantity') + 
                         Avg('evening_milk_quantity')
            )['avg_yield']
            
            if milk_yield is not None:  # Only include if we have milk records
                training_data.append({
                    'breed': breed,
                    'age': (pd.Timestamp('now').date() - animal.dob).days / 365.25,
                    'weight': float(animal.weight),
                    'pregnancy_status': animal.pregnancy_status,
                    'lactation_cycle': lactation_cycle,
                    'milk_yield': milk_yield
                })
        
        return pd.DataFrame(training_data)

    def train_model(self):
        """Train the prediction model"""
        df = self.prepare_training_data()
        
        # Print unique breeds before encoding
        print("Unique breeds before encoding:", df['breed'].unique())
        
        # Encode categorical variables
        df['breed'] = self.label_encoders['breed'].fit_transform(df['breed'])
        df['lactation_cycle'] = self.label_encoders['lactation_cycle'].fit_transform(df['lactation_cycle'])
        
        # Print breed label mapping
        print("Breed label mapping:", 
              dict(zip(self.label_encoders['breed'].classes_, 
                       range(len(self.label_encoders['breed'].classes_)))))
        
        # Prepare features and target
        X = df[['breed', 'age', 'weight', 'pregnancy_status', 'lactation_cycle']]
        y = df['milk_yield']
        
        # Convert boolean to integer
        X['pregnancy_status'] = X['pregnancy_status'].astype(int)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        
        # Save model and preprocessors
        joblib.dump(self.model, 'milk_yield_model.joblib')
        joblib.dump(self.scaler, 'scaler.joblib')
        joblib.dump(self.label_encoders, 'label_encoders.joblib')
        
        return {
            'model_score': self.model.score(X_scaled, y),
            'feature_importance': dict(zip(X.columns, self.model.feature_importances_))
        }

    def predict(self, features):
        """
        Predict milk yield based on input features
        
        Args:
            features (dict): {
                'breed': str,
                'age': float,
                'weight': float,
                'pregnancy_status': bool,
                'lactation_cycle': str
            }
        """
        try:
            # Normalize input features
            features['breed'] = str(features['breed']).lower().strip()
            features['lactation_cycle'] = str(features['lactation_cycle']).lower().strip()
            
            # Check if breed exists in known labels
            known_breeds = self.label_encoders['breed'].classes_
            
            if features['breed'] not in known_breeds:
                # If breed is unseen, find the closest match
                closest_breed = min(known_breeds, key=lambda x: abs(len(x) - len(features['breed'])))
                print(f"WARNING: Breed '{features['breed']}' not found. Using closest match: '{closest_breed}'")
                features['breed'] = closest_breed
            
            # Prepare features
            df = pd.DataFrame([features])
            
            # Encode categorical variables
            df['breed'] = self.label_encoders['breed'].transform([features['breed']])
            df['lactation_cycle'] = self.label_encoders['lactation_cycle'].transform([features['lactation_cycle']])
            
            # Convert boolean to integer
            df['pregnancy_status'] = int(features['pregnancy_status'])
            
            # Scale features
            X_scaled = self.scaler.transform(df)
            
            # Make prediction
            prediction = self.model.predict(X_scaled)[0]
            
            return float(prediction)
            
        except Exception as e:
            raise ValueError(f"Prediction error: {str(e)}")