from django.urls import path

from . import views
urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead_list'),
    path('lead_detail/<str:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('create_lead/', views.LeadCreateView.as_view(), name='create_lead'),
    path('update_lead/<str:pk>/', views.LeadUpdateView.as_view(), name='update_lead'),
    path('delete_lead/<str:pk>/', views.LeadDeleteView.as_view(), name='delete_lead'),
    path('assign_lead/<str:pk>/', views.AssignAgentView.as_view(), name='assign_lead'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category-detail/<str:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category-update/<str:pk>', views.LeadCategoryUpdateView.as_view(), name='update_category'),
]
