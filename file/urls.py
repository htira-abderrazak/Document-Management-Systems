from django.urls import path
from file import views as view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'file', view.Fileviewset, basename='user')
urlpatterns=[
    path("get-total-size/",view.GetTotalSize.as_view())

]
urlpatterns += router.urls