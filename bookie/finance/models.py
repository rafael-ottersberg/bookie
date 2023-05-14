from django.db import models
from django.contrib import admin


class Category(models.Model):
    name = models.CharField(max_length=64)
    monthly_budget = models.FloatField(default=0)
    saldo = models.FloatField(default=0)

    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"

    def __str__(self):
        return self.name

    def calculate_saldo(self):
        self.saldo = sum([income.amount for income in self.income_set.all()])\
            - sum([expense.amount for expense in self.expense_set.all()])
        self.save()


class Expense(models.Model):
    name = models.CharField(max_length=128)
    amount = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        verbose_name = "Ausgabe"
        verbose_name_plural = "Ausgaben"

    def __str__(self):
        return self.name


class Income(models.Model):
    name = models.CharField(max_length=128)
    amount = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        verbose_name = "Einnahme"
        verbose_name_plural = "Einnahmen"

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=128)
    saldo = models.FloatField(default=0)

    class Meta:
        verbose_name = "Konto"
        verbose_name_plural = "Konten"

    def __str__(self):
        return self.name
