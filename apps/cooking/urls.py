from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_recipe, name='add_recipe'),
    path('', view=views, name='index'),
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
]

from django.urls import include, path

urlpatterns = [
    path('users/', include('users.urls')),
    # ... другие URL ...
]

from django.contrib.auth import views as auth_views

urlpatterns = [
    # ...
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
