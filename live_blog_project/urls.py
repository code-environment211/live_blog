
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import LiveBlogViewSet, CommentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from users.views import UserRegisterView

router = DefaultRouter()
router.register(r'blogs', LiveBlogViewSet, basename='blogs')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'register', UserRegisterView, basename='register' )


urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('', include('users.urls')),
    path('', include('blog.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
