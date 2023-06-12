import re
import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import GenericAPIView
from .serial import RegistrationSerialization, RegisterInputSerializer, LoginSerializer, ChangePasswordSerial
from drf_yasg.utils import swagger_auto_schema
from .models import Registration
from rest_framework import status, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from knox.auth import TokenAuthentication


# Create your views here.

def index(request):
    return HttpResponse('<h1 style="text-align: center;"><span style="margin-top:50%;">Welcome To API Integration Project with React and Django</span></h1>')


def password_check(passwd):
    flag = 0
    import re
    if not re.search("[A-Z]", passwd):
        flag = 1
    if not re.search("[0-9]", passwd):
        flag = 2
    if not re.search("[@$!%*#?&]", passwd):
        flag = 3
    return flag

class RegistrionView(GenericAPIView):
    serializer_class = RegistrationSerialization

    @swagger_auto_schema(tags=['Authentication'], request_body=RegisterInputSerializer)
    def post(self, request, *args, **kwargs):
        try:
            if not RegisterInputSerializer(data=request.data).is_valid():
                return JsonResponse({'result':'false','response':'please insert valid data'},safe=False)
            check_data = request.data
            password = check_data['password']
            email = check_data['email']
            first_name = check_data['first_name']
            last_name = check_data['last_name']
            mobile_number = check_data.get('mobile_number')
            date_of_birth = check_data['date_of_birth']
            checkpoint  =  password_check(password)
            if checkpoint == 1:
                return JsonResponse({'result': 'fail', 'response': 'Password must contain atleast one capital alphbat'}, safe=False)
            if checkpoint == 2:
                return JsonResponse({'result': 'fail', 'response': 'Password must contain atleast one digit'}, safe=False)
            if checkpoint == 3:
                return JsonResponse({'result': 'fail', 'response': 'Password must contains one special character like @, $,#,&'}, safe=False)
        except Exception as e:
            return JsonResponse({'result': 'fail', 'response': 'Please enter valid password '}, safe=False)
        user_check_obj = Registration.objects.filter(email=email).count()
        if user_check_obj != 0:
            return JsonResponse({'result': 'false', 'response': 'user already exists!'}, safe=False)
        data = {
            'first_name': first_name, 
            'last_name': last_name, 
            'email': email,
            'username': email,
            'password': password, 
            'mobile_number': mobile_number, 
            'date_of_birth': datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = Registration.objects.create_user(username = email, email = email, password = password, first_name = first_name, last_name = last_name, mobile_number = mobile_number, date_of_birth = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date())
        return JsonResponse({'result': 'true', 'user': RegistrationSerialization(user).data}, status = status.HTTP_201_CREATED, safe=False)

class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request, format=None):
        info = request.data
        try:
            email = info['email']
            password = info['password']
        except Exception as e:
            return Response({'status': 'Success Fail', 'message': 'PLease enter valid email or password '},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        usercheck = Registration.objects.filter(email__iexact=email).count()
        if usercheck == 0:
            message = {'status': 'Fail',
                       'message': 'Please enter valid email or password! '}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        userdata = Registration.objects.get(email__iexact=email)

        if userdata.check_password(password) and userdata.is_active == True:
            print("getting user data: ", userdata)
            result = {
                'token':AuthToken.objects.create(user=userdata)[1],
                **RegistrationSerialization(userdata, context=self.get_serializer_context()).data
            }
            return JsonResponse({'status': 'Success', 'message': 'You have signin successfully!', 'data': result}, safe=False)
        else:
            message = {'status': 'Fail', 'message': 'Please enter valid email or password! '}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

class Logout(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):
        AuthToken.objects.filter(user=request.user).delete()
        return Response({'result': 'true', 'response': 'logged out successfully'},status=status.HTTP_200_OK)

class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerial
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):
        message = {'result': '', 'response': ''}
        info = request.data
        try:
            email = request.user.email
        except Exception as e:
            message['result'] = 'false'
            message['response'] = 'Email not sent please check'
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        try:
            currentpassword = info['currentpassword']
        except Exception as e:
            message['result'] = 'false'
            message['response'] = 'currentpassword not sent please check '
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        try:
            password = info['new_password']
        except Exception as e:
            message['result'] = 'false'
            message['response'] = 'password not sent please check '
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        try:
            confirmpassword = info['confirmpassword']
        except Exception as e:
            message['result'] = 'false'
            message['response'] = 'confirmpassword not sent please check '
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

        if not email:
            message = {'result': 'false', 'response': 'enter valid email data'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

        if not currentpassword:
            message = {'result': 'false',
                       'response': 'enter valid current password'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        if not password:
            message = {'result': 'false',
                       'response': 'enter valid password data'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        if not confirmpassword:
            message = {'result': 'false',
                       'response': 'enter valid confirmpassword data'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 4:
            message = {'result': 'false',
                       'response': 'enter password of minimun 4 digits'}
            return JsonResponse(message, safe=False)

        check_password = password
        checkpoint = password_check(check_password)
        if checkpoint == 1:
            return JsonResponse({'result': 'fail', 'response': 'Password must contain atleast one capital alphbat'}, safe=False)
        if checkpoint == 2:
            return JsonResponse({'result': 'fail', 'response': 'Password must contain atleast one digit'}, safe=False)
        if checkpoint == 3:
            return JsonResponse({'result': 'fail', 'response': 'Password must contains one special character like @, $,#,&'}, safe=False)

        if password != confirmpassword:
            message = {'result': 'false',
                       'response': 'password and confirmpassword doesnot match'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        userobj = Registration.objects.filter(email=email).count()
        if userobj == 0:
            message = {'result': 'false',
                       'response': 'Either Email or password doesnot match'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            userdata = Registration.objects.get(email=email)
            if userdata.check_password(password):
                message = {'result': 'false',
                       'response': 'new password already exists'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
            if userdata.check_password(currentpassword) :
                userdata.set_password(password)
                userdata.save()                
            else:
                message = {'result': 'false',
                           'response': 'wrong current password'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message = {'result': 'false', 'response': 'something went wrong'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        result = AuthToken.objects.filter(user=userdata).delete()
        message = {'result': 'true', 'response': 'successfull changed password'}
        return Response(message, status=status.HTTP_200_OK)

