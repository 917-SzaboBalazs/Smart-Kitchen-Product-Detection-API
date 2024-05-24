from django.urls import path
from .views import TestView
from .views import PredictDairyProductView

urlpatterns = [
    path('test/', TestView.as_view(), name='TestView'),
    path('predict_dairy_product/', PredictDairyProductView.as_view(), name='PredictDairyProductView'),
]