"""
URL configuration for kpi_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# urlpatterns = [

#     # Spectacular API schema endpoints
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
#     path('admin/', admin.site.urls),
#     path('api/', include('kpi_app.urls')),
#     path('api/input/', include('interpreter_app.urls')),
# ]


from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from graphene_django.views import GraphQLView
from .schema import schema
from django.views.decorators.csrf import csrf_exempt

# Custom Router for API Root
class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        @api_view(['GET'])
        def api_root(request):
            return Response({
                "KPIs": reverse('kpi-list', request=request),
                "Assets": reverse('asset-list', request=request),
                "Linker": reverse('attribute-list', request=request),
                "Ingester": request.build_absolute_uri('/api/Ingester/'),
            })
        return api_root

# Define the main router
router = CustomRouter()

# Register viewsets from `kpi_app`
from kpi_app.views import KPIViewSet, AssetViewSet, AttributeViewSet

router.register(r'KPIs', KPIViewSet, basename='kpi')
router.register(r'Assets', AssetViewSet, basename='asset')
router.register(r'Linker', AttributeViewSet, basename='attribute')

urlpatterns = [
    # Spectacular API schema endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Admin site
    path('admin/', admin.site.urls),

    # Include API routes
    path('api/', include(router.urls)),
    path('api/', include('interpreter_app.urls')),
    # path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]




# from django.contrib import admin
# from django.urls import path, include
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
# from rest_framework.routers import DefaultRouter
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
# from rest_framework.decorators import api_view

# # Custom Router for custom API Root
# class CustomRouter(DefaultRouter):
#     def get_api_root_view(self, api_urls=None):
#         @api_view(['GET'])
#         def api_root(request, format=None):
#             return Response({
#                 "KPIs": reverse('kpi-list', request=request, format=format),
#                 "Assets": reverse('asset-list', request=request, format=format),
#                 "Linker": reverse('attribute-list', request=request, format=format),
#                 "Ingester": request.build_absolute_uri('/api/input/ingester/')
#             })
#         return api_root

# # Create and register routes
# router = CustomRouter()
# from kpi_app.views import KPIViewSet, AssetViewSet, AttributeViewSet

# router.register(r'KPIs', KPIViewSet, basename='kpi')
# router.register(r'Assets', AssetViewSet, basename='asset')
# router.register(r'Linker', AttributeViewSet, basename='attribute')

# # Main urlpatterns
# urlpatterns = [
#     # Spectacular API schema endpoints
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
#     # Admin site
#     path('admin/', admin.site.urls),
    
#     # API routes
#     path('api/', include(router.urls)),
#     path('api/input/', include('interpreter_app.urls')),  # Custom path for the Ingester app
# ]
