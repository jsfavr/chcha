from product.viewsets import ProductaddView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('product',ProductaddView)