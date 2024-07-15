from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, CustomUser, Department, Budget, SelectedItem, Company
from .forms import ItemForm, UserForm, DepartmentForm, BudgetForm, CompanyForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Sum
from django.core.serializers.json import DjangoJSONEncoder


import openpyxl
from django.http import HttpResponse
from openpyxl.styles import Font

from collections import defaultdict

from django.shortcuts import render


def get_selected_company(request):
    company_id = request.session.get('selected_company')
    if company_id:
        return get_object_or_404(Company, id=company_id)
    return None

def main_home(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        company_id = request.POST.get('company')
        request.session['selected_company'] = company_id
        return redirect('home')
    return render(request, 'core/main_home.html', {'companies': companies})

def add_new_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_home')
    else:
        form = CompanyForm()
    return render(request, 'core/add_new_company.html', {'form': form})

def update_company_name(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('main_home')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'core/update_company_name.html', {'form': form})

def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        company.delete()
        return redirect('main_home')
    return render(request, 'core/delete_company.html', {'company': company})

def home(request):
    return render(request, 'core/home.html')

def admin_home(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    return render(request, 'core/admin_home.html', {'company': company})

def item_home(request):
    return render(request, 'core/item_home.html')

def user_home(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    users = CustomUser.objects.filter(company=company)
    if request.method == 'POST':
        user_id = request.POST.get('user')
        user = get_object_or_404(CustomUser, id=user_id)
        request.session['selected_user'] = user_id
        return redirect('select_item')
    return render(request, 'core/user_home.html', {'users': users})

def select_item(request):
    user_id = request.session.get('selected_user')
    user = get_object_or_404(CustomUser, id=user_id)
    items = Item.objects.filter(company=user.company)
    selected_items = SelectedItem.objects.filter(user=user)
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
        user_id = request.session.get('selected_user')
        if not user_id:
            return JsonResponse({'status': 'failed', 'message': 'No user selected'}, status=400)
        user = get_object_or_404(CustomUser, id=user_id)
        selected_items = json.loads(request.POST.get('selected_items'))
        SelectedItem.objects.filter(user=user).delete()
        for item in selected_items:
            item_obj = get_object_or_404(Item, id=item['itemId'])
            SelectedItem.objects.create(user=user, item=item_obj, quantity=int(item['quantity']))
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=405)

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

def item_list(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    items = Item.objects.filter(company=company)
    return render(request, 'core/item_list.html', {'items': items})


def add_item(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.company = company
            item.save()
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

def user_list(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    users = CustomUser.objects.filter(company=company)
    return render(request, 'core/user_list.html', {'users': users})

def add_user(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.company = company
            user.save()
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

def settings(request):
    return render(request, 'core/settings.html')

def select_department(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    departments = Department.objects.filter(company=company)
    return render(request, 'core/items_departments_select.html', {'departments': departments})

def items_per_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    users = CustomUser.objects.filter(department=department)
    selected_items = SelectedItem.objects.filter(user__department=department)
    
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
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    items = Item.objects.filter(company=company)
    departments = Department.objects.filter(company=company)

    item_quantities_per_department = {item.id: {} for item in items}
    for department in departments:
        for item in items:
            total_quantity = SelectedItem.objects.filter(item=item, user__department=department).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
            item_quantities_per_department[item.id][department.id] = total_quantity

    total_quantities = {item.id: sum(item_quantities_per_department[item.id].values()) for item in items}
    total_costs = {item.id: total_quantities[item.id] * item.price for item in items}
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
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    items = Item.objects.filter(company=company)
    departments = Department.objects.filter(company=company)

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

def view_budgets(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    budgets = Budget.objects.filter(company=company)
    return render(request, 'core/view_budgets.html', {'budgets': budgets})

def add_budget(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.company = company
            budget.save()
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

def department_list(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    departments = Department.objects.filter(company=company)
    return render(request, 'core/department_list.html', {'departments': departments})

def add_department(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.company = company
            department.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'core/add_department.html', {'form': form})

def edit_departments(request):
    company = get_selected_company(request)
    if not company:
        return redirect('main_home')
    departments = Department.objects.filter(company=company)
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

def view_all_items(request):
    items = Item.objects.all()
    return render(request, 'core/view_all_items.html', {'items': items})
