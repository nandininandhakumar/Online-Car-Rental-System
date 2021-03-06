# Generated by Django 4.0.3 on 2022-04-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('car_model', models.CharField(max_length=50)),
                ('fuel_type', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('picture', models.FileField(null=True, upload_to='media')),
            ],
        ),
    ]
