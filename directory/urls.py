from directory.views import FolderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'folder', FolderViewSet, basename='user')
urlpatterns = router.urls