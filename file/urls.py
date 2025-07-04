from django.urls import path
from file import views as view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'file', view.Fileviewset, basename='user')
urlpatterns=[
    path("get-total-size/",view.GetTotalSize.as_view()),
    path("restore-file/<uuid:id>/",view.RestoreFile.as_view()),
    path("movefile/",view.MoveFile.as_view())

]
urlpatterns += router.urls