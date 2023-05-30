
from django.contrib import admin
from django.urls import path
from manifestStores.views import (
    home,
    store,
    product_detail,
    cart,
    add_cart,
    add_cart2,
    remove_cart,
    delete_cart,
    search,

    logout,
    login,
    register,
    about,
    contact,
    activate,
    activate_email,
    forgotPassword,
    resetPassword,
    resetpassword_validate,
    )

from staff.views import(
    staff,
    )

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('store/', store, name='store'),
    path('store/<slug:category_slug>/', store, name='products_by_category'),
    path('store/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', remove_cart, name='remove_cart'),
    path('add_cart2/<int:product_id>/', add_cart2, name='add_cart2'),
    path('delete_cart/<int:product_id>/', delete_cart, name='delete_cart'),

    path('search/', search, name='search'),
    path('about-us/', about, name='about'),
    path('contact-us/', contact, name='contact'),

    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),


    path('staff/', staff, name='staff'),
    path('activate-email/', activate_email, name='activate_email'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),


    path('forgotPassword/', forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', resetPassword, name='resetPassword'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
