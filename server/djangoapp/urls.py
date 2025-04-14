# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Authentication paths
    path('login/', views.login_user, name='api_login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration, name='register'),
    
    # Dealer paths
    path('get_dealers', views.get_dealers, name='get_dealers'),
    path('get_dealers/', views.get_dealers, name='get_dealers_with_slash'),
    path('get_dealers/<str:state>', views.get_dealers_by_state, name='get_dealers_by_state'),
    path('get_dealers/<str:state>/', views.get_dealers_by_state, name='get_dealers_by_state_with_slash'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    
    # Review paths
    path('reviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),
    path('add_review/', views.add_review, name='add_review'),
    
    # Car paths
    path('get_cars/', views.get_cars, name='getcars'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
