from django.contrib import admin
from django.urls import path
from users import views as userViews
from django.contrib.auth import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', userViews.register, name="reg"),
    path('profile/', userViews.profile, name="profile"),
    path('user/', authViews.LoginView.as_view(template_name='users/user.html'), name="user"),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name="exit"),
    path('house/', userViews.ShowHouseView.as_view(), name="house"),
    path('house/<int:pk>/', userViews.HouseDetailView.as_view(), name="house-detail"),
    path('house/add/', userViews.CreateHouseView.as_view(), name="house-add"),
    path('house/<int:pk>/update/', userViews.UpdateHouseView.as_view(), name="house-update"),
    path('house/<int:pk>/delete/', userViews.DeleteHouseView.as_view(), name="house-delete"),
    path('house/<int:pk>/TController/add/', userViews.CreateTControllerView.as_view(), name="TController-add"),
    path('house/TController/<str:pk>/update/', userViews.UpdateTControllerView.as_view(), name="TController-update"),
    path('house/TController/<str:pk>/delete/', userViews.DeleteTControllerView.as_view(), name="TController-delete"),
    path('house/TController/<str:pk>/ControllerDetail/', userViews.ControllerDetail, name="ControllerDetail"),
    path('firstconnection/', userViews.FirstConnection, name="firstconnection"),
    path('connection/', userViews.Connection, name="connection"),
    path('house/<int:pk>/LController/add/', userViews.CreateLControllerView.as_view(), name="LController-add"),
    path('house/LController/<str:pk>/update/', userViews.UpdateLControllerView.as_view(), name="LController-update"),
    path('house/LController/<str:pk>/delete/', userViews.DeleteLControllerView.as_view(), name="LController-delete"),
    path('house/LController/<str:pk>/ControllerDetail/', userViews.LControllerDetail, name="LControllerDetail"),
    path('lfirstconnection/', userViews.LFirstConnection, name="lfirstconnection"),
    path('lconnection/', userViews.LConnection, name="lconnection"),
    path('house/<int:pk>/WController/add/', userViews.CreateWControllerView.as_view(), name="WController-add"),
    path('house/WController/<str:pk>/update/', userViews.UpdateWControllerView.as_view(), name="WController-update"),
    path('house/WController/<str:pk>/delete/', userViews.DeleteWControllerView.as_view(), name="WController-delete"),
    path('house/WController/<str:pk>/ControllerDetail/', userViews.WControllerDetail, name="WControllerDetail"),
    path('wfirstconnection/', userViews.WFirstConnection, name="wfirstconnection"),
    path('wconnection/', userViews.WConnection, name="wconnection"),
]
