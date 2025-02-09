import pandas as pd
from ConnectReactandDjango.Backend.CowFarmManagementSystem.app.analytics_app import models
from app.animal_records.models import AnimalRecords
from app.milk_records.models import MilkRecord
from .random_forest import RandomForest

def get_training_data():
    animals = AnimalRecords.objects.prefetch_related('milk_records')
    data = []

    for animal in animals:
        milk_yield = MilkRecord.objects.filter(animal=animal).aggregate(
            avg_yield=(
                (models.Avg('morning_milk_quantity') + 
                 models.Avg('afternoon_milk_quantity') + 
                 models.Avg('evening_milk_quantity')) / 3
            )
        )['avg_yield']

        if milk_yield:
            data.append({
                'age': (pd.Timestamp('now').date() - animal.dob).days / 365.25,
                'weight': animal.weight,
                'pregnancy_status': int(animal.pregnancy_status),
                'lactation_cycle': animal.lactation_cycle,
                'milk_yield': milk_yield
            })

    return pd.DataFrame(data)

# Train the model
df = get_training_data()
X_train = df[['age', 'weight', 'pregnancy_status', 'lactation_cycle']].values
y_train = df['milk_yield'].values

rf_model = RandomForest(n_trees=10, max_depth=3)
rf_model.fit(X_train, y_train)

# Save the model
import pickle
with open('rf_model.pkl', 'wb') as file:
    pickle.dump(rf_model, file)
