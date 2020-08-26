from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)

from .authentication import expires_in, token_expire_handler
from .serializers import UserSerializer, UserSigninSerializer


# Create your views here.
@api_view(["POST"])
@permission_classes((AllowAny,))
def signin(request):
    """
    Sign in endpoint User must be successfully signed in to get session token
    Session token will be used for accessing other endpoint
    """
    signin_serializer = UserSigninSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, 
        status=HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=signin_serializer.data['username'],
        password=signin_serializer.data['password'])
    if not user:
        return Response({'data': 'Invalid Credentials'}, 
        status=HTTP_404_NOT_FOUND)
        
    token, _ = Token.objects.get_or_create(user = user)
    
    is_expired, token = token_expire_handler(token) 
    user_serialized = UserSerializer(user)

    return Response({
    'user': user_serialized.data, 
    'expires_in': expires_in(token),
    'token': token.key}, 
    status=HTTP_200_OK)


class UserView(viewsets.ModelViewSet):
    """
    User viewset
    For basic CRUD (Create Read Update Delete)
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
