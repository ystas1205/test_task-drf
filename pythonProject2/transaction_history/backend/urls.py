from django.urls import path

from backend.views import ImportProduct

app_name = 'backend'
urlpatterns = [
    path('import', ImportProduct.as_view(), name='importproduct'),

]
