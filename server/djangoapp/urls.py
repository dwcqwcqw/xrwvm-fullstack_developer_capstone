# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Authentication routes
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration, name='register'),

    # Car routes
    path('cars/', views.get_cars, name='cars'),

    # Dealer routes
    path('dealers/', views.get_dealers, name='dealers'),
    path(
        'dealers/<int:dealer_id>/',
        views.get_dealer_details,
        name='dealer_details'
    ),

    # Review routes
    path('reviews/', views.add_review, name='add_review'),

    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # API routes
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('current_user/', views.current_user, name='current_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
