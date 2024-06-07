from rest_framework.routers import DefaultRouter

from backend.views import EmployeeViewSet, DepartamentViewSet

app_name = 'backend'

router = DefaultRouter()
router.register('employee', EmployeeViewSet)
router.register('departament', DepartamentViewSet)
urlpatterns = router.urls
