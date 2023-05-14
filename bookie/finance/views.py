from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
import datetime
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import expense_form, income_form

from .models import Category, Account


@login_required
def home(request):
    return render(request, "finance/home.html")


@login_required    
def overview(request):
    template_name = "finance/overview.html"

    total_categories = sum([category.saldo for category in Category.objects.all()])
    total_accounts = sum([account.saldo for account in Account.objects.all()])

    difference = total_accounts - total_categories

    context = {
        "categories": Category.objects.all(),
        "accounts": Account.objects.all(),
        "difference": difference,
    }
    return render(request, template_name, context)

@login_required
def add_expense(request):
    if request.method == "POST":
        form = expense_form(request.POST)
        if form.is_valid():
            form.save()
            for category in Category.objects.all():
                category.calculate_saldo()
                category.save()
            return HttpResponseRedirect(reverse("finance:home"))
    else:
        initial = {"date": timezone.now().strftime("%Y-%m-%d")}
        if Category.objects.filter(name="Haushalt").exists():
            initial["category"] = Category.objects.get(name="Haushalt")
        form = expense_form(initial=initial)

    return render(request, "finance/add_expense.html", {"form": form})

@login_required
def add_income(request):
    if request.method == "POST":
        form = income_form(request.POST)
        if form.is_valid():
            form.save()
            for category in Category.objects.all():
                category.calculate_saldo()
                category.save()
            return HttpResponseRedirect(reverse("finance:home"))
    else:
        initial = {"date": timezone.now().strftime("%Y-%m-%d")}
        form = income_form(initial=initial)

    return render(request, "finance/add_income.html", {"form": form})


class CategoryDetail(LoginRequiredMixin, generic.DetailView):
    model = Category
    template_name = "finance/category.html"

    def get_context_data(self, **kwargs):
        show_last = 10
        context = super().get_context_data(**kwargs)
        context["expenses"] = self.object.expense_set.order_by("-date")[:show_last]
        context["incomes"] = self.object.income_set.order_by("-date")[:show_last]
        return context
