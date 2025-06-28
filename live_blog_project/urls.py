
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import LiveBlogViewSet, CommentViewSet
from users.views import UserRegisterView, FollowUserView, UnfollowUserView
from users.views import UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

router = DefaultRouter()
router.register(r'blogs', LiveBlogViewSet, basename='blogs')
router.register(r'comments', CommentViewSet, basename='comments')



urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include('users.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
