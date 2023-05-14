from finance.models import Category, Expense, Income, Account
import pandas as pd
import datetime

months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli',
            'August', 'September', 'Oktober', 'November', 'Dezember']

sheet_names = {
 'Wohnen': 2282.92,
 'Medien': 20,
 'Haushalt': 1000,
 'Kleider-Schuhe':200,
 'Geschenke': 100,
 'Sackgeld Rafael': 100,
 'Sackgeld Rahel': 100,
 'Sport & Musik': 100,
 'ÖV-Ferien': 865,
 'Auto': 378.33,
 'Spenden': 130,
 'Gesundheitskosten': 870,
 'Versicherungen': 35,
 'Steuern': 740,
 'Anschaffungen': 150,
 'Berufskosten': 120,
 'Sparen': 10,
 'Lohnzahlungen': 7200,
 'Gleitschirmfirma': 0
}



account_names = [
    'Postfinance Rafael',
    'Postfinance Rahel',
    'ABS',
    'Kreditkarte Rafael',
    'Kreditkarte Rahel',
    'Bargeld']


def create_categories():
    for sheet_name in sheet_names.keys():
        c = Category.objects.create(name=sheet_name, saldo=0, monthly_budget=sheet_names[sheet_name])
        c.save()

def create_income_expense_lohn():
    df = pd.read_excel('Kontenblaetter_2023.xlsx', sheet_name='Lohnzahlungen', skiprows=4)
    df = df[df['Rafael'].notna()]

    for i, row in df.iterrows():
        date = datetime.date(year=2023, month=i+1, day=1)
        e = Income.objects.create(
            date=date,
            category=Category.objects.get(name='Lohnzahlungen'),
            amount=row['Rafael'],
            name=f"{row['Journal']} Rafael")
        e.save()

        e = Income.objects.create(
            date=date,
            category=Category.objects.get(name='Lohnzahlungen'),
            amount=row['Rahel'],
            name=f"{row['Journal']} Rahel")
        e.save()

        e = Income.objects.create(
            date=date,
            category=Category.objects.get(name='Lohnzahlungen'),
            amount=row['Stipendium'],
            name=f"{row['Journal']} Stipendium")
        e.save()

    for i in range(2,6):
        e = Expense.objects.create(
            date=datetime.date(year=2023, month=i, day=1),
            category=Category.objects.get(name='Lohnzahlungen'),
            amount=sheet_names['Lohnzahlungen'],
            name=f"{months[i-1]}")
        e.save()


def create_expenses_income():
    for sheet_name in list(sheet_names.keys()):
        if sheet_name == 'Lohnzahlungen':
            continue
        df = pd.read_excel('Kontenblaetter_2023.xlsx', sheet_name=sheet_name, skiprows=3)

        df = df[df['Journal'].notna()]
        df_einnahmen = df[df['Einnahmen'].notna()]
        df_ausgaben = df[df['Ausgaben'].notna()]

        for _, row in df_einnahmen.iterrows():
            print(row['Datum'], row['Einnahmen'], row['Journal'])
            e = Income.objects.create(
                date=row['Datum'],
                category=Category.objects.get(name=sheet_name),
                amount=row['Einnahmen'],
                name=row['Journal'])
            e.save()

        for _, row in df_ausgaben.iterrows():
            print(row['Datum'], row['Ausgaben'], row['Journal'])
            e = Expense.objects.create(
                date=row['Datum'],
                category=Category.objects.get(name=sheet_name),
                amount=row['Ausgaben'],
                name=row['Journal'])
            e.save()
    
    for category in Category.objects.all():
        if category.name in ['Lohnzahlungen', 'Gleitschirmfirma', 'Geschenke', 'Sackgeld Rahel']:
            continue
        i = Income.objects.create(
            date='2023-01-01',
            category=category,
            amount=sheet_names[category.name],
            name='Januar')
        i.save()

def create_accounts():
    for account_name in account_names:
        a = Account.objects.create(name=account_name, saldo=0)
        a.save()

def update_saldo():
    for category in Category.objects.all():
        category.calculate_saldo()
        category.save()

def run():
    create_categories()
    create_accounts()
    create_expenses_income()
    create_income_expense_lohn()
    update_saldo()
