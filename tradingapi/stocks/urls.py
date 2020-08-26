from rest_framework_nested.routers import DefaultRouter
from .views import StockView

# Create your urls here
router = DefaultRouter()
router.register(r'', StockView)

urlpatterns = []
urlpatterns += router.urls