from django.urls import path
from directory.views import FolderViewSet,GetFolder
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'folder', FolderViewSet, basename='user')
urlpatterns=[
    path("Folder-content/<uuid:pk>/", GetFolder.as_view()),

]
urlpatterns += router.urls