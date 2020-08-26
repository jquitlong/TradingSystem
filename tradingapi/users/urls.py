from rest_framework_nested.routers import DefaultRouter
from .views import UserView

# User endpoint URL configuration
router = DefaultRouter()
router.register(r'', UserView)

urlpatterns = []
urlpatterns += router.urls