from django.urls import path
from directory import views as view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'folder', view.FolderViewSet, basename='user')
urlpatterns=[
    path("folder-content/<uuid:pk>/", view.GetFolder.as_view()),
    path("root-folders/", view.GetRootFolders.as_view()),
    path("navigation-pane/", view.GetNavigationPane.as_view()),
    path("search/<str:name>/",view.SerchByname.as_view())

]
urlpatterns += router.urls