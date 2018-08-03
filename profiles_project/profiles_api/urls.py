from django.conf.urls import url
from .views import HelloAPIView,HelloViewset,UserProfileViewSet,LoginViewSet,UserProfileFeedViewSet
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

# Viewsets define their own url rouutes.
router = DefaultRouter()
router.register('hello-viewset',HelloViewset, base_name='Hello-viewset')
router.register('profile',UserProfileViewSet)
router.register('login',LoginViewSet,base_name='login')
router.register('feed',UserProfileFeedViewSet)


urlpatterns = [
    url(r'^hello-view/',HelloAPIView.as_view()),
    url(r'',include(router.urls))

]
