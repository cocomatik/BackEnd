from django.urls import path,include
import POCOS.urls as PCU
import POJOS.urls as PJU
import Orders.urls as OU
from .view_login import send_otp_login,login,logout
from .views_home import home_best_sellers

from Accounts.userandaddressviews import user_profile_view,user_address_view,address_detail_view
urlpatterns = [
    path('pocos/', include(PCU)),
    path('pojos/', include(PJU)),
    path('orders/', include(OU)),

    path('home/bestsellers',home_best_sellers,name="home-best-sellers"),
    
    path("login/", login, name="api_login"),
    path("logout/", logout, name="api_logout"),
    path("send_otp_login/", send_otp_login, name="api_send_otp"),



    path('profile/', user_profile_view, name='user-profile'),
    path('addresses/',user_address_view, name='user-addresses'),
    path('addresses/<int:pk>/',address_detail_view, name='address-detail'),
]