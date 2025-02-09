import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from django.db.models import Avg, Sum

class CustomLabelEncoder:
    """Encode categorical variables"""
    def __init__(self):
        self.classes_ = {}
        
    def fit(self, values: List[str]):
        unique_values = sorted(set(values))
        self.classes_ = {val: idx for idx, val in enumerate(unique_values)}
        
    def transform(self, values: List[str]) -> List[int]:
        return [self.classes_.get(val.lower().strip(), 0) for val in values]

class CustomLinearRegression:
    """Custom Linear Regression implementation"""
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
        
    def fit(self, X: List[List[float]], y: List[float]):
        """Train the model using gradient descent"""
        # Convert to numpy arrays for easier computation
        X = np.array(X)
        y = np.array(y)
        
        # Initialize parameters
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        # Gradient descent
        for _ in range(self.n_iterations):
            # Make predictions
            y_pred = np.dot(X, self.weights) + self.bias
            
            # Calculate gradients
            dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
            db = (1/n_samples) * np.sum(y_pred - y)
            
            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
    
    def predict(self, X: List[List[float]]) -> List[float]:
        """Make predictions"""
        X = np.array(X)
        return np.dot(X, self.weights) + self.bias

class MilkYieldPredictor:
    """Main predictor class for milk yield"""
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.model = CustomLinearRegression(
            learning_rate=learning_rate,
            n_iterations=n_iterations
        )
        self.label_encoders = {
            'breed': CustomLabelEncoder(),
            'lactation_cycle': CustomLabelEncoder()
        }
        self.feature_means = {}
        self.feature_stds = {}
        
    def _calculate_age(self, dob: datetime.date) -> float:
        """Calculate age in years"""
        today = datetime.now().date()
        return (today - dob).days / 365.25
    
    def _normalize_features(self, features: List[List[float]], training=False) -> List[List[float]]:
        """Normalize numerical features"""
        features = np.array(features)
        
        if training:
            # Calculate means and stds during training
            self.feature_means = np.mean(features, axis=0)
            self.feature_stds = np.std(features, axis=0)
            self.feature_stds[self.feature_stds == 0] = 1  # Avoid division by zero
            
        # Normalize features
        normalized = (features - self.feature_means) / self.feature_stds
        return normalized.tolist()
    
    def prepare_training_data(self, animals_queryset):
        """Prepare training data from Django queryset"""
        training_data = []
        
        # First pass: collect all breeds and lactation cycles for encoding
        breeds = []
        lactation_cycles = []
        
        for animal in animals_queryset:
            breeds.append(str(animal.breed).lower().strip())
            lactation_cycles.append(str(animal.lactation_cycle).lower().strip())
        
        # Fit label encoders
        self.label_encoders['breed'].fit(breeds)
        self.label_encoders['lactation_cycle'].fit(lactation_cycles)
        
        # Second pass: prepare features and targets
        X = []
        y = []
        
        for animal in animals_queryset:
            # Calculate average daily milk yield
            milk_records = animal.milk_records.all()
            if not milk_records.exists():
                continue
            
            avg_yield = milk_records.aggregate(
                avg_total=Avg(
                    Sum('morning_milk_quantity') +
                    Sum('afternoon_milk_quantity') +
                    Sum('evening_milk_quantity')
                )
            )['avg_total']
            
            if avg_yield is not None:
                # Prepare features
                features = [
                    self.label_encoders['breed'].transform([str(animal.breed)])[0],
                    self._calculate_age(animal.dob),
                    float(animal.weight),
                    1 if animal.pregnancy_status else 0,
                    self.label_encoders['lactation_cycle'].transform([str(animal.lactation_cycle)])[0]
                ]
                X.append(features)
                y.append(float(avg_yield))
        
        return X, y
    
    def train(self, animals_queryset) -> Dict[str, float]:
        """Train the model using Django queryset"""
        # Prepare data
        X, y = self.prepare_training_data(animals_queryset)
        
        if not X:
            raise ValueError("No valid training data found")
        
        # Normalize features
        X_normalized = self._normalize_features(X, training=True)
        
        # Train model
        self.model.fit(X_normalized, y)
        
        # Calculate metrics
        y_pred = self.model.predict(X_normalized)
        metrics = self._calculate_metrics(y, y_pred)
        
        return metrics
    
    def predict(self, animal_data: Dict[str, Any]) -> float:
        """Make prediction for new animal data"""
        if self.model.weights is None:
            raise ValueError("Model not trained yet")
        
        # Prepare features
        features = [
            self.label_encoders['breed'].transform([str(animal_data['breed'])])[0],
            self._calculate_age(animal_data['dob']),
            float(animal_data['weight']),
            1 if animal_data['pregnancy_status'] else 0,
            self.label_encoders['lactation_cycle'].transform([str(animal_data['lactation_cycle'])])[0]
        ]
        
        # Normalize features
        X_normalized = self._normalize_features([features])
        
        # Make prediction
        prediction = self.model.predict(X_normalized)[0]
        
        # Ensure non-negative prediction
        return max(0, prediction)
    
    def _calculate_metrics(self, y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
        """Calculate regression metrics"""
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Mean Squared Error
        mse = np.mean((y_true - y_pred) ** 2)
        
        # Root Mean Squared Error
        rmse = np.sqrt(mse)
        
        # R-squared
        y_mean = np.mean(y_true)
        ss_total = np.sum((y_true - y_mean) ** 2)
        ss_residual = np.sum((y_true - y_pred) ** 2)
        r2 = 1 - (ss_residual / ss_total if ss_total != 0 else 0)
        
        # Mean Absolute Percentage Error
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        return {
            'mse': float(mse),
            'rmse': float(rmse),
            'r2': float(r2),
            'mape': float(mape)
        }

# import pandas as pd
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
# from app.milk_records.models import MilkRecord
# from app.animal_records.models import AnimalRecords
# from app.analytics_app.models import MilkYieldPrediction

# def predict_milk_yield():
    # Fetch data from MilkRecord and AnimalRecords models
    milk_data = MilkRecord.objects.all().values('cow_id', 'milking_date', 'morning_milk_quantity', 'afternoon_milk_quantity', 'evening_milk_quantity')
    cow_data = AnimalRecords.objects.all().values('id', 'dob', 'breed', 'weight', 'pregnancy_status', 'lactation_cycle')

    # Convert to DataFrames
    milk_df = pd.DataFrame(milk_data)
    cow_df = pd.DataFrame(cow_data)

    # Merge data on cow_id
    df = pd.merge(milk_df, cow_df, left_on='cow_id', right_on='id')

    # Feature Engineering
    df['total_milk_quantity'] = df['morning_milk_quantity'] + df['afternoon_milk_quantity'] + df['evening_milk_quantity']
    df['age'] = (pd.to_datetime(df['milking_date']) - pd.to_datetime(df['dob'])).dt.days // 365  # Age in years
    df['pregnancy_status'] = df['pregnancy_status'].astype(int)  # Convert boolean to int
    df['lactation_cycle'] = df['lactation_cycle'].map({'dry': 0, 'lactating': 1, 'fresh': 2})  # Encode lactation cycle

    # Select features and target
    features = ['age', 'weight', 'pregnancy_status', 'lactation_cycle']
    X = df[features]
    y = df['total_milk_quantity']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on test data
    y_pred = model.predict(X_test)

    # Evaluate model
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Predict on the entire dataset
    df['predicted_yield'] = model.predict(X)

    # Save predictions to the database
    for _, row in df.iterrows():
      MilkYieldPrediction.objects.create(
            cow_id=row['cow_id'],
            predicted_yield=row['predicted_yield']
        )

    
    # Return the trained model and evaluation metrics
    return model, mse