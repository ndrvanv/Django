from django.urls import path
from .views import user_form, many_fields_form
from .views import add_user, upload_image

urlpatterns = [
    path('user/add', user_form, name='user_form'),
    path('forms/', many_fields_form, name='many_fields_form'),
    path('user/', add_user, name='add_user'),
    path('upload', upload_image, name='upload_image')

    path('upload/', views.upload_image, name='upload_image'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('prod_edit/', views.prod_edit, name='prod_edit'),
]