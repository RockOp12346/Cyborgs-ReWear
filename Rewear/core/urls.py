from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('item/<int:pk>/', views.item_detail, name='item_detail'),
    # path('item/new/', views.item_create, name='item_create'),
    # path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
    # path('swap-request/<int:pk>/', views.swap_request, name='swap_request'),
    # path('profile/', views.profile, name='profile'),
    # path('profile/edit/', views.profile_edit, name='profile_edit'),
]
