# Generated by Django 4.2.1 on 2023-08-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightbook', '0007_alter_flight_comment_alter_flight_distance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialflight',
            name='photo_payment',
            field=models.CharField(choices=[(None, 'Keine Fotos'), ('Bar', 'Bar'), ('Desk', 'Desk'), ('Kreditkarte', 'Kreditkarte')], default=None, max_length=16),
        ),
        migrations.AlterField(
            model_name='commercialflight',
            name='tip',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='commercialflight',
            name='tip_payment',
            field=models.CharField(choices=[(None, 'Kein Trinkgeld'), ('Bar', 'Bar'), ('Kreditkarte', 'Kreditkarte')], default=None, max_length=16),
        ),
    ]