# Generated by Django 5.1.1 on 2024-11-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('conference', 'Conference'), ('concert', 'Concert'), ('workshop', 'Workshop'), ('seminar', 'Seminar'), ('others', 'Others')], default='others', max_length=20),
        ),
    ]
