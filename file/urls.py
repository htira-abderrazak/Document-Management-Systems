from .views import Fileviewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'file', Fileviewset, basename='user')
urlpatterns = router.urls