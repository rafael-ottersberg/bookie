from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Category, Expense, Income

class CategoryModelTests(TestCase):
    def test_category_sum_saldo(self):
        """Test that the saldo is calculated correctly."""
        category = Category.objects.create(name="Test Category", monthly_budget=100)
        Expense.objects.create(name="Test Expense", amount=50, category=category, date=timezone.now())
        Income.objects.create(name="Test Income", amount=100, category=category, date=timezone.now())
        Expense.objects.create(name="Test Expense 2", amount=2.50, category=category, date=timezone.now())
        category.calculate_saldo()
        assert category.saldo == 47.5

class CategoryDetailViewTest(TestCase):
    def test_no_expense_no_income(self):
        """Test that correct message is shown when no expenses or incomes are present."""
        category = Category.objects.create(name="Test Category", monthly_budget=100)
        response = self.client.get(reverse("finance:category-detail", args=[category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Keine Ausgaben")
        self.assertContains(response, "Keine Einnahmen")
        self.assertContains(response, "0.0")

    def test_last_10_expense(self):
        """Test that only the last 10 expenses are shown."""
        category = Category.objects.create(name=f"Test Category", monthly_budget=100)
        for i in range(12):
            Expense.objects.create(name=f"Test Expense {i}", amount=50, category=category, date=timezone.now()-timezone.timedelta(days=i))

        response = self.client.get(reverse("finance:category-detail", args=[category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Expense 0")
        self.assertContains(response, "Test Expense 9")
        self.assertNotContains(response, "Test Expense 10")

    def test_last_10_income(self):
        """Test that only the last 10 incomes are shown."""
        category = Category.objects.create(name=f"Test Category", monthly_budget=100)
        for i in range(12):
            Income.objects.create(name=f"Test Income {i}", amount=50, category=category, date=timezone.now()-timezone.timedelta(days=i))

        response = self.client.get(reverse("finance:category-detail", args=[category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Income 0")
        self.assertContains(response, "Test Income 9")
        self.assertNotContains(response, "Test Income 10")

    

