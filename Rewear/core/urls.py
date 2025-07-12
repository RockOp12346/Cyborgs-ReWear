from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.signin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/new/', views.item_create, name='item_create'),
    path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('swap-request/<int:pk>/', views.swap_request, name='swap_request'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('adminusr', views.admin_items, name='admin_items'),
    path('incoming-swaps/', views.incoming_swaps, name='incoming_swaps'),
]
