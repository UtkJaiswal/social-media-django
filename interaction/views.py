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
            friend_list = Request.objects.filter(from_user = data['id'], status="Approved").values('to_user__name')
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

            sent_pending_requests = Request.objects.filter(from_user = logged_user_data['id'], status="Pending").values('to_user__name')
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
            received_pending_requests = Request.objects.filter(to_user = logged_user_data['id'], status="Pending").values('from_user__name')
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
            from_user_id = request.data['from_user_id']

            data = Request.objects.get(from_user=from_user_id, to_user = logged_user_data['id'], status="Pending")
            data.status = "Approved"
            data.save()
            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Request accepted successfully"
            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SendRequest(APIView):
    @handle_auth_exceptions
    def post(self, request):
        result = {
            'status': 'NOK',
            'valid': False,
            'result': {"message": "Unauthorized access", "data": {}}
        }

        try:
            logged_user_data = request.user_data
            to_user_id = request.data['to_user_id']

            from_user = User.objects.get(id=logged_user_data['id'])
            to_user = User.objects.get(id=to_user_id)

            data = {
                "from_user": from_user,
                "to_user": to_user,
                "status": "Pending"
            }
            Request.objects.create(**data)
            result['status'] = "OK"
            result['valid'] = True
            result['result']['message'] = "Request sent successfully"
            return Response(result, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            result['result']['message'] = "User not found"
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RejectRequest(APIView):
    @handle_auth_exceptions
    def post(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}

        try:
            logged_user_data = request.user_data
            from_user_id = request.data['from_user_id']

            data = Request.objects.get(from_user=from_user_id, to_user = logged_user_data['id'], status="Pending")
            data.delete()
            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Request rejected successfully"
            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    
