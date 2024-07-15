from django.urls import path
from .views import *

urlpatterns = [ 
    path('signup/', RegisterUser.as_view()),
    path('login/', Login.as_view()),
    # path('user-details/', UserDetailsView.as_view()),
]
