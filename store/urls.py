from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth import views as auth_views
from django.urls import path

from store import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('address/', views.address, name='address'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='store/login.html',
            authentication_form=AuthenticationForm,
        ),
        name='login',
    ),
    path('buy/', views.buy_now, name='buy-now'),
    path('bottomwear/', views.bottom_wear, name='bottomwear'),
    path('checkout/', views.checkout, name='checkout'),
    path(
        'changepassword/',
        auth_views.PasswordChangeView.as_view(
            template_name='store/change_password.html',
            form_class=PasswordChangeForm,
            success_url='/changepassworddone/',
        ),
        name='changepassword',
    ),
    path(
        'changepassworddone/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='store/change_password_done.html',
        ),
        name='changepassworddone',
    ),
    path('emptycart/', views.show_cart, name='emptycart'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:company>', views.laptop, name='laptopdata'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('orders/', views.orders, name='orders'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('profile/', views.profile, name='profile'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='store/password_reset.html',
            form_class=PasswordResetForm,
        ),
        name='passwordreset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='store/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='store/password_reset_confirm.html',
            form_class=SetPasswordForm,
        ),
        name='password_reset_confirm',
    ),
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='store/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    path('removecart/', views.remove_cart, name='removecart'),
    path('signup/', views.sign_up, name='customersignup'),
    path('showcart/', views.show_cart, name='showcart'),
    path('topwear/', views.top_wear, name='topwear'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
