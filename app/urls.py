"""
    name='urls',
    project='contacts'
    date='3/14/2020',
    author='Oshodi Kolapo',
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('detail/<int:pk>/', views.DetailPageView.as_view(), name="detail"),
    path('search/', views.search, name='search'),
    path('contact/create/', views.CreateContactView.as_view(), name='create'),
    path('contact/update/<int:pk>/', views.UpdateContactView.as_view(), name="update"),
    path('contact/delete/<int:pk>/', views.DeletePageView.as_view(), name="delete"),
    # path('signup/', views.SignUpView.as_view(), name='signup')

]
