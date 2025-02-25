from rest_framework import serializers
from django.db import models

from datetime import datetime

from .models import User, Credit, Plan, Payment, Dictionary


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ['issuance_date', 'return_date', 'actual_return_date', 'body', 'percent']
    
    closed = serializers.SerializerMethodField()
    sum_payments = serializers.SerializerMethodField()
    overdue_days = serializers.SerializerMethodField()
    sum_body_payments = serializers.SerializerMethodField()
    sum_interest_payments = serializers.SerializerMethodField()

    def get_closed(self, obj):
        if obj.actual_return_date:
            return True
        else:
            return False

    def get_sum_payments(self, obj):
        return obj.payments.aggregate(total=models.Sum('sum'))['total'] or 0
    
    def get_sum_body_payments(self, obj):
        type_body = Dictionary.objects.get(name='Тіло')
        return obj.payments.filter(type=type_body).aggregate(total=models.Sum('sum'))['total'] or 0
    
    def get_sum_interest_payments(self, obj):
        type_interest = Dictionary.objects.get(name='Відсотки')
        return obj.payments.filter(type=type_interest).aggregate(total=models.Sum('sum'))['total'] or 0
    
    def get_overdue_days(self, obj):
        if obj.return_date and not obj.actual_return_date:
            diff = datetime.now().date() - obj.return_date
            return max(diff.days, 0)
        return 0


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = '__all__'