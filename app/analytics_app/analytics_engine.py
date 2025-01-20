# analytics_app/analytics_engine.py
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import pandas as pd
from django.db.models import Avg, Sum, Count
from django.db.models.functions import TruncMonth, TruncDate

class StatisticalAnalytics:
    @staticmethod
    def calculate_milk_production_stats(milk_records):
        """Calculate detailed milk production statistics"""
        df = pd.DataFrame(milk_records.values())
        
        return {
            'basic_stats': {
                'mean_daily_production': df['total_daily'].mean(),
                'std_dev': df['total_daily'].std(),
                'median': df['total_daily'].median(),
                'min': df['total_daily'].min(),
                'max': df['total_daily'].max(),
            },
            'percentiles': {
                'top_25': df['total_daily'].quantile(0.75),
                'top_10': df['total_daily'].quantile(0.90),
                'bottom_25': df['total_daily'].quantile(0.25),
            },
            'moving_averages': {
                '7_day': df.groupby('milking_date')['total_daily'].rolling(window=7).mean(),
                '30_day': df.groupby('milking_date')['total_daily'].rolling(window=30).mean(),
            }
        }

class PredictiveAnalytics:
    @staticmethod
    def predict_milk_production(milk_records, days_to_predict=30):
        """Predict future milk production using linear regression"""
        # Convert records to DataFrame
        df = pd.DataFrame(milk_records.values())
        df['days_from_start'] = (df['milking_date'] - df['milking_date'].min()).dt.days
        
        # Prepare data for prediction
        X = df['days_from_start'].values.reshape(-1, 1)
        y = df['total_daily'].values
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate future dates for prediction
        future_days = np.array(range(X.max() + 1, X.max() + days_to_predict + 1))
        future_predictions = model.predict(future_days.reshape(-1, 1))
        
        return {
            'predictions': [
                {
                    'date': (df['milking_date'].min() + timedelta(days=int(day))).strftime('%Y-%m-%d'),
                    'predicted_yield': float(pred)
                }
                for day, pred in zip(future_days, future_predictions)
            ],
            'confidence_score': model.score(X, y),
            'trend': 'increasing' if model.coef_[0] > 0 else 'decreasing'
        }
    
    @staticmethod
    def predict_health_risks(health_records, animal_records):
        """Predict health risks based on historical data"""
        df = pd.DataFrame(health_records.values())
        
        # Calculate risk scores based on historical health issues
        risk_factors = df.groupby('cow_id').agg({
            'diagnosed_illness': 'count',
            'treatment_cost': 'sum',
            'health_condtion': lambda x: (x == 'sick').sum()
        }).reset_index()
        
        # Normalize risk factors
        scaler = StandardScaler()
        risk_factors_scaled = scaler.fit_transform(
            risk_factors[['diagnosed_illness', 'treatment_cost']]
        )
        
        # Calculate overall risk score
        risk_factors['risk_score'] = np.mean(risk_factors_scaled, axis=1)
        
        return {
            'high_risk_animals': risk_factors.nlargest(5, 'risk_score').to_dict('records'),
            'risk_distribution': {
                'low_risk': len(risk_factors[risk_factors['risk_score'] < 0.3]),
                'medium_risk': len(risk_factors[(risk_factors['risk_score'] >= 0.3) & 
                                              (risk_factors['risk_score'] < 0.7)]),
                'high_risk': len(risk_factors[risk_factors['risk_score'] >= 0.7])
            }
        }

class ClusteringAnalytics:
    @staticmethod
    def cluster_animals_by_performance(animal_records, milk_records):
        """Cluster animals based on performance metrics"""
        # Prepare feature matrix
        features = []
        for animal in animal_records:
            animal_milk = milk_records.filter(cow=animal)
            features.append([
                animal_milk.aggregate(Avg('total_daily'))['total_daily__avg'],
                animal.weight,
                animal_milk.count(),  # number of records
            ])
        
        # Normalize features
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(features_scaled)
        
        # Analyze clusters
        cluster_results = []
        for i in range(3):
            cluster_indices = clusters == i
            cluster_results.append({
                'cluster_id': i,
                'size': sum(cluster_indices),
                'avg_milk_production': np.mean([f[0] for j, f in enumerate(features) if clusters[j] == i]),
                'avg_weight': np.mean([f[1] for j, f in enumerate(features) if clusters[j] == i]),
                'animals': [a.id for j, a in enumerate(animal_records) if clusters[j] == i]
            })
        
        return {
            'clusters': cluster_results,
            'cluster_centers': kmeans.cluster_centers_.tolist(),
            'cluster_distribution': pd.Series(clusters).value_counts().to_dict()
        }

class AdvancedAnalyticsService:
    def __init__(self, milk_records, health_records, animal_records):
        self.milk_records = milk_records
        self.health_records = health_records
        self.animal_records = animal_records

    def generate_advanced_analytics(self):
        """Generate comprehensive advanced analytics"""
        return {
            'statistical_analysis': StatisticalAnalytics.calculate_milk_production_stats(
                self.milk_records
            ),
            'predictions': {
                'milk_production': PredictiveAnalytics.predict_milk_production(
                    self.milk_records
                ),
                'health_risks': PredictiveAnalytics.predict_health_risks(
                    self.health_records,
                    self.animal_records
                )
            },
            'clustering': ClusteringAnalytics.cluster_animals_by_performance(
                self.animal_records,
                self.milk_records
            )
        }