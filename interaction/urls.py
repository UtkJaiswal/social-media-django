from django.urls import path
from .views import *

urlpatterns = [ 
    path('get_friends/', GetFriendsList.as_view()),
    path('get_sent_pending_requests/', GetSentPendingRequests.as_view()),
    path('get_received_pending_requests/', GetReceivedPendingRequests.as_view()),
    path('accept_request/', AcceptRequest.as_view()),
    path('send_request/', SendRequest.as_view()),
]
