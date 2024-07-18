import jwt
from django.conf import settings
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import check_password




# function to generate token for a logged in user
def generate_token(id, name,phone,email,gender,age):
    payload = {
        'id':id,
        'name' : name,
        'phone':phone,
        'email' : email,
        'gender':gender,
        'age':age
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS512')
    return token



# function to handle authentication
def handle_auth_exceptions(func):
    def wrapper(*args, **kwargs):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}
        try:
            request = args[1]
            header_access_token = request.META.get('HTTP_AUTHORIZATION')
            if not header_access_token:
                result['result']['message'] = "Authorization header missing"
                return Response(result,status=status.HTTP_400_BAD_REQUEST)
            splited_access_token = header_access_token.split(' ')
            if len(splited_access_token) != 2:
                result['result']['message'] = "Authorization header missing"
                return Response(result,status=status.HTTP_400_BAD_REQUEST)
            access_token = splited_access_token[1]
            user_data = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=["HS512"])
            if not user_data or 'email' not in user_data:
                result['result']['message'] = "User data not found in token"
                return Response(result,status=status.HTTP_401_UNAUTHORIZED)
            request.user_data = user_data
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            result['result']['message'] = "Token expired. Please login again"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            result['result']['message'] = "User not found"
            return Response(result, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result['result']['message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper




# POST API to register a user
class RegisterUser(APIView):
    def post(self,request):
        result = {}
        result['status'] =  'NOK'
        result['valid']  =  False
        result['result'] = {"message":"Unauthorized access","data" :{}}

        try:
            # email field
            email = request.data['email']
            
            # logic to check if user with this email already exists or not
            if len(email)>0:
                email_data = User.objects.filter(email=email)
                if len(email_data)>0:
                    result['result'] = {"message":"User with this email already exists","data" :{}}
                    return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                
            serializer       = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()

                response_data = serializer.data

                # remove password from the response
                response_data.pop('password', None)
                    
                result['status']    =   "OK"
                result['valid']     =   True
                result['result']['message'] =   "User registered successfully"
                result['result']['data'] = response_data
                return Response(result,status=status.HTTP_200_OK)

            else:
                result['result']['message'] = (list(serializer.errors.keys())[
                    0]+' - '+list(serializer.errors.values())[0][0]).capitalize()
                return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        except Exception as e:
                result['result']['message'] =   str(e)
                return Response(result,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



# POST API to login a user
class Login(APIView):
    def post(self,request):
        result = {}
        result['status']    =   "NOK"
        result['valid']     =   False
        result['result']    =   {"message":"Unauthorized access","data":{}}

        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():

            email           = serializer.validated_data['email']

            # conevr the email to lower case for case insensitive
            email           = email.lower()
            password        = serializer.validated_data['password']

            try:

                # fetch the user with the given email
                user_data       = User.objects.get(email=email)

            except Exception as e:
                    result['result']['message'] = "Invalid Username or Password"
                    return Response(result, status=status.HTTP_401_UNAUTHORIZED)
            
            if (user_data is None):
                result['result']['message'] = "Invalid username or password"
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                # match the hashed password for the user
                if user_data.check_password(password)==False:
                    result['result']['message'] = "Incorrect password"
                    return Response(result, status=status.HTTP_401_UNAUTHORIZED)
                
                # generate the token for the user
                token                       =   generate_token(user_data.id,user_data.name,user_data.phone,user_data.email,user_data.gender,user_data.age)
                
                final_response  =   {
                            'name'          : user_data.name,
                            'user_id'       : user_data.id,
                            'email'         : user_data.email,
                            'phone'         : user_data.phone,
                            'token'         : token,
                        }

                result['status']            =   "OK"
                result['valid']             =   True
                result['result']['message'] =   "You are successfully logged in."
                result['result']['data']    =   final_response
                return Response(result,status=status.HTTP_200_OK)
                    
        else:
            result['result']['message'] = (list(serializer.errors.keys())[
                0]+' - '+list(serializer.errors.values())[0][0]).capitalize()
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)