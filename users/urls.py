from django.urls import path, include
from .views import FollowUserView, UnfollowUserView

urlpatterns = [
    path('api/followpage/', FollowUserView.as_view(), name='followpage'),
    path('api/unfollowpage/<int:user_id>/', UnfollowUserView.as_view(), name='unfollowpage'),

]