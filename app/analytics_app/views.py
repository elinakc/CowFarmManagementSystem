from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import joblib
import numpy as np


model = joblib.load("milk_yield_model.joblib")
scaler = joblib.load("scaler.joblib")
label_encoders = joblib.load("label_encoders.joblib")

@csrf_exempt  
def predict_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  


            required_fields = ["breed", "age", "weight", "pregnancy_status", "lactation_cycle"]
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Missing field: {field}"}, status=400)

           
            breed = str(data["breed"]).lower().strip()
            age = float(data["age"])
            weight = float(data["weight"])
            pregnancy_status = int(data["pregnancy_status"])
            lactation_cycle = str(data["lactation_cycle"]).lower().strip()

            
            if breed not in label_encoders["breed"].classes_:
                breed = label_encoders["breed"].classes_[0]  
            if lactation_cycle not in label_encoders["lactation_cycle"].classes_:
                lactation_cycle = label_encoders["lactation_cycle"].classes_[0]  

           
            breed_encoded = label_encoders["breed"].transform([breed])[0]
            lactation_cycle_encoded = label_encoders["lactation_cycle"].transform([lactation_cycle])[0]

           
            input_data = np.array([[breed_encoded, age, weight, pregnancy_status, lactation_cycle_encoded]])
            input_scaled = scaler.transform(input_data)  # Scale input

            # Predict milk yield
            prediction = model.predict(input_scaled)[0]

            return JsonResponse({"predicted_milk_yield": round(float(prediction), 2)})

        except ValueError as ve:
            return JsonResponse({"error": f"Invalid input: {str(ve)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
