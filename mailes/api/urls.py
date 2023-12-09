from mailes.api import api_views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('mail', api_views.MailViewSet, basename='mail'),
router.register('massage', api_views.MessageViewSet, basename='massage'),

urlpatterns = router.urls
