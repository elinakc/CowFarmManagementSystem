import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from app.milk_records.models import MilkRecord
from app.animal_records.models import AnimalRecords
from app.analytics_app.models import MilkYieldPrediction

def predict_milk_yield():
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