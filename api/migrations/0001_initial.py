# Generated by Django 5.1.6 on 2025-02-25 01:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuance_date', models.DateField(auto_now_add=True)),
                ('return_date', models.DateField()),
                ('actual_return_date', models.DateField(blank=True, null=True)),
                ('body', models.DecimalField(decimal_places=2, max_digits=8)),
                ('percent', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50, unique=True)),
                ('registration_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('credit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='api.credit')),
                ('type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_type', to='api.dictionary')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.DateField()),
                ('sum', models.DecimalField(decimal_places=2, max_digits=8)),
                ('category_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plans', to='api.dictionary')),
            ],
        ),
        migrations.AddField(
            model_name='credit',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='api.user'),
        ),
    ]
