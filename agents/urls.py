from django.urls import path

from . import views



urlpatterns = [
    path('', views.AgentListView.as_view(), name='agent_list'),
    path('create_agent', views.AgentCreateView.as_view(), name='create_agent'),
    path('agent_detail/<str:pk>', views.AgentDetailView.as_view(), name='agent_detail'),
    path('update_agent/<str:pk>', views.AgentUpdateView.as_view(), name='update_agent'),
    path('delete_agent/<str:pk>', views.AgentDeleteView.as_view(), name='delete_agent'),
]
