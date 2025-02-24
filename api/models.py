from django.db import models
from django.core.exceptions import ValidationError


class User(models.Model):
    login = models.CharField(max_length=50, blank=False, null=False, unique=True)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.login


class Credit(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='credits')
    issuance_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=False, blank=False)
    actual_return_date = models.DateField(null=True, blank=True)
    body = models.DecimalField(max_digits=8, decimal_places=2)
    percent = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.user_id.login} --> {self.body}'


class Dictionary(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False)

    def __str__(self):
        return self.name


class Plan(models.Model):
    period = models.DateField()
    sum = models.DecimalField(max_digits=8, decimal_places=2)
    category_id = models.ForeignKey(Dictionary, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='plans')

    def __str__(self):
        return f'{self.period} - {self.sum}'
    
    def date_check(self):
        if self.period.day != 1:
            raise ValidationError('Період повинен бути першим числом місяця!')

    def save(self, *args, **kwargs):
        self.date_check()
        return super().save(*args, **kwargs)


class Payment(models.Model):
    sum = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    credit_id = models.ForeignKey(Credit, on_delete=models.CASCADE,
                                  related_name='payments')
    type_id = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name='payment_type')

    def __str__(self):
        return f'{self.payment_date} - {self.sum}'
