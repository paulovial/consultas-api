from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfissionalSaudeViewSet, ConsultaViewSet

router = DefaultRouter()
router.register(r'profissionais', ProfissionalSaudeViewSet)
router.register(r'consultas', ConsultaViewSet)

urlpatterns = [
    path('', include(router.urls))
]
