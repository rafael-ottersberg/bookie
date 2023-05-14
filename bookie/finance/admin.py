from django.contrib import admin

from .models import Category, Expense, Income, Account

class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0
    search_fields = ['name']
    ordering = ['-date']

class IncomeInline(admin.TabularInline):
    model = Income
    extra = 0
    search_fields = ['name']
    ordering = ['-date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_budget', 'saldo')
    inlines = [ExpenseInline, IncomeInline]

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    ordering = ['-date', 'name']
    list_filter = [
        'category', 
        'date',
    ]
    list_display = ('date', 'name', 'amount')
    search_fields = ['name']
    list_display_links = ('name',)
    list_per_page = 10

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    ordering = ['-date', 'name']
    list_filter = ('category', 'date')
    list_display = ('date', 'name', 'amount')
    search_fields = ['name']
    list_display_links = ('name',)


admin.site.register(Account)

