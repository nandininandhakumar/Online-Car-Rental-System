# Generated by Django 4.0.3 on 2022-05-24 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_customer_stripe_subscription_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'active'), ('pause', 'pause')], max_length=15, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.customerstatus'),
        ),
    ]