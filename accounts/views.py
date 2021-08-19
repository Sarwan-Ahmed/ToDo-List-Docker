from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import UserSerializer, RegisterSerializer, ResendLinkSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail, EmailMessage
from .models import User
from django.core.cache import cache
from django.contrib.sites.shortcuts import get_current_site
import threading
from rest_framework.exceptions import AuthenticationFailed

'''
POST: http://127.0.0.1:8000/accounts/register/  <-- create user
POST: http://127.0.0.1:8000/accounts/login/  <-- login user
POST: http://127.0.0.1:8000/accounts/logout/  <-- logout user
'''


class RegisterAPI(generics.GenericAPIView):
    """
    An API view to SignUp(register) a user.
    Takes Username, Email and Password.
    Creates a user and sends verification link for verifying ownership of email.
    """
    
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        
        try:
            domain = get_current_site(request)
            verificationLink = "http://"+str(domain)+"/accounts/verify-email/"+token.key+"/"
            messageContent = 'Hello '+str(request.data['username'])+"\nPlease click on the link below to verify your account:\n"+verificationLink
            messageSubject = 'Account verification'

            if not settings.TESTING:
                send_mail(subject=messageSubject,
                    message=messageContent,
                    from_email=None,
                    recipient_list=[request.data['email']],
                    fail_silently=False,)

                '''email = EmailMessage(subject=messageSubject, body=messageContent, 
                    from_email=settings.EMAIL_HOST_USER, to=[request.data['email']])
                email.send()'''

            return Response({'success':'Verification link sent to your email. Please verify your account'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error':"Email not sent"}, status=status.HTTP_400_BAD_REQUEST)



class VerifyEmail(generics.GenericAPIView):
    """
    An API view to verify email of new user.
    User redirects to this view when clicks on verification link sent on their email.
    User's email will be verified if they registered through email not through OAuth 2 .
    """

    permission_classes = (AllowAny,)

    def get(self, request, token):
        try:
            user_token = Token.objects.filter(key=token)
            if not user_token.exists():
                return Response({'detail': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

            user_id = user_token[0].user.pk
            user = User.objects.filter(id=user_id)
            
            if user[0].email_verified:
                return Response({'Response' : 'Email already verified'}, status=status.HTTP_200_OK)

            request.data['username'] = user[0].username
            request.data['email'] = user[0].email
            request.data['email_verified'] = True
            serializer = UserSerializer(user[0], data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response({
                "message": "Email verified successfully",
                "user": serializer.data,
                "token": token}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error':'Email verification failed.'}, status=status.HTTP_400_BAD_REQUEST)



class ResendLink(generics.GenericAPIView):
    """
    An Api view to resend verification link.
    Takes Email of registered user.
    Sends verification link for verifying ownership of email. 
    """

    permission_classes = (AllowAny,)
    serializer_class = ResendLinkSerializer

    def post(self, request):

        try:
            if 'email' not in request.data:
                return Response({'field error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=request.data['email'])
            if not user.exists():
                return Response({'error': 'SignUp required! Account does not exist.'}, status=status.HTTP_404_NOT_FOUND)

            if user[0].auth_provider != 'email':
                return Response({'error': "Can't send link. Your account is associated with "+user[0].auth_provider}, status=status.HTTP_403_FORBIDDEN)

            user = user[0]
            token, created = Token.objects.get_or_create(user=user)
            domain = get_current_site(request)
            verificationLink = "http://"+str(domain)+"/accounts/verify-email/"+token.key+"/"
            messageContent = 'Hello '+user.username+"\nPlease click on the link below to verify your account:\n"+verificationLink
            messageSubject = 'Account verification'

            if not settings.TESTING:
                send_mail(subject=messageSubject,
                    message=messageContent,
                    from_email=None,
                    recipient_list=[request.data['email']],
                    fail_silently=False,)
            
                '''email = EmailMessage(subject=messageSubject, body=messageContent, 
                from_email=settings.EMAIL_HOST_USER, to=[request.data['email']])
                email.send()
                EmailThread(email).start()'''

            return Response({'success':'verification link sent on email'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'verification link sending failed'}, status=status.HTTP_400_BAD_REQUEST)



        
class LoginView(ObtainAuthToken):
    """
    An API view to login a user.
    Takes Email in username field and Password. 
    Returns Token, User_ID and Email.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.email_verified:
            raise AuthenticationFailed(detail='Please verify your email first')
        if user.auth_provider!='email':
            raise AuthenticationFailed(detail='Please continue your login using ' + user.auth_provider)

        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)



class LogoutView(generics.GenericAPIView):
    """
    An API view to Logout a Logged In user.
    Takes Token in header for Authorization.
    Clear user's cache and Logout that user.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        # delete user reports from cache before logging out
        if cache.get(str(request.user.pk)+'_TotalTasks'):
            cache.delete(str(request.user.pk)+'_TotalTasks')

        if cache.get(str(request.user.pk)+'_AverageCompleted'):
            cache.delete(str(request.user.pk)+'_AverageCompleted')

        if cache.get(str(request.user.pk)+'_OverdueTasks'):
            cache.delete(str(request.user.pk)+'_OverdueTasks')

        if cache.get(str(request.user.pk)+'_MaxDate'):
            cache.delete(str(request.user.pk)+'_MaxDate')

        if cache.get(str(request.user.pk)+'_CountOpened'):
            cache.delete(str(request.user.pk)+'_CountOpened')

        request._auth.delete()
        logout(request)
        return Response({'Response':'successfully logged out'}, status=status.HTTP_200_OK)


'''
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

        def run(self):
            self.email.send()
'''