
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .ml_models import MilkYieldPredictor

predictor = MilkYieldPredictor()

@csrf_exempt
def train_model(request):
    if request.method == 'POST':
        try:
            results = predictor.train_model()
            return JsonResponse({
                'status': 'success',
                'results': results
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

@csrf_exempt
def predict_yield(request):
    if request.method == 'POST':
        try:
            features = json.loads(request.body)
            prediction = predictor.predict(features)
            return JsonResponse({
                'status': 'success',
                'predicted_milk_yield': prediction
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)