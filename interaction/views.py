from rest_framework.views import APIView
from user.views import *
from rest_framework import status
from .models import *
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination



# GET API : to fetch all friends list for the user
class GetFriendsList(APIView,PageNumberPagination):
    # checking for authentication
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            # get user data from token
            logged_data = request.user_data

            # list of friends who sent request to this user and got accepted
            friend_list_from_user = Request.objects.filter(from_user=logged_data['id'], status="Approved").values('to_user__id', 'to_user__name')

            # list of friends whom the user sent request and got accepted
            friend_list_to_user = Request.objects.filter(to_user=logged_data['id'], status="Approved").values('from_user__id', 'from_user__name')

            # logic to structure data in organized way
            combined_friend_list = []
            for friend in friend_list_from_user:
                combined_friend_list.append({
                    'id': friend['to_user__id'],
                    'name': friend['to_user__name']
                })

            for friend in friend_list_to_user:
                combined_friend_list.append({
                    'id': friend['from_user__id'],
                    'name': friend['from_user__name']
                })

            # pagination logic
            paginated_data = self.paginate_queryset(combined_friend_list,request, view=self)
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
        


# GET API : to fetch list of pending requests sent by the user      
class GetSentPendingRequests(APIView, PageNumberPagination):
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            logged_user_data = request.user_data
            
            # list of requests sent by user which are still pending
            sent_pending_requests = Request.objects.filter(from_user = logged_user_data['id'], status="Pending").values('to_user__id','to_user__name')

            final_sent_pending_requests = []
            for sent_pending_request in sent_pending_requests:
                final_sent_pending_requests.append({
                    'id': sent_pending_request['to_user__id'],
                    'name': sent_pending_request['to_user__name']
                })

            paginated_data = self.paginate_queryset(final_sent_pending_requests,request, view=self)
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
        



# GET API : to fetch received pending request
class GetReceivedPendingRequests(APIView, PageNumberPagination):
    @handle_auth_exceptions
    def get(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            logged_user_data = request.user_data

            # list of requests received by the user which are pending
            received_pending_requests = Request.objects.filter(to_user = logged_user_data['id'], status="Pending").values('from_user__id','from_user__name')

            final_received_pending_requests = []
            for received_pending_request in received_pending_requests:
                final_received_pending_requests.append({
                    'id': received_pending_request['from_user__id'],
                    'name': received_pending_request['from_user__name']
                })

            paginated_data = self.paginate_queryset(final_received_pending_requests,request, view=self)
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
        



# POST API : to accept a pending request
class AcceptRequest(APIView):
    @handle_auth_exceptions
    def post(self, request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}

        try:
            logged_user_data = request.user_data

            # id of the user who sent the request to the logged in user
            from_user_id = request.data['from_user_id']
            
            # get the instance of the pending request entry
            data = Request.objects.get(from_user=from_user_id, to_user = logged_user_data['id'], status="Pending")

            # change the status from "Pending" to "Approved"
            data.status = "Approved"

            # update the entry in the database
            data.save()

            result['status']    =   "OK"
            result['valid']     =   True
            result['result']['message'] =   "Request accepted successfully"
            return Response(result,status=status.HTTP_200_OK)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# POST API : to send request to another user who is neither a friend nor the status is "pending"        
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

            # logic to check if the user is not sending the request to self
            if from_user.id == to_user.id:
                result['result']['message'] = "Cannot send request to yourself"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            # logic to check a user cannot send 3 requests withing a minute
            current_time = datetime.now()
            last_three_times = from_user.last_three_request_times

            
            last_three_times = [datetime.fromisoformat(t) for t in last_three_times]
            last_three_times = [t for t in last_three_times if current_time - t < timedelta(minutes=1)]

            if len(last_three_times) >= 3:
                result['result']['message'] = "Cannot send more than 3 requests within a minute"
                return Response(result, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # logic to check if the user has already sent a request and is a friend or the status is "Pending"
            
            is_request_data = Request.objects.filter(from_user=logged_user_data['id'], to_user=to_user_id)

            if len(is_request_data) != 0:
                result['result']['message'] = "Cannot send request"
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # logic to check if the user has already received a request and is a friend or the status is "Pending"


            is_request_data = Request.objects.filter(from_user=to_user_id, to_user=logged_user_data['id'])

            if len(is_request_data) != 0:
                result['result']['message'] = "Cannot send request"
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

            # add the current time to the list of last_three_time

            
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
        


        
# POST API : to reject a pending request
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



# POST API : to search for a user based on exact matching of email or substring matching of name
class SearchUser(APIView, PageNumberPagination):
    @handle_auth_exceptions
    def post(self, request):
        result = {
            'status': 'NOK',
            'valid': False,
            'result': {"message": "Unauthorized access", "data": {}}
        }

        try:
            # search_string request from user
            search_string = request.data.get('search_string', '')

            if not search_string:
                result['result']['message'] = "Search string is required"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            # search for exact matching of the email for a user
            user_by_email = User.objects.filter(email=search_string)

            

            if len(user_by_email)>0:
                users_list = [{'id': user.id, 'name': user.name} for user in user_by_email]

                paginated_data = self.paginate_queryset(users_list,request, view=self)
                paginated_data = self.get_paginated_response(paginated_data).data

                result['status'] = "OK"
                result['valid'] = True
                result['result']['message'] = "User found by email"
                result['result']['next'] = paginated_data['next']
                result['result']['previous'] = paginated_data['previous']
                result['result']['count'] = paginated_data['count']
                result['result']['data'] = paginated_data['results']
                return Response(result, status=status.HTTP_200_OK)

            # check for substring match for name
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