from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("incomes",views.IncomeViewSet,basename="incomes"),

router.register("expenses",views.ExpenseViewSet,basename="expenses")




urlpatterns=[
    path("register/",views.UserCreationView.as_view()),

    path("income/summary/",views.IncomeSummaryView.as_view()),



    path("exp/summary/",views.ExpenseSummaryView.as_view()),


    path("token/",ObtainAuthToken.as_view()),
]+router.urls