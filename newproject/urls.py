"""newproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tshop import views
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name="home"),
    path("checkout/",views.checkout,name="checkout"),
    path('login/',views.userlogin,name="login"),
    path('sign',views.signup,name="signup"),
    path('logout',views.userlogout,name="logout"),
    path('product/<str:slug>',views.productpage,name="productpage"),
    path('addtocart/<str:slug>/<str:size>',views.add_to_cart,name="addtocart"),
    path('cart/',views.cartitem,name="cart"),
    path('validate_payment/',views.validate_payment,name="validatepayment"),
    path('order/',views.orderpage,name="order"),
    path('cart/<int:id>/',views.delete_session,name="session"),
    path('removequantity/<str:slug>/<str:size>',views.removequantity,name="remove"),
    path('removeitem/',views.removeitem,name="removeitem"),
    path('passchange/',views.passchange,name="passchange"),
    path('profile/',views.userprofile,name="profile"),
    path('search/',views.search,name="search"),
    path('postcomment/',views.postcommentss,name="postcoment"),
    path("deleteitem/",views.deleteitem,name="deete")


  


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
