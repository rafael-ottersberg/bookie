from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64)
    monthly_budget = models.FloatField(default=0)
    saldo = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=128)
    amount = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()