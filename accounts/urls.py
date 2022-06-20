from django.urls import path

from accounts import views

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path('signup/', views.signup_user, name='signup'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    # path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update'),
    path('send_qrcode/', views.send_qrcode_to_email, name='send_qrcode'),
]
