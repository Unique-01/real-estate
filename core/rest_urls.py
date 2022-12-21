from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register('property-list', views.PropertyViewSet, basename='property')
router.register('categories', views.CategoryViewSet, basename='category')


urlpatterns = [

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('myprofile/', views.UserApiView.as_view()),
    path('register/', views.RegisterApiView.as_view()),

    # DOCUMENTATION
    path('docs/default', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]

