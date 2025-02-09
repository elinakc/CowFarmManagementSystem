import pickle
import numpy as np

def predict_milk_yield(new_animal):
    with open('rf_model.pkl', 'rb') as file:
        rf_model = pickle.load(file)

    X_test = [[new_animal['age'], new_animal['weight'], new_animal['pregnancy_status'], new_animal['lactation_cycle']]]
    return rf_model.predict(np.array(X_test))
