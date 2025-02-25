from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User, Credit, Plan, Payment, Dictionary
from .serializers import UserSerializer, CreditSerializer, PlanSerializer, PaymentSerializer, DictionarySerializer


class UserCreditsViewSet(viewsets.ViewSet):
    def list(self, request, user_id=None):
        user = get_object_or_404(User, pk=user_id)
        credits = user.credits.all()
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data)
