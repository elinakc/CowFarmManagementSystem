# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.ensemble import RandomForestRegressor
# from django.db.models import Avg
# import pandas as pd
# import numpy as np
# import joblib

# from app.animal_records.models import AnimalRecords
# from app.milk_records.models import MilkRecord

# class MilkYieldPredictor:
#     def __init__(self):
#         self.model = RandomForestRegressor(
#             n_estimators=100,
#             random_state=42
#         )
#         self.scaler = StandardScaler()
#         self.label_encoders = {
#             'breed': LabelEncoder(),
#             'lactation_cycle': LabelEncoder()
#         }
    
#     def prepare_training_data(self):
    
#         animals = AnimalRecords.objects.all().prefetch_related('milk_records')
        
#         training_data = []
#         for animal in animals:
#             # Normalize breed and lactation cycle
#             breed = str(animal.breed).lower().strip()
#             lactation_cycle = str(animal.lactation_cycle).lower().strip()
            
#             # Calculate average daily milk yield
#             milk_yield = animal.milk_records.aggregate(
#                 avg_yield=Avg('morning_milk_quantity') + 
#                          Avg('afternoon_milk_quantity') + 
#                          Avg('evening_milk_quantity')
#             )['avg_yield']
            
#             if milk_yield is not None:  
#                 training_data.append({
#                     'breed': breed,
#                     'age': (pd.Timestamp('now').date() - animal.dob).days / 365.25,
#                     'weight': float(animal.weight),
#                     'pregnancy_status': animal.pregnancy_status,
#                     'lactation_cycle':animal.lactation_cycle,
#                     'milk_yield': milk_yield
#                 })
        
#         return pd.DataFrame(training_data)

#     def train_model(self):
       
#         df = self.prepare_training_data()
    
#         print("Unique breeds before encoding:", df['breed'].unique())
       
#         df['breed'] = self.label_encoders['breed'].fit_transform(df['breed'])
#         df['lactation_cycle'] = self.label_encoders['lactation_cycle'].fit_transform(df['lactation_cycle'])

#         print("Breed label mapping:", 
#               dict(zip(self.label_encoders['breed'].classes_, 
#                        range(len(self.label_encoders['breed'].classes_)))))
        
       
#         X = df[['breed', 'age', 'weight', 'pregnancy_status', 'lactation_cycle']]
#         y = df['milk_yield']
        
    
#         X['pregnancy_status'] = X['pregnancy_status'].astype(int)
        
      
#         X_scaled = self.scaler.fit_transform(X)
        
        
#         self.model.fit(X_scaled, y)

#         joblib.dump(self.model, 'milk_yield_model.joblib')
#         joblib.dump(self.scaler, 'scaler.joblib')
#         joblib.dump(self.label_encoders, 'label_encoders.joblib')
        
#         return {
#             'model_score': self.model.score(X_scaled, y),
#             'feature_importance': dict(zip(X.columns, self.model.feature_importances_))
#         }

#     def predict(self, features):
#         try:
#             features['breed'] = str(features['breed']).lower().strip()
#             features['lactation_cycle'] = str(features['lactation_cycle']).lower().strip()

            
#             df = pd.DataFrame([features])

            
#             known_breeds = self.label_encoders['breed'].classes_
#             if features['breed'] not in known_breeds:
#                 print(f"WARNING: Unseen breed '{features['breed']}'. Assigning default.")
#                 features['breed'] = known_breeds[0]

           
#             known_cycles = self.label_encoders['lactation_cycle'].classes_
#             if features['lactation_cycle'] not in known_cycles:
#                 print(f"WARNING: Unseen lactation cycle '{features['lactation_cycle']}'. Assigning default.")
#                 features['lactation_cycle'] = known_cycles[0]

            
#             df['breed'] = self.label_encoders['breed'].transform([features['breed']])
#             df['lactation_cycle'] = self.label_encoders['lactation_cycle'].transform([features['lactation_cycle']])

           
#             df['pregnancy_status'] = int(features['pregnancy_status'])

           
#             X_scaled = self.scaler.transform(df)
#             prediction = self.model.predict(X_scaled)[0]

#             return float(prediction)
        
#         except Exception as e:
#             raise ValueError(f"Prediction error: {str(e)}")
