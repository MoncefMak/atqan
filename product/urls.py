from django.urls import path

from product import views

urlpatterns = [
    path('create/', views.ProductCreateApiView.as_view(), name='product-create'),
]
