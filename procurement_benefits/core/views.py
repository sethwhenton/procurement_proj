# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, CustomUser, Department, Budget, SelectedItem
from .forms import ItemForm, UserForm, DepartmentForm, BudgetForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from collections import defaultdict
# Admin Home
# core/views.py
from django.shortcuts import render

############### NAVIGATIONS #####################

def home(request):
    return render(request, 'core/home.html')

def admin_home(request):
    return render(request, 'core/admin_home.html')

# def user_home(request):
#     return render(request, 'core/user_home.html')
def item_home(request):
    return render(request, 'core/item_home.html')


# def user_home(request):
#     departments = Department.objects.all()  # Retrieve all departments
#     users = CustomUser.objects.all()        # Retrieve all users
#     return render(request, 'core/user_home.html', {'departments': departments, 'users': users})



########## USER SELECT ITEM ################


def user_home(request):
    users = CustomUser.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        user = get_object_or_404(CustomUser, id=user_id)
        request.session['selected_user'] = user_id
        return redirect('select_item')
    return render(request, 'core/user_home.html', {'users': users})

# core/views.py




from django.core.serializers.json import DjangoJSONEncoder

def select_item(request):
    user_id = request.session.get('selected_user')
    user = get_object_or_404(CustomUser, id=user_id)
    items = Item.objects.all()
    selected_items = SelectedItem.objects.filter(user=user)

    # Convert the selected items to a JSON serializable format
    selected_items_data = [
        {
            'id': item.item.id,
            'name': item.item.name,
            'quantity': item.quantity,
            'total': float(item.quantity * item.item.price)
        } for item in selected_items
    ]
    
    return render(request, 'core/select_item.html', {
        'user': user,
        'items': items,
        'selected_items_data': json.dumps(selected_items_data, cls=DjangoJSONEncoder)
    })



@csrf_exempt
def save_selection(request):
    if request.method == 'POST':
        print("Received POST request")
        user_id = request.session.get('selected_user')
        if not user_id:
            print("No user selected")
            return JsonResponse({'status': 'failed', 'message': 'No user selected'}, status=400)

        user = get_object_or_404(CustomUser, id=user_id)
        selected_items = json.loads(request.POST.get('selected_items'))
        print(f"Selected items: {selected_items}")

        # Clear previous selections
        SelectedItem.objects.filter(user=user).delete()

        # Save new selections
        for item in selected_items:
            item_obj = get_object_or_404(Item, id=item['itemId'])
            SelectedItem.objects.create(user=user, item=item_obj, quantity=int(item['quantity']))
        
        print("Selections saved successfully")
        return JsonResponse({'status': 'success'})

    print("Invalid request method")
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=405)


# def summary_checkout(request):
#     user_id = request.session.get('selected_user')
#     user = CustomUser.objects.get(id=user_id)
#     selected_items = SelectedItem.objects.filter(user=user)
    
#     # Calculate the total cost for each selected item
#     for selected_item in selected_items:
#         selected_item.total = selected_item.quantity * selected_item.item.price

#     return render(request, 'core/summary_checkout.html', {'user': user, 'selected_items': selected_items})

def summary_checkout(request, user_id=None):
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user_id = request.session.get('selected_user')
        user = get_object_or_404(CustomUser, id=user_id)
        
    selected_items = SelectedItem.objects.filter(user=user)
    
    for selected_item in selected_items:
        selected_item.total = selected_item.quantity * selected_item.item.price
    
    total_cost = sum(item.total for item in selected_items)
    
    return render(request, 'core/summary_checkout.html', {
        'user': user,
        'selected_items': selected_items,
        'total_cost': total_cost
    })


def user_selected_items(request):
    user_id = request.session.get('selected_user')
    user = CustomUser.objects.get(id=user_id)
    selected_items = SelectedItem.objects.filter(user=user)
    return render(request, 'core/user_selected_items.html', {'user': user, 'selected_items': selected_items})



############# ITEMS #####################

def item_list(request):
    items = Item.objects.all()
    return render(request, 'core/item_list.html', {'items': items})


def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'core/add_item.html', {'form': form})

def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'core/update_item.html', {'form': form})

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'core/delete_item.html', {'item': item})



########## USERS ########################
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'core/user_list.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'core/add_user.html', {'form': form})

def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'core/update_user.html', {'form': form})

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'core/delete_user.html', {'user': user})


############### ADMIN NAV ###############

def settings(request):
    return render(request, 'core/settings.html')


############### BUDGET #####################


def view_budgets(request):
    budgets = Budget.objects.all()
    return render(request, 'core/view_budgets.html', {'budgets': budgets})

def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_budgets')
    else:
        form = BudgetForm()
    return render(request, 'core/add_budget.html', {'form': form})


def update_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('view_budgets')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'core/update_budget.html', {'form': form})


def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    if request.method == 'POST':
        budget.delete()
        return redirect('view_budgets')
    return render(request, 'core/delete_budget.html', {'budget': budget})


########## DEPARTMENTS ################
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'core/department_list.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'core/add_department.html', {'form': form})

def add_departments(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Department.objects.create(name=name)
        return redirect('edit_departments')
    return render(request, 'core/add_department.html')


def view_all_items(request):
    items = Item.objects.all()
    departments = Department.objects.all()
    return render(request, 'core/view_all_items.html', {'items': items, 'departments': departments})



def edit_departments(request):
    departments = Department.objects.all()
    return render(request, 'core/edit_departments.html', {'departments': departments})


def update_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'core/update_department.html', {'form': form})

def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    return render(request, 'core/delete_department.html', {'department': department})

