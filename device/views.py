from django.shortcuts import render,redirect,reverse
from . import forms,models
import random
from django.db.models import Sum
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from .models import Userip
from django.contrib.auth.models import User


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    
    def get_ip(request):
        adress = request.META.get('HTTP_X_FORWARDED_FOR')
        if adress:
            ip = adress.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_ip(request)
    u = Userip(userip=ip)
    print(ip)
    result = Userip.objects.filter(Q(userip__icontains=ip))
    if len(result)==1:
        print("user exist")
    elif len(result)>1:
        print("user exist more ..")
    else:
        u.save()
        print("user is unique")
    
    count = Userip.objects.all().count
    print(count)

    return render(request,'device/index.html',{'count':count})


#for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'device/customerclick.html')

#for showing signup/login button for mechanics
def mechanicsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'device/mechanicsclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'device/customersignup.html',context=mydict)


# def mechanic_signup_view(request):
#     userForm=forms.MechanicUserForm()
#     mechanicForm=forms.MechanicForm()
#     mydict={'userForm':userForm,'mechanicForm':mechanicForm}
#     if request.method=='POST':
#         userForm=forms.MechanicUserForm(request.POST)
#         mechanicForm=forms.MechanicForm(request.POST,request.FILES)
#         if userForm.is_valid() and mechanicForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             mechanic=mechanicForm.save(commit=False)
#             mechanic.user=user
#             mechanic.save()
#             my_mechanic_group = Group.objects.get_or_create(name='ENGINEER')
#             my_mechanic_group[0].user_set.add(user)
#         return HttpResponseRedirect('mechaniclogin')
#     return render(request,'device/mechanicsignup.html',context=mydict)


# #for checking user customer, mechanic or admin(by sumit)
# def is_customer(user):
#     return user.groups.filter(name='CUSTOMER').exists()
# def is_mechanic(user):
#     return user.groups.filter(name='ENGINEER').exists()


# def afterlogin_view(request):
#     if is_customer(request.user):
#         return redirect('customer-dashboard')
#     elif is_mechanic(request.user):
#         accountapproval=models.Mechanic.objects.all().filter(user_id=request.user.id,status=True)
#         if accountapproval:
#             return redirect('mechanic-dashboard')
#         else:
#             return render(request,'device/mechanic_wait_for_approval.html')
#     else:
#         return redirect('admin-dashboard')



# #============================================================================================
# # ADMIN RELATED views start
# #============================================================================================

# @login_required(login_url='adminlogin')
# def admin_dashboard_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     dict={
#     'total_customer':models.Customer.objects.all().count(),
#     'total_mechanic':models.Mechanic.objects.all().count(),
#     'total_request':models.Request.objects.all().count(),
#     'total_feedback':models.Feedback.objects.all().count(),
#     'data':zip(customers,enquiry),
#     }
#     return render(request,'device/admin_dashboard.html',context=dict)


# @login_required(login_url='adminlogin')
# def admin_customer_view(request):
#     customers=models.Customer.objects.all()    
#     return render(request,'device/admin_customer.html',{'customers':customers})

# @login_required(login_url='adminlogin')
# def admin_view_customer_view(request):
#     customers=models.Customer.objects.all()
#     return render(request,'device/admin_view_customer.html',{'customers':customers})


# @login_required(login_url='adminlogin')
# def delete_customer_view(request,pk):
#     customer=models.Customer.objects.get(id=pk)
#     user=models.User.objects.get(id=customer.user_id)
#     user.delete()
#     customer.delete()
#     return redirect('admin-view-customer')


# @login_required(login_url='adminlogin')
# def update_customer_view(request,pk):
#     customer=models.Customer.objects.get(id=pk)
#     user=models.User.objects.get(id=customer.user_id)
#     userForm=forms.CustomerUserForm(instance=user)
#     customerForm=forms.CustomerForm(request.FILES,instance=customer)
#     mydict={'userForm':userForm,'customerForm':customerForm}
#     if request.method=='POST':
#         userForm=forms.CustomerUserForm(request.POST,instance=user)
#         customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
#         if userForm.is_valid() and customerForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             customerForm.save()
#             return redirect('admin-view-customer')
#     return render(request,'device/update_customer.html',context=mydict)


# @login_required(login_url='adminlogin')
# def admin_add_customer_view(request):
#     userForm=forms.CustomerUserForm()
#     customerForm=forms.CustomerForm()
#     mydict={'userForm':userForm,'customerForm':customerForm}
#     if request.method=='POST':
#         userForm=forms.CustomerUserForm(request.POST)
#         customerForm=forms.CustomerForm(request.POST,request.FILES)
#         if userForm.is_valid() and customerForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             customer=customerForm.save(commit=False)
#             customer.user=user
#             customer.save()
#             my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
#             my_customer_group[0].user_set.add(user)
#         return HttpResponseRedirect('/admin-view-customer')
#     return render(request,'device/admin_add_customer.html',context=mydict)


# @login_required(login_url='adminlogin')
# def admin_view_customer_enquiry_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     return render(request,'device/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})


# @login_required(login_url='adminlogin')
# def admin_view_customer_invoice_view(request):
#     enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
#     print(enquiry)
#     customers=[]
#     for enq in enquiry:
#         print(enq)
#         customer=models.Customer.objects.get(id=enq['customer_id'])
#         customers.append(customer)
#     return render(request,'device/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

# @login_required(login_url='adminlogin')
# def admin_mechanic_view(request):
#     mechanics=models.Mechanic.objects.all()
#     return render(request,'device/admin_mechanic.html',{'mechanics': mechanics})


# @login_required(login_url='adminlogin')
# def admin_approve_mechanic_view(request):
#     mechanics=models.Mechanic.objects.all().filter(status=False)
#     return render(request,'device/admin_approve_mechanic.html',{'mechanics':mechanics})

# @login_required(login_url='adminlogin')
# def approve_mechanic_view(request,pk):
#     mechanicSalary=forms.MechanicSalaryForm()
#     if request.method=='POST':
#         mechanicSalary=forms.MechanicSalaryForm(request.POST)
#         if mechanicSalary.is_valid():
#             mechanic=models.Mechanic.objects.get(id=pk)
#             mechanic.salary=mechanicSalary.cleaned_data['salary']
#             mechanic.status=True
#             mechanic.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-approve-mechanic')
#     return render(request,'device/admin_approve_mechanic_details.html',{'mechanicSalary':mechanicSalary})


# @login_required(login_url='adminlogin')
# def delete_mechanic_view(request,pk):
#     mechanic=models.Mechanic.objects.get(id=pk)
#     user=models.User.objects.get(id=mechanic.user_id)
#     user.delete()
#     mechanic.delete()
#     return redirect('admin-approve-mechanic')


# @login_required(login_url='adminlogin')
# def admin_add_mechanic_view(request):
#     userForm=forms.MechanicUserForm()
#     mechanicForm=forms.MechanicForm()
#     mechanicSalary=forms.MechanicSalaryForm()
#     mydict={'userForm':userForm,'mechanicForm':mechanicForm,'mechanicSalary':mechanicSalary}
#     if request.method=='POST':
#         userForm=forms.MechanicUserForm(request.POST)
#         mechanicForm=forms.MechanicForm(request.POST,request.FILES)
#         mechanicSalary=forms.MechanicSalaryForm(request.POST)
#         if userForm.is_valid() and mechanicForm.is_valid() and mechanicSalary.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             mechanic=mechanicForm.save(commit=False)
#             mechanic.user=user
#             mechanic.status=True
#             mechanic.salary=mechanicSalary.cleaned_data['salary']
#             mechanic.save()
#             my_mechanic_group = Group.objects.get_or_create(name='ENGINEER')
#             my_mechanic_group[0].user_set.add(user)
#             return HttpResponseRedirect('admin-view-mechanic')
#         else:
#             print('problem in form')
#     return render(request,'device/admin_add_mechanic.html',context=mydict)


# @login_required(login_url='adminlogin')
# def admin_view_mechanic_view(request):
#     mechanics=models.Mechanic.objects.all()
#     return render(request,'device/admin_view_mechanic.html',{'mechanics':mechanics})


# @login_required(login_url='adminlogin')
# def delete_mechanic_view(request,pk):
#     mechanic=models.Mechanic.objects.get(id=pk)
#     user=models.User.objects.get(id=mechanic.user_id)
#     user.delete()
#     mechanic.delete()
#     return redirect('admin-view-mechanic')


# @login_required(login_url='adminlogin')
# def update_mechanic_view(request,pk):
#     mechanic=models.Mechanic.objects.get(id=pk)
#     user=models.User.objects.get(id=mechanic.user_id)
#     userForm=forms.MechanicUserForm(instance=user)
#     mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
#     mydict={'userForm':userForm,'mechanicForm':mechanicForm}
#     if request.method=='POST':
#         userForm=forms.MechanicUserForm(request.POST,instance=user)
#         mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
#         if userForm.is_valid() and mechanicForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             mechanicForm.save()
#             return redirect('admin-view-mechanic')
#     return render(request,'device/update_mechanic.html',context=mydict)

# @login_required(login_url='adminlogin')
# def admin_view_mechanic_salary_view(request):
#     mechanics=models.Mechanic.objects.all()
#     return render(request,'device/admin_view_mechanic_salary.html',{'mechanics':mechanics})

# @login_required(login_url='adminlogin')
# def update_salary_view(request,pk):
#     mechanicSalary=forms.MechanicSalaryForm()
#     if request.method=='POST':
#         mechanicSalary=forms.MechanicSalaryForm(request.POST)
#         if mechanicSalary.is_valid():
#             mechanic=models.Mechanic.objects.get(id=pk)
#             mechanic.salary=mechanicSalary.cleaned_data['salary']
#             mechanic.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-view-mechanic-salary')
#     return render(request,'device/admin_approve_mechanic_details.html',{'mechanicSalary':mechanicSalary})


# @login_required(login_url='adminlogin')
# def admin_request_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     return render(request,'device/admin_request.html',{'data':zip(customers,enquiry)})

# @login_required(login_url='adminlogin')
# def admin_view_request_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     return render(request,'device/admin_view_request.html',{'data':zip(customers,enquiry)})


# @login_required(login_url='adminlogin')
# def change_status_view(request,pk):
#     adminenquiry=forms.AdminApproveRequestForm()
#     if request.method=='POST':
#         adminenquiry=forms.AdminApproveRequestForm(request.POST)
#         if adminenquiry.is_valid():
#             enquiry_x=models.Request.objects.get(id=pk)
#             enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
#             enquiry_x.cost=adminenquiry.cleaned_data['cost']
#             enquiry_x.status=adminenquiry.cleaned_data['status']
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-view-request')
#     return render(request,'device/admin_approve_request_details.html',{'adminenquiry':adminenquiry})


# @login_required(login_url='adminlogin')
# def admin_delete_request_view(request,pk):
#     requests=models.Request.objects.get(id=pk)
#     requests.delete()
#     return redirect('admin-view-request')



# @login_required(login_url='adminlogin')
# def admin_add_request_view(request):
#     enquiry=forms.RequestForm()
#     adminenquiry=forms.AdminRequestForm()
#     mydict={'enquiry':enquiry,'adminenquiry':adminenquiry}
#     if request.method=='POST':
#         enquiry=forms.RequestForm(request.POST)
#         adminenquiry=forms.AdminRequestForm(request.POST)
#         if enquiry.is_valid() and adminenquiry.is_valid():
#             enquiry_x=enquiry.save(commit=False)
#             enquiry_x.customer=adminenquiry.cleaned_data['customer']
#             enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
#             enquiry_x.cost=adminenquiry.cleaned_data['cost']
#             enquiry_x.status='Approved'
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('admin-view-request')
#     return render(request,'device/admin_add_request.html',context=mydict)

# @login_required(login_url='adminlogin')
# def admin_approve_request_view(request):
#     enquiry=models.Request.objects.all().filter(status='Pending')
#     return render(request,'device/admin_approve_request.html',{'enquiry':enquiry})

# @login_required(login_url='adminlogin')
# def approve_request_view(request,pk):
#     adminenquiry=forms.AdminApproveRequestForm()
#     if request.method=='POST':
#         adminenquiry=forms.AdminApproveRequestForm(request.POST)
#         if adminenquiry.is_valid():
#             enquiry_x=models.Request.objects.get(id=pk)
#             enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
#             enquiry_x.cost=adminenquiry.cleaned_data['cost']
#             enquiry_x.status=adminenquiry.cleaned_data['status']
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-approve-request')
#     return render(request,'device/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




# @login_required(login_url='adminlogin')
# def admin_view_service_cost_view(request):
#     enquiry=models.Request.objects.all().order_by('-id')
#     customers=[]
#     for enq in enquiry:
#         customer=models.Customer.objects.get(id=enq.customer_id)
#         customers.append(customer)
#     print(customers)
#     return render(request,'device/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


# @login_required(login_url='adminlogin')
# def update_cost_view(request,pk):
#     updateCostForm=forms.UpdateCostForm()
#     if request.method=='POST':
#         updateCostForm=forms.UpdateCostForm(request.POST)
#         if updateCostForm.is_valid():
#             enquiry_x=models.Request.objects.get(id=pk)
#             enquiry_x.cost=updateCostForm.cleaned_data['cost']
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/admin-view-service-cost')
#     return render(request,'device/update_cost.html',{'updateCostForm':updateCostForm})



# @login_required(login_url='adminlogin')
# def admin_mechanic_attendance_view(request):
#     return render(request,'device/admin_mechanic_attendance.html')


# @login_required(login_url='adminlogin')
# def admin_take_attendance_view(request):
#     mechanics=models.Mechanic.objects.all().filter(status=True)
#     aform=forms.AttendanceForm()
#     if request.method=='POST':
#         form=forms.AttendanceForm(request.POST)
#         if form.is_valid():
#             Attendances=request.POST.getlist('present_status')
#             date=form.cleaned_data['date']
#             for i in range(len(Attendances)):
#                 AttendanceModel=models.Attendance()
                
#                 AttendanceModel.date=date
#                 AttendanceModel.present_status=Attendances[i]
#                 print(mechanics[i].id)
#                 print(int(mechanics[i].id))
#                 mechanic=models.Mechanic.objects.get(id=int(mechanics[i].id))
#                 AttendanceModel.mechanic=mechanic
#                 AttendanceModel.save()
#             return redirect('admin-view-attendance')
#         else:
#             print('form invalid')
#     return render(request,'device/admin_take_attendance.html',{'mechanics':mechanics,'aform':aform})

# @login_required(login_url='adminlogin')
# def admin_view_attendance_view(request):
#     form=forms.AskDateForm()
#     if request.method=='POST':
#         form=forms.AskDateForm(request.POST)
#         if form.is_valid():
#             date=form.cleaned_data['date']
#             attendancedata=models.Attendance.objects.all().filter(date=date)
#             mechanicdata=models.Mechanic.objects.all().filter(status=True)
#             mylist=zip(attendancedata,mechanicdata)
#             return render(request,'device/admin_view_attendance_page.html',{'mylist':mylist,'date':date})
#         else:
#             print('form invalid')
#     return render(request,'device/admin_view_attendance_ask_date.html',{'form':form})

# @login_required(login_url='adminlogin')
# def admin_report_view(request):
#     reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
#     dict={
#         'reports':reports,
#     }
#     return render(request,'device/admin_report.html',context=dict)


# @login_required(login_url='adminlogin')
# def admin_feedback_view(request):
#     feedback=models.Feedback.objects.all().order_by('-id')
#     return render(request,'device/admin_feedback.html',{'feedback':feedback})

# #============================================================================================
# # ADMIN RELATED views END
# #============================================================================================


# #============================================================================================
# # CUSTOMER RELATED views start
# #============================================================================================

# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_dashboard_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     work_in_progress=models.Request.objects.all().filter(customer_id=customer.id,status='Repairing').count()
#     work_completed=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).count()
#     new_request_made=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Pending") | Q(status="Approved")).count()
#     bill=models.Request.objects.all().filter(customer_id=customer.id).filter(Q(status="Repairing Done") | Q(status="Released")).aggregate(Sum('cost'))
#     enquiries=models.Request.objects.all().filter(customer_id=customer.id)
#     print(bill)
#     dict={
#     'work_in_progress':work_in_progress,
#     'work_completed':work_completed,
#     'new_request_made':new_request_made,
#     'bill':bill['cost__sum'],
#     'customer':customer,
#     'enquiries': enquiries
#     }
#     return render(request,'device/customer_dashboard.html',context=dict)

# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_request_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
#     return render(request,'device/customer_request.html',{'customer':customer,'enquiries':enquiries})

# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_view_request_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
#     return render(request,'device/customer_view_request.html',{'customer':customer,'enquiries':enquiries})


# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_delete_request_view(request,pk):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     enquiry=models.Request.objects.get(id=pk)
#     enquiry.delete()
#     return redirect('customer-view-request')

# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_view_approved_request_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
#     return render(request,'device/customer_view_approved_request.html',{'customer':customer,'enquiries':enquiries})

# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_view_approved_request_invoice_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
#     return render(request,'device/customer_view_approved_request_invoice.html',{'customer':customer,'enquiries':enquiries})



# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_add_request_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     enquiry=forms.RequestForm()
#     if request.method=='POST':
#         enquiry=forms.RequestForm(request.POST)
#         if enquiry.is_valid():
#             customer=models.Customer.objects.get(user_id=request.user.id)
#             enquiry_x=enquiry.save(commit=False)
#             enquiry_x.customer=customer
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('customer-dashboard')
#     return render(request,'device/customer_add_request.html',{'enquiry':enquiry,'customer':customer})


# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_profile_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     return render(request,'device/customer_profile.html',{'customer':customer})


# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def edit_customer_profile_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     user=models.User.objects.get(id=customer.user_id)
#     userForm=forms.CustomerUserForm(instance=user)
#     customerForm=forms.CustomerForm(request.FILES,instance=customer)
#     mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
#     if request.method=='POST':
#         userForm=forms.CustomerUserForm(request.POST,instance=user)
#         customerForm=forms.CustomerForm(request.POST,instance=customer)
#         if userForm.is_valid() and customerForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             customerForm.save()
#             return HttpResponseRedirect('customer-profile')
#     return render(request,'device/edit_customer_profile.html',context=mydict)


# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_invoice_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
#     return render(request,'device/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


# @login_required(login_url='customerlogin')
# @user_passes_test(is_customer)
# def customer_feedback_view(request):
#     customer=models.Customer.objects.get(user_id=request.user.id)
#     feedback=forms.FeedbackForm()
#     if request.method=='POST':
#         feedback=forms.FeedbackForm(request.POST)
#         if feedback.is_valid():
#             feedback.save()
#         else:
#             print("form is invalid")
#         return render(request,'device/feedback_sent_by_customer.html',{'customer':customer})
#     return render(request,'device/customer_feedback.html',{'feedback':feedback,'customer':customer})
# #============================================================================================
# # CUSTOMER RELATED views END
# #============================================================================================






# #============================================================================================
# # MECHANIC RELATED views start
# #============================================================================================


# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
# def mechanic_dashboard_view(request):
#     mechanic=models.Mechanic.objects.get(user_id=request.user.id)
#     work_in_progress=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Repairing').count()
#     work_completed=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Repairing Done').count()
#     new_work_assigned=models.Request.objects.all().filter(mechanic_id=mechanic.id,status='Approved').count()
#     works=models.Request.objects.all().filter(mechanic_id=mechanic.id)

#     dict={
#     'work_in_progress':work_in_progress,
#     'work_completed':work_completed,
#     'new_work_assigned':new_work_assigned,
#     'salary':mechanic.salary,
#     'engineer':mechanic,
#     'works': works,
#     }
#     return render(request,'device/mechanic_dashboard.html',context=dict)

# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
# def mechanic_work_assigned_view(request):
#     mechanic=models.Mechanic.objects.get(user_id=request.user.id)
#     works=models.Request.objects.all().filter(mechanic_id=mechanic.id)
#     return render(request,'device/mechanic_work_assigned.html',{'works':works,'engineer':mechanic})


# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
# def mechanic_update_status_view(request,pk):
#     mechanic=models.Mechanic.objects.get(user_id=request.user.id)
#     updateStatus=forms.MechanicUpdateStatusForm()
#     if request.method=='POST':
#         updateStatus=forms.MechanicUpdateStatusForm(request.POST)
#         if updateStatus.is_valid():
#             enquiry_x=models.Request.objects.get(id=pk)
#             enquiry_x.status=updateStatus.cleaned_data['status']
#             enquiry_x.save()
#         else:
#             print("form is invalid")
#         return HttpResponseRedirect('/mechanic-work-assigned')
#     return render(request,'device/mechanic_update_status.html',{'updateStatus':updateStatus,'engineer':mechanic})

# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
# def mechanic_attendance_view(request):
#     mechanic=models.Mechanic.objects.get(user_id=request.user.id)
#     attendaces=models.Attendance.objects.all().filter(mechanic=mechanic)
#     return render(request,'device/mechanic_view_attendance.html',{'attendaces':attendaces,'engineer':mechanic})





# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
# def mechanic_feedback_view(request):
#     mechanic=models.Mechanic.objects.get(user_id=request.user.id)
#     feedback=forms.FeedbackForm()
#     if request.method=='POST':
#         feedback=forms.FeedbackForm(request.POST)
#         if feedback.is_valid():
#             feedback.save()
#         else:
#             print("form is invalid")
#         return render(request,'device/feedback_sent.html',{'engineer':mechanic})
#     return render(request,'device/mechanic_feedback.html',{'feedback':feedback,'engineer':mechanic})

# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
# def mechanic_salary_view(request):
#     mechanic=models.Mechanic.objects.get(user_id=request.user.id)
#     workdone=models.Request.objects.all().filter(mechanic_id=mechanic.id).filter(Q(status="Repairing Done") | Q(status="Released"))
#     reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
#     dict={
#         'reports':reports,
#         'engineer':mechanic,
#         'workdone':workdone,
#         'data':zip(workdone,reports),
#     }
#     return render(request,'device/mechanic_salary.html',context=dict)

# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
# def mechanic_profile_view(request):
#     mechanic=models.Mechanic.objects.get(user_id=request.user.id)
#     return render(request,'device/mechanic_profile.html',{'engineer':mechanic})

# @login_required(login_url='mechaniclogin')
# @user_passes_test(is_mechanic)
# def edit_mechanic_profile_view(request):
#     mechanic=models.Mechanic.objects.get(user_id=request.user.id)
#     user=models.User.objects.get(id=mechanic.user_id)
#     userForm=forms.MechanicUserForm(instance=user)
#     mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
#     mydict={'userForm':userForm,'mechanicForm':mechanicForm,'engineer':mechanic}
#     if request.method=='POST':
#         userForm=forms.MechanicUserForm(request.POST,instance=user)
#         mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
#         if userForm.is_valid() and mechanicForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             mechanicForm.save()
#             return redirect('mechanic-profile')
#     return render(request,'device/edit_mechanic_profile.html',context=mydict)






# #============================================================================================
# # MECHANIC RELATED views start
# #============================================================================================





def aboutus_view(request):

    def get_ip(request):
        adress = request.META.get('HTTP_X_FORWARDED_FOR')
        if adress:
            ip = adress.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_ip(request)
    u = Userip(userip=ip)
    print(ip)
    result = Userip.objects.filter(Q(userip__icontains=ip))
    if len(result)==1:
        print("user exist")
    elif len(result)>1:
        print("user exist more ..")
    else:
        u.save()
        print("user is unique")
    
    count = Userip.objects.all().count
    print(count)
    return render(request,'device/aboutus.html',{'count':count})


def errorpage(request):
    return render(request,'device/error.html')

# # def contactus_view(request):
# #     sub = forms.ContactusForm()
# #     if request.method == 'POST':
# #         sub = forms.ContactusForm(request.POST)
# #         if sub.is_valid():
# #             email = sub.cleaned_data['Email']
# #             name=sub.cleaned_data['Name']
# #             message = sub.cleaned_data['Message']
# #             send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
# #             return render(request, 'device/contactussuccess.html')
# #     return render(request, 'device/contactus.html', {'form':sub})


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        subject = request.POST['subject']
        token_id = random.randrange(1, 10000)
        message_body = 'Dear Admin,' + '\n' + 'There is an Query from ' + name  + '\n\n' + 'Message: ' + message + '\n\n' + 'Token Id: #' + str(token_id) + '\n'+ 'Email: ' + email + '\n' +  'Phone: ' + phone + '\n' 
        email_subject = 'You have a new message from #' + str(token_id) + ' regarding ' + subject
        email_subjectUser = 'Ticket Raised - #'+ str(token_id) + '- Regarding ' + subject
        message_bodyUser = 'Dear ' +name+',' + '\n' + 'Thank You, for Contacting Us! Your, Query Has Been Raised' + '\n' + 'Your Reference/Token Id - #'+ str(token_id) +'.'+'\n' + 'Your Query is :'+message + '\n\n\n\n\n' + 'With Regard,' + '\n' + 'ApnaEngineer Support Team' + '\n' + 'Feel Free To Contact Again' + '\n' + 'Contact No.: ' + '+91 9519291313' + '\n' + '\t\t\t' +  '+91 9519722864' + '\n' + '\t\t\t'+'+919235566533' + '\n' + 'Also Mail On: ' + 'service4u.apnaengineer@gmail.com' + '\n\n' + 'LogOn To Our Website : '+ 'www.apnaengineer.com' + '\n\n' + 'JAI HIND !!'

        
        admin_email ='service4u.apnaengineer@gmail.com'
        send_mail(
            email_subject,
            message_body,
            '',
            [admin_email],
            fail_silently=False,
        )

        send_mail(
            email_subjectUser,
            message_bodyUser,
            '',
            [email],
            fail_silently=False,
        )
        messages.success(request, ' Thank You For Contacting Us . We Will Get Back To You Shortly')
        return redirect('contact')

    def get_ip(request):
        adress = request.META.get('HTTP_X_FORWARDED_FOR')
        if adress:
            ip = adress.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    ip = get_ip(request)
    u = Userip(userip=ip)
    print(ip)
    result = Userip.objects.filter(Q(userip__icontains=ip))
    if len(result)==1:
        print("user exist")
    elif len(result)>1:
        print("user exist more ..")
    else:
        u.save()
        print("user is unique")

    count = Userip.objects.all().count
    print(count)
    return render(request, 'device/contactus.html',{'count':count})