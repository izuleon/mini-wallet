from django.urls import path
from customer import views

urlpatterns = [
    path('api/v1/init', views.init_customer),
]