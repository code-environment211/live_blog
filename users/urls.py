from django.urls import path
from .views import FollowUserView, UnfollowUserView

urlpatterns = [
    path('followpage', FollowUserView.as_view(), name='followpage'),
    path('unfollowpage', UnfollowUserView.as_view(), name='unfollowpage')

]