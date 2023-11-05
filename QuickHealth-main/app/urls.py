from unicodedata import name
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.IndexView,name="LandingPage"),
    path("signup/",views.Signup,name="signup"),
    path("insert/",views.InsertData,name="insert"),
    path("login/",views.LoginUser,name="login"),
    path("appointpage/",views.Appointpage,name="appointpage"),
    path("search/",views.Searchpage,name="search"),
    path("zoom/",views.Book,name="zoom"),
    path("main/",views.Mainpage,name="main"),
    path("details1/",views.DoctorView,name="details1"),
    path("email/",views.SendEmail,name="email"),
    path("delete/<str:pk>", views.DeleteData, name="delete"),
    path("doctor/", views.DoctorPage, name="doctor"),
    path("record/", views.Record, name="record"),
    path("details/", views.doctorFormView, name="details"),
    path("wallet/", views.WalletView, name="wallet"),
    path("addmoney/", views.Addmoney, name="addmoney"),
    path("balance/", views.BalanceView, name="balance"),
    # path("delete/<int:pk>", views.DeleteData, name="delete"),
]