from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from storage_spaces.views import StorageSpaceViewSet
from inventory.views import ItemViewSet, ClassViewSet
from core.views import PatchLogoutView, ActivityLogViewSet
from django.contrib.auth.decorators import login_required
from django.urls import reverse

schema_view = get_schema_view(
   openapi.Info(
      title="Warehouse API",
      default_version='v1',
      description="Strypes assesment test",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@warehouse.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)


router = routers.DefaultRouter()
# router.register(r'users', django_rest_framework.UserViewSet)
# router.register(r'groups', django_rest_framework.GroupViewSet)
# router.register(r'inventory/class', ClassViewSet)

router.register(r'storage_spaces', StorageSpaceViewSet)
router.register(r'inventory/item', ItemViewSet)
router.register(r'activity_log', ActivityLogViewSet)
# router.register(r'core', LogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('swagger<format>/', login_required(schema_view.without_ui(cache_timeout=0), login_url='/api-auth/login'), name='schema-json'),
    path('swagger/', login_required(schema_view.with_ui('swagger', cache_timeout=0), login_url='/api-auth/login'), name='schema-swagger-ui'),
    path('redoc/', login_required(schema_view.with_ui('redoc', cache_timeout=0), login_url='/api-auth/login'), name='schema-redoc'),
    path("api-auth/logout/", PatchLogoutView.as_view(), name="logout"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
