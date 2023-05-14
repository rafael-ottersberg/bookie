# Generated by Django 4.2.1 on 2023-05-14 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('saldo', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'Konto',
                'verbose_name_plural': 'Konten',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategorie', 'verbose_name_plural': 'Kategorien'},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name': 'Ausgabe', 'verbose_name_plural': 'Ausgaben'},
        ),
        migrations.AlterModelOptions(
            name='income',
            options={'verbose_name': 'Einnahme', 'verbose_name_plural': 'Einnahmen'},
        ),
    ]
