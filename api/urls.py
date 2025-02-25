from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserCreditsViewSet, plans_insert, plans_performance, year_performance


router = DefaultRouter()
router.register('user_credits', UserCreditsViewSet, basename='usercredits')

urlpatterns = [
    path('', include(router.urls)),
    path('plans_insert/', plans_insert, name='plans_insert'),
    path('plans_perfomance/', plans_performance, name='plans_perfomance'),
    path('year_perfomance/', year_performance, name='year_perfomance')
]