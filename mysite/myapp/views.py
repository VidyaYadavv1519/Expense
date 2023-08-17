from django.shortcuts import render,redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
from django.views import View
from rest_framework import viewsets
from .serializers import ExpenseSerializer

# Create your views here.
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()



# def index(request):
#     if request.method == "POST":
#         expense = ExpenseForm(request.POST)
#         if expense.is_valid():
#             expense.save()
#     expenses = Expense.objects.all()
#     total_expenses = expenses.aggregate(Sum('amount'))

# #Logic to create 365 days expenses
#     last_year = datetime.date.today() - datetime.timedelta(days=365)
#     data = Expense.objects.filter(date__gt=last_year)
#     yearly_sum = data.aggregate(Sum('amount'))

# #Logic to create 30 days expenses
#     last_month = datetime.date.today() - datetime.timedelta(days=30)
#     data = Expense.objects.filter(date__gt=last_month)
#     monthly_sum = data.aggregate(Sum('amount'))

# #Logic to create 7 days expenses
#     last_week = datetime.date.today() - datetime.timedelta(days=7)
#     data = Expense.objects.filter(date__gt=last_week)
#     weekly_sum = data.aggregate(Sum('amount'))


#     daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    

#     categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
#     print(categorical_sums)


#     expense_form = ExpenseForm()
#     return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum,'weekly_sum':weekly_sum,'monthly_sum':monthly_sum,'daily_sums':daily_sums,'categorical_sums':categorical_sums})

class IndexView(View):
    template_name = 'myapp/index.html'
    form_class = ExpenseForm

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.all()
        total_expenses = expenses.aggregate(Sum('amount'))

        last_year = datetime.date.today() - datetime.timedelta(days=365)
        yearly_sum = Expense.objects.filter(date__gt=last_year).aggregate(Sum('amount'))

        last_month = datetime.date.today() - datetime.timedelta(days=30)
        monthly_sum = Expense.objects.filter(date__gt=last_month).aggregate(Sum('amount'))

        last_week = datetime.date.today() - datetime.timedelta(days=7)
        weekly_sum = Expense.objects.filter(date__gt=last_week).aggregate(Sum('amount'))

        daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))

        categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))

        expense_form = self.form_class()
        return render(
            request,
            self.template_name,
            {
                'expense_form': expense_form,
                'expenses': expenses,
                'total_expenses': total_expenses,
                'yearly_sum': yearly_sum,
                'weekly_sum': weekly_sum,
                'monthly_sum': monthly_sum,
                'daily_sums': daily_sums,
                'categorical_sums': categorical_sums,
            }
        )

    def post(self, request, *args, **kwargs):
        expense_form = self.form_class(request.POST)
        if expense_form.is_valid():
            expense_form.save()

        return self.get(request, *args, **kwargs)

# def edit(request,id):
#     expense = Expense.objects.get(id=id)
#     expense_form = ExpenseForm(instance=expense)
#     if request.method == 'POST':
#         expense = Expense.objects.get(id=id)
#         form = ExpenseForm(request.POST,instance=expense)
#         if form.is_valid():
#             form.save()
#             return redirect('index')

#     return render(request,'myapp/edit.html',{'expense_form':expense_form})

class EditView(View):
    template_name = 'myapp/edit.html'
    form_class = ExpenseForm

    def get(self, request, id, *args, **kwargs):
        expense = Expense.objects.get(id=id)
        expense_form = self.form_class(instance=expense)
        return render(
            request,
            self.template_name,
            {'expense_form': expense_form}
        )

    def post(self, request, id, *args, **kwargs):
        expense = Expense.objects.get(id=id)
        form = self.form_class(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

        return render(
            request,
            self.template_name,
            {'expense_form': form}
        )

# def delete(request,id):
#     if request.method == 'POST' and 'delete' in request.POST:
#         expense = Expense.objects.get(id=id)
#         expense.delete()
#     return redirect('index')

class DeleteView(View):
    def post(self, request, id, *args, **kwargs):
        if 'delete' in request.POST:
            expense = Expense.objects.get(id=id)
            expense.delete()
        return redirect('index')
