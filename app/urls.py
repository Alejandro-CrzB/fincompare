from django.urls import path
from .views import compare_returns

urlpatterns = [
    path('compare/', compare_returns),
]
