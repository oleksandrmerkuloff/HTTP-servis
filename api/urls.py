from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserCreditsViewSet, plans_insert, plans_performance, year_performance


router = DefaultRouter()
router.register(r'user_credits', UserCreditsViewSet, basename='usercredits')

urlpatterns = [
    path('', include(router.urls)),
    path('plans_insert/', plans_insert, name='plans_insert'),
    path('plans_performance/', plans_performance, name='plans_performance'),
    path('year_performance/', year_performance, name='year_performance'),
]
