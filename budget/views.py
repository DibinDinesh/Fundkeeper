from django.shortcuts import render,redirect

from django.views.generic import View

from budget.models import Expense,Income

from budget.forms import ExpenseForm,IncomeForm,RegistrationForm,LoginForm

from django.contrib import messages

from django.utils import timezone

from django.db.models import Sum

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from budget.decorators import signin_required

from django.utils.decorators import method_decorator





@method_decorator(signin_required,name="dispatch")
class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):
        
        form_instance=ExpenseForm()

        qs=Expense.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"expense_add.html",{"form":form_instance,"data":qs})
    

    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object=request.user

            form_instance.save()

            messages.success(request,"expense has been created !!")

            print("expense has been created")

            return redirect("expense-add")
        
        else:

            messages.error(request,"error")

            return render(request,"expense_add.html",{"form":form_instance})
        

@method_decorator(signin_required,name="dispatch")
class ExpenseUpdateView(View):

     def get(self,request,*args,**kwargs):
         
        id=kwargs.get("pk")

        expense_object=Expense.objects.get(id=id)
     
        form_instance=ExpenseForm(instance=expense_object)

        return render(request,"expense_edit.html",{"form":form_instance})
     
     def post(self,request,*args,**kwargs): 
    
         id=kwargs.get("pk")

         expense_object=Expense.objects.get(id=id)

         form_instance=ExpenseForm(instance=expense_object,data=request.POST)

         if form_instance.is_valid():
              
              form_instance.save()

              messages.success(request,"expense changed")

              return redirect("expense-add")
         else:
              
              messages.error(request,"error")
              
              return render(request,"expense_edit.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        qs = Expense.objects.get(id=id)

        return render(request,"expense_detail.html",{"data":qs})        


@method_decorator(signin_required,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"expense removed")

        return redirect("expense-add")
    

@method_decorator(signin_required,name="dispatch")
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total)

        category_list=expense_list.values("category").annotate(total=Sum("amount"))

        print("cat list: ",category_list)

        priority_list=expense_list.values("priority").annotate(total=Sum("amount"))

        print("priority list:" , priority_list)

        data={
            
            "expense_total":expense_total,

            "category_summary":category_list,

            "priority_summary":priority_list

        }

        return render(request,"expense_summary.html",data)


class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"registration.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            # form_instance.save() password will not encrypted
            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            print("user object created")

            return redirect("signin")
        
        else:

            print("failed")

            return render(request,"registration.html",{"form":form_instance})
        

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})     
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("dashboard")
            
        messages.error(request,"Invalid Credential") 

        return render(request,"login.html",{"form":form_instance})   
    
@method_decorator(signin_required,name="dispatch")    
class SignOutView(View):

     def get(self,request,*args,**kwargs):

         logout(request)

         return redirect("signin")    




# ===================================================================================================================================================




@method_decorator(signin_required,name="dispatch")
class IncomeCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=IncomeForm()

        qs=Income.objects.filter(user_object=request.user).order_by("-created_date")

        return render(request,"income_add.html",{"form":form_instance,"data":qs})
    

    def post(self,request,*args,**kwargs):

        form_instance=IncomeForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object=request.user

            form_instance.save()

            messages.success(request,"income has been created !!")

            return redirect("income-add")
        
        else:

            messages.error(request,"error")

            return render(request,"income_add.html",{"form":form_instance})



@method_decorator(signin_required,name="dispatch")
class IncomeUpdateView(View):

     def get(self,request,*args,**kwargs):
         
        id=kwargs.get("pk")

        income_object=Income.objects.get(id=id)
     
        form_instance=IncomeForm(instance=income_object)

        return render(request,"income_edit.html",{"form":form_instance})
     
     def post(self,request,*args,**kwargs): 
    
         id=kwargs.get("pk")

         expense_object=Income.objects.get(id=id)

         form_instance=IncomeForm(instance=expense_object,data=request.POST)

         if form_instance.is_valid():
              
              form_instance.save()

              messages.success(request,"Income changed")

              return redirect("income-add")
         else:
              
              messages.error(request,"Failed")
              
              return render(request,"income_edit.html",{"form":form_instance})         
         

@method_decorator(signin_required,name="dispatch")
class IncomeDetailView(View):

    def get(self,request,*args,**kwargs):

        id = kwargs.get("pk")

        qu = Income.objects.get(id=id)

        return render(request,"income_detail.html",{"data":qu})     
    

@method_decorator(signin_required,name="dispatch")
class IncomeDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Income.objects.get(id=id).delete()

        messages.success(request,"income removed")

        return redirect("income-add")       

@method_decorator(signin_required,name="dispatch")
class IncomeSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        income_list=Income.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)

        income_total=income_list.values("amount").aggregate(total=Sum("amount"))

        print(income_total)

        category_list=income_list.values("category").annotate(total=Sum("amount"))

        print("category list: ",category_list)

        data={
              
            "income_total":income_total,

            "category_summary":category_list,

        }

        return render(request,"income_summary.html",data)
    

class DashBoardView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        expense_list=Expense.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)

        income_list=Income.objects.filter(created_date__month=current_month,created_date__year=current_year,user_object=request.user)

        # print(expense_list,income_list)

        expense_total=expense_list.values("amount").aggregate(total=Sum("amount"))

        income_total=income_list.values("amount").aggregate(total=Sum("amount"))

        print(expense_total,income_total)

        return render(request,"dashboard.html")    









