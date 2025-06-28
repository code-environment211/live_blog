from rest_framework import generics
from .models import CustomUser
from .serializers import UserRegisterSerializer, FollowSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Follow

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FollowSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save(follower=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        try:
            follow = Follow.objects.get(follower=request.user, following_id=user_id)
            follow.delete()
            return Response({'detail': 'Unfollowed successfully'})
        except Follow.DoesNotExist:
            return Response({'detail': 'Follow relationship does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        