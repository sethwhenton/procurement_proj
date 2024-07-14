# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, CustomUser, Department, Budget, SelectedItem
from .forms import ItemForm, UserForm, DepartmentForm, BudgetForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Sum

##to convert to excel
import openpyxl
from django.http import HttpResponse
from openpyxl.styles import Font

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
    context = {'user': user}
    return render(request, 'core/delete_user.html',{'user': user})


############### ADMIN NAV ###############

def settings(request):
    return render(request, 'core/settings.html')

def view_all_items(request):
    return render(request, 'core/view_all_items.html')



def select_department(request):
    departments = Department.objects.all()
    return render(request, 'core/items_departments_select.html', {'departments': departments})



def items_per_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    users = CustomUser.objects.filter(department=department)
    selected_items = SelectedItem.objects.filter(user__department=department)

    # Create a dictionary to hold user selections
    user_selections = {}
    item_names = set()
    for user in users:
        user_selected_items = selected_items.filter(user=user)
        user_selections[user.id] = {
            'name': user.name,
            'items': {item.item.name: item.quantity for item in user_selected_items},
            'total_cost': sum(item.quantity * item.item.price for item in user_selected_items)
        }
        for item in user_selected_items:
            item_names.add(item.item.name)

    item_names = sorted(item_names)

    return render(request, 'core/items_per_department.html', {
        'department': department,
        'user_selections': user_selections,
        'item_names': item_names
    })




def view_total_items(request):
    items = Item.objects.all()
    departments = Department.objects.all()

    # Create a dictionary to hold total item quantities per department
    item_quantities_per_department = {item.id: {} for item in items}
    for department in departments:
        for item in items:
            total_quantity = SelectedItem.objects.filter(item=item, user__department=department).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            item_quantities_per_department[item.id][department.id] = total_quantity

    # Calculate total quantity and total cost for each item
    total_quantities = {item.id: sum(item_quantities_per_department[item.id].values()) for item in items}
    total_costs = {item.id: total_quantities[item.id] * item.price for item in items}

    # Calculate the sum of all total costs
    grand_total_cost = sum(total_costs.values())

    return render(request, 'core/total_department_items.html', {
        'items': items,
        'departments': departments,
        'item_quantities_per_department': item_quantities_per_department,
        'total_quantities': total_quantities,
        'total_costs': total_costs,
        'grand_total_cost': grand_total_cost,
    })


def download_excel(request):
    items = Item.objects.all()
    departments = Department.objects.all()

    item_quantities_per_department = {item.id: {} for item in items}
    for department in departments:
        for item in items:
            total_quantity = SelectedItem.objects.filter(item=item, user__department=department).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            item_quantities_per_department[item.id][department.id] = total_quantity

    total_quantities = {item.id: sum(item_quantities_per_department[item.id].values()) for item in items}
    total_costs = {item.id: total_quantities[item.id] * item.price for item in items}
    grand_total_cost = sum(total_costs.values())

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Total Items per Department"

    headers = ["Item"]
    for department in departments:
        headers.append(department.name)
    headers.extend(["Total Quantity", "Price", "Total Cost"])

    ws.append(headers)

    for item in items:
        row = [item.name]
        for department in departments:
            row.append(item_quantities_per_department[item.id][department.id])
        row.extend([total_quantities[item.id], item.price, total_costs[item.id]])
        ws.append(row)

    ws.append([""] * (len(departments) + 3) + ["Total Amount:", grand_total_cost])

    for cell in ws["1:1"]:
        cell.font = Font(bold=True)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=total_items_per_department.xlsx'
    wb.save(response)
    return response




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

