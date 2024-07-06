# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, CustomUser, Department, Budget
from .forms import ItemForm, UserForm, DepartmentForm, BudgetForm

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


def user_home(request):
    departments = Department.objects.all()  # Retrieve all departments
    users = CustomUser.objects.all()        # Retrieve all users
    return render(request, 'core/user_home.html', {'departments': departments, 'users': users})

########## USER SELECT ITEM ################


def select_item(request):
    # Logic to filter items based on user's department
    items = Item.objects.all()  # Replace with actual filtering logic
    return render(request, 'core/select_item.html', {'items': items})

def summary_checkout(request):
    # Logic to retrieve selected items
    selected_items = request.session.get('selected_items', [])  # Assuming selected items are stored in session
    return render(request, 'core/summary_checkout.html', {'selected_items': selected_items})



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

