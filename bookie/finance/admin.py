from django.contrib import admin
import datetime

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


def add_monthly_budget(modeladmin, request, queryset):
    for category in queryset:
        months = {1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April', 5: 'Mai',
                  6: 'Juni', 7: 'Juli', 8: 'August', 9: 'September', 10: 'Oktober',
                  11: 'November', 12: 'Dezember'}
        
        month_nr = 1
        date = datetime.date(datetime.date.today().year, month_nr, 1)
        category.income_set.create(name=months[month_nr], amount=category.monthly_budget, date=date)
        category.save()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_budget', 'saldo')
    inlines = [ExpenseInline, IncomeInline]

    actions = [add_monthly_budget]


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

