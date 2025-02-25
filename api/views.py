import pandas as pd
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db import models

from .models import User, Credit, Plan, Payment, Dictionary
from .serializers import UserSerializer, CreditSerializer, PlanSerializer, PaymentSerializer, DictionarySerializer


class UserCreditsViewSet(viewsets.ViewSet):
    def list(self, request, user_id=None):
        user = get_object_or_404(User, pk=user_id)
        credits = user.credits.all()
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data)


@api_view(['POST',])
def plans_insert(request):

    plans_file = request.FILES.get('file')
    if not plans_file:
        return Response({'error': 'You don\'t upload the file'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        data_frame = pd.read_excel(plans_file)
        for _, row in data_frame.iterrows():
            if row['period'].day != 1:
                return Response({'error': 'Період повинен бути першим днем місяця!'}, status=status.HTTP_400_BAD_REQUEST)
            if Plan.objects.filter(period=row['period'], category__name=row['category']).exists():
                return Response({'error': f'План для {row["category"]} на {row["period"]} вже існує'}, status=status.HTTP_400_BAD_REQUEST)
            category, _ = Dictionary.objects.get_or_create(name=row['category'])
            Plan.objects.create(period=row['period'], sum=row['sum'], category=category)
        return Response({'message': 'Плани були успішно завантаженими'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def plans_performance(request):
    date = request.query_params.get('date')
    if not date:
        return Response({'error': 'Введіть дату'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        date = pd.to_datetime(date)
        plans = Plan.objects.all()
        performance_data = []

        for plan in plans:
            if plan.category.name == "Видача":
                total_issued = Credit.objects.filter(issuance_date__range=[plan.period, date]).aggregate(total=models.Sum('body'))['total'] or 0
            else:
                total_issued = Payment.objects.filter(payment_date__range=[plan.period, date], type=plan.category).aggregate(total=models.Sum('sum'))['total'] or 0

            performance_data.append({
                'period': plan.period,
                'category': plan.category.name,
                'sum': plan.sum,
                'total_issued': total_issued,
                'performance_percent': (total_issued / plan.sum) * 100 if plan.sum != 0 else 0
            })

        return Response(performance_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def year_performance(request):
    year = request.query_params.get('year')
    if not year:
        return Response({'error': 'Введіть рік'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        year = int(year)
        performance_data = []

        for month in range(1, 13):
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year}-{month+1:02d}-01" if month != 12 else f"{year+1}-01-01"
            plans = Plan.objects.filter(period__year=year, period__month=month)
            issued_credits = Credit.objects.filter(issuance_date__range=[start_date, end_date])
            payments = Payment.objects.filter(payment_date__range=[start_date, end_date])

            sum_plans_issued = plans.filter(category__name="Видача").aggregate(total=models.Sum('sum'))['total'] or 0
            sum_credits_issued = issued_credits.aggregate(total=models.Sum('body'))['total'] or 0

            sum_plans_collected = plans.filter(category__name="Збір").aggregate(total=models.Sum('sum'))['total'] or 0
            sum_payments_collected = payments.aggregate(total=models.Sum('sum'))['total'] or 0

            total_year_credits = Credit.objects.filter(issuance_date__year=year).aggregate(total=models.Sum('body'))['total'] or 0
            total_year_payments = Payment.objects.filter(payment_date__year=year).aggregate(total=models.Sum('sum'))['total'] or 0

            performance_data.append({
                'month_year': f"{year}-{month:02d}",
                'count_credits_issued': issued_credits.count(),
                'sum_plans_issued': sum_plans_issued,
                'sum_credits_issued': sum_credits_issued,
                'performance_percent_issued': (sum_credits_issued / sum_plans_issued) * 100 if sum_plans_issued != 0 else 0,
                'count_payments': payments.count(),
                'sum_plans_collected': sum_plans_collected,
                'sum_payments_collected': sum_payments_collected,
                'performance_percent_collected': (sum_payments_collected / sum_plans_collected) * 100 if sum_plans_collected != 0 else 0,
                'percent_of_year_credits': (sum_credits_issued / total_year_credits) * 100 if total_year_credits != 0 else 0,
                'percent_of_year_payments': (sum_payments_collected / total_year_payments) * 100 if total_year_payments != 0 else 0,
            })

        return Response(performance_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
