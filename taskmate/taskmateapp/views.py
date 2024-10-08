from django.shortcuts import render, HttpResponse
from django.db.models import Q
from .models import Employee, Department
from .models import Department, Role

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    print(context)
    return render(request, 'all_emp.html',context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dept_id = request.POST['dept']  # Getting selected department id
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        role_id = request.POST['role']  # Getting selected role id
        phone = request.POST['phone']
        hire_date = request.POST['hire_date']

        dept = Department.objects.get(id=dept_id)  # Get Department instance by id
        role = Role.objects.get(id=role_id)  # Get Role instance by id

        newemp = Employee(first_name=first_name, last_name=last_name, dept_id=dept,
                          salary=salary, bonus=bonus, role_id=role, phone=phone,
                          hire_date=hire_date)
        newemp.save()
        return HttpResponse('Employee added successfully!')
    else:
        departments = Department.objects.all()  # Query all departments
        roles = Role.objects.all()  # Query all roles
        return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})
    
    


def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
           emp_to_be_removed = Employee.objects.get(id=emp_id)
           emp_to_be_removed.delete()
           return HttpResponse("Employee is removed successfully!")
        except:
            return HttpResponse("Please enter a valid Employee ID.") 
    emps = Employee.objects.all()
    data = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', data)

def filter_emp(request):
    if request.method == 'POST':
        # Retrieving the form inputs
        name = request.POST.get('name')
        dept_id = request.POST.get('dept')  # Getting selected department
        role_id = request.POST.get('role')  # Getting selected role

        # Initializing the query
        emps = Employee.objects.all()

        # Filtering based on form inputs
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept_id:
            emps = emps.filter(dept_id=dept_id)
        if role_id:
            emps = emps.filter(role_id=role_id)

        # Preparing the context data
        data = {
            'emps': emps
        }

        return render(request, 'all_emp.html', data)

    elif request.method == 'GET':
        # Handle GET request by loading the departments and roles for the filter form
        departments = Department.objects.all()
        roles = Role.objects.all()

        data = {
            'departments': departments,
            'roles': roles,
        }

        return render(request, 'filter_emp.html', data)

    else:
        return HttpResponse("An Exception Occurred!")

