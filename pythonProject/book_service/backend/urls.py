from django.urls import path
from backend.views import RegisterUser, ContactUser, UserData, OrderView, OrderData, OrderHistory, Updateproduct, ImportProduct

app_name = 'backend'
urlpatterns = [
    path('user', RegisterUser.as_view(), name='user'),
    path('contact', ContactUser.as_view(), name='contact'),
    path('userdata', UserData.as_view(), name='userdata'),
    path('order', OrderView.as_view(), name='order'),
    path('orderdata', OrderData.as_view(), name='orderdata'),
    path('orderhistory', OrderHistory.as_view(), name='orderhistory'),
    path('updateproduct', Updateproduct.as_view(), name='updateproduct'),
    path('importproduct', ImportProduct.as_view(), name='importproduct')

]
