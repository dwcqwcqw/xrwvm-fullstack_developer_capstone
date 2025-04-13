# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for API login
    path('login/', views.login_user, name='api_login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),
    # path for registration
    path('register/', views.registration, name='register'),
    
    # path for dealer reviews view
    path('fetchReviews/dealer/<int:dealer_id>/', views.get_dealer_reviews, name='dealer_reviews'),
    # path for dealers
    path('fetchDealers/', views.get_dealers, name='get_dealers'),
    # path for dealer by id
    path('fetchDealer/<int:dealer_id>/', views.get_dealer_by_id, name='dealer_by_id'),
    # path for dealers by state
    path('fetchDealers/<str:state>/', views.get_dealers_by_state, name='dealers_by_state'),
    # path for get cars
    path('get_cars/', views.get_cars, name='getcars'),

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
