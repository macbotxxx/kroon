# from django.conf import settings
# from django_hosts import patterns, host
# from drf_yasg.views import get_schema_view
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi


# schema_view = get_schema_view(
#    openapi.Info(
#       title="Kroon API V2",
#       default_version='v2',

#       description="this is endpoint for kroon and kioks inventory system",

#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@kroonapp.com"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )



# host_patterns = patterns('',
#     host(r'www', settings.ROOT_URLCONF, name='www'),
#     host(r'api', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# )