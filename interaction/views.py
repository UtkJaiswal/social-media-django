from django.shortcuts import render
from rest_framework.views import APIView
from user.views import *
from rest_framework import status
from .models import *



# Create your views here.
class GetFriendsList(APIView):
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            data = request.user_data
            friend_list = Request.objects.filter(from_user = data.id, status="Approved").values('to_user')
            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Friends list fetched successfully"
            result['result']['data'] = friend_list
            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetSentPendingRequests(APIView):
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            logged_user_data = request.user_data
            sent_pending_requests = Request.objects.filter(from_user = logged_user_data.id, status="Pending").values('to_user')
            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Sent pending requests fetched successfully"
            result['result']['data'] = sent_pending_requests
            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetReceivedPendingRequests(APIView):
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            logged_user_data = request.user_data
            received_pending_requests = Request.objects.filter(to_user = logged_user_data.id, status="Pending").values('from_user')
            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Received pending requests fetched successfully"
            result['result']['data'] = received_pending_requests
            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AcceptRequest(APIView):
    @handle_auth_exceptions
    def post(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}

        try:
            logged_user_data = request.user_data
            from_user_id = request.body['from_user_id']

            data = Request.objects.data(from_user=from_user_id, to_user = logged_user_data.id)
            data.status = "Approved"
            data.save()
            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Request accepted successfully"
            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    
