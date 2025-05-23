from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.transactions.models import *
from django.contrib import messages

# Create your views here.

def budget(request):
    category = Category.objects.filter(user=request.user, type='EX')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        categories = request.POST.getlist('categories')

        budget = Budget.objects.create(
            user=request.user,
            name=name,
            amount=amount,
            start_date=start_date,
            end_date=end_date
        )
        
        budget.categories.set(categories)
        budget.save()
    
    context = {
        'category': category,
    }
    return render(request, 'budgets/budget_create.html', context)

def list(request):
    budgets = Budget.objects.filter(user=request.user)
    
    context = {
        'budgets': budgets,
    }
    return render(request, 'budgets/budget_list.html', context)
    
def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    categories = Category.objects.filter(user=request.user, type='EX')  # Only expense categories
    
    if request.method == 'POST':
        new_name = request.POST.get('name', '')
        new_start_date = request.POST.get('start_date', '')
        new_end_date = request.POST.get('end_date', '')

        budget.name = new_name
        budget.start_date = new_start_date
        budget.end_date = new_end_date
        budget.save()

        messages.success(request, "Budget updated successfully!")
        return redirect('budget_list')
        
    context = {
        'budget': budget,
        'categories': categories,
    }
    
    return render(request, 'budgets/budget_edit.html', context)

def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'budgets/budget_list.html', {'budget': budget})