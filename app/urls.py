from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('',views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(),name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
  
    path('historia/', views.historia, name='historia'),
    path('contato/', views.contato, name='contato'),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('capacete/', views.capacete, name='capacete'),
    path('capacete/<slug:data>', views.capacete, name='capacetedata'),

    path('touca/', views.touca, name='touca'),
    path('touca/<slug:data>', views.touca, name='toucadata'),

    path('protetorFacial/', views.protetorFacial, name='protetorFacial'),
    path('protetorFacial/<slug:data>', views.protetorFacial, name='protetorFacialdata'),

    path('abafadorConcha/', views.abafadorConcha, name='abafadorConcha'),
    path('abafadorConcha/<slug:data>', views.abafadorConcha, name='abafadorConchadata'),

    path('protetorPlug/', views.protetorPlug, name='protetorPlug'),
    path('protetorPlug/<slug:data>', views.protetorPlug, name='protetorPlugdata'),

    path('mascaraPFF2/', views.mascaraPFF2, name='mascaraPFF2'),
    path('mascaraPFF2/<slug:data>', views.mascaraPFF2, name='mascaraPFF2data'),

    path('mascaraSemiFacial/', views.mascaraSemiFacial, name='mascaraSemiFacial'),
    path('mascaraSemiFacial/<slug:data>', views.mascaraSemiFacial, name='mascaraSemiFacialdata'),

    path('luvaRaspa/', views.luvaRaspa, name='luvaRaspa'),
    path('luvaRaspa/<slug:data>', views.luvaRaspa, name='luvaRaspadata'),

    path('luvaAntiCorte/', views.luvaAntiCorte, name='luvaAntiCorte'),
    path('luvaAntiCorte/<slug:data>', views.luvaAntiCorte, name='luvaAntiCortedata'),

    path('botinaMetatarso/', views.botinaMetatarso, name='botinaMetatarso'),
    path('botinaMetatarso/<slug:data>', views.botinaMetatarso, name='botinaMetatarsodata'),

    path('botina/', views.botina, name='botina'),
    path('botina/<slug:data>', views.botina, name='botinadata'),

    path('perneiraRaspa/', views.perneiraRaspa, name='perneiraRaspa'),
    path('perneiraRaspa/<slug:data>', views.perneiraRaspa, name='perneiraRaspadata'),


    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class= MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
   
    

    path('registration/', views.CustomerRegistrationView.as_view(),name="customerregistration")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
