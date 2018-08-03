from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import HelloSerializer, UserProfileSerializer,ProfileFeedItemSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .models import UserProfile, ProfileFeedItem
from .permissions import UpdateOwnProfile,PostOwnStatus
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class HelloAPIView(APIView):
    """Testing API view"""
    serializer_class = HelloSerializer

    def get(self,request,format=None):
        """Returns a List of API views Features"""

        an_apiview = [
            'Uses HTTP methods as functions(get,post,patch,put,delete)',
            'It is similar to a traditional django view',
            'Gives you most control over your logic',
            'Its mapped  manually to URLs'
        ]
        return Response({
            'message':'Hello',
            'an_apiview':an_apiview
        })

    def post(self,request):
        """Create a  hello message from name."""
        serializer = HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(
                serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        """Handles updating a project"""
        return Response({'method':'put'})

    def patch(self,request,pk=None):
        """Patch request only updates fields provided in the request"""
        return Response({'method':'patch'})

    def delete(self,request,pk=None):
        """Deletes an object in the database"""
        return Response({'method':'delete'})


class HelloViewset(viewsets.ViewSet):
    """Test API Viewset"""

    serializer_class = HelloSerializer
    def list(self,request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list,create,return,update,partial_update)',
            'Automatically maps to urls using Routers',
            'Provides more functionality with less codes.'
        ]

        return Response({'message':'Hello','a_viewset':a_viewset})

    def create(self,request):
        """Create a new hello message"""

        serializer = HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
        """Handles getting an object by its ID."""
        return Response({'http_method':'GET'})

    def update(self,request,pk = None):
        """Handles updating an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self,request,pk=None):
        """Handles updating part of an object."""
        return Response({'http_method':'Patch'})

    def destroy(self,request,pk=None):
        """Handles removing an object"""
        return Response({'http_method':'Delete'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, and updating of profiles"""
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token"""

    serializer_class = AuthTokenSerializer
    def create(self,request):
        """Use the ObtainAuthToken APIView to validate and crreate a token"""
        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating of profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    # permission_classes=(PostOwnStatus,IsAuthenticatedOrReadOnly)
    permission_classes=(PostOwnStatus,IsAuthenticated)

    def perform_create(self,serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile = self.request.user)
