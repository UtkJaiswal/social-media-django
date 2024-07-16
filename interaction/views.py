from rest_framework.views import APIView
from user.views import *
from rest_framework import status
from .models import *
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination




class GetFriendsList(APIView,PageNumberPagination):
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            data = request.user_data
            friend_list = Request.objects.filter(from_user = data['id'], status="Approved").values('to_user__id','to_user__name')

            paginated_data = self.paginate_queryset(friend_list,request, view=self)
            paginated_data = self.get_paginated_response(paginated_data).data

            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Friends list fetched successfully"
            result['result']['next'] = paginated_data['next']
            result['result']['previous'] = paginated_data['previous']
            result['result']['count'] = paginated_data['count']
            result['result']['data'] = paginated_data['results']

            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


        
class GetSentPendingRequests(APIView, PageNumberPagination):
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            logged_user_data = request.user_data

            sent_pending_requests = Request.objects.filter(from_user = logged_user_data['id'], status="Pending").values('to_user__id','to_user__name')

            paginated_data = self.paginate_queryset(sent_pending_requests,request, view=self)
            paginated_data = self.get_paginated_response(paginated_data).data

            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Sent pending requests fetched successfully"
            result['result']['next'] = paginated_data['next']
            result['result']['previous'] = paginated_data['previous']
            result['result']['count'] = paginated_data['count']
            result['result']['data'] = paginated_data['results']

            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




class GetReceivedPendingRequests(APIView, PageNumberPagination):
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            logged_user_data = request.user_data
            received_pending_requests = Request.objects.filter(to_user = logged_user_data['id'], status="Pending").values('from_user__id','from_user__name')

            paginated_data = self.paginate_queryset(received_pending_requests,request, view=self)
            paginated_data = self.get_paginated_response(paginated_data).data

            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Received pending requests fetched successfully"
            result['result']['next'] = paginated_data['next']
            result['result']['previous'] = paginated_data['previous']
            result['result']['count'] = paginated_data['count']
            result['result']['data'] = paginated_data['results']

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

            
            current_time = datetime.now()
            last_three_times = from_user.last_three_request_times

            
            last_three_times = [datetime.fromisoformat(t) for t in last_three_times]
            last_three_times = [t for t in last_three_times if current_time - t < timedelta(minutes=1)]

            if len(last_three_times) >= 3:
                result['result']['message'] = "Cannot send more than 3 requests within a minute"
                return Response(result, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            is_request_data = Request.objects.filter(from_user=logged_user_data['id'], to_user=to_user_id)

            if len(is_request_data) != 0:
                result['result']['message'] = "Cannot send request"
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


            is_request_data = Request.objects.filter(from_user=to_user_id, to_user=logged_user_data['id'])

            if len(is_request_data) != 0:
                result['result']['message'] = "Cannot send request"
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            last_three_times.append(current_time)

           
            last_three_times = last_three_times[-3:]

            
            from_user.last_three_request_times = [t.isoformat() for t in last_three_times]
            from_user.save()

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




class SearchUser(APIView, PageNumberPagination):
    @handle_auth_exceptions
    def post(self, request):
        result = {
            'status': 'NOK',
            'valid': False,
            'result': {"message": "Unauthorized access", "data": {}}
        }

        try:
            search_string = request.data.get('search_string', '')

            if not search_string:
                result['result']['message'] = "Search string is required"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            
            user_by_email = User.objects.filter(email=search_string)

            

            if len(user_by_email)>0:
                users_list = [{'id': user.id, 'name': user.name} for user in user_by_email]

                paginated_data = self.paginate_queryset(users_list,request, view=self)
                paginated_data = self.get_paginated_response(paginated_data).data

                result['status'] = "OK"
                result['valid'] = True
                result['result']['message'] = "User found by email"
                # result['result']['data'] = {
                #     'id': user_by_email.id,
                #     'name': user_by_email.name
                # }
                result['result']['next'] = paginated_data['next']
                result['result']['previous'] = paginated_data['previous']
                result['result']['count'] = paginated_data['count']
                result['result']['data'] = paginated_data['results']
                return Response(result, status=status.HTTP_200_OK)

            
            users_by_name = User.objects.filter(name__icontains=search_string)
            if users_by_name.exists():
                users_list = [{'id': user.id, 'name': user.name} for user in users_by_name]

                paginated_data = self.paginate_queryset(users_list,request, view=self)
                paginated_data = self.get_paginated_response(paginated_data).data

                result['status'] = "OK"
                result['valid'] = True
                result['result']['message'] = "Users found by name"
                result['result']['next'] = paginated_data['next']
                result['result']['previous'] = paginated_data['previous']
                result['result']['count'] = paginated_data['count']
                result['result']['data'] = paginated_data['results']
                
                return Response(result, status=status.HTTP_200_OK)

            result['result']['message'] = "No users found"
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)