from django.urls import path
from .views import deploy_site, serve_site

urlpatterns = [
    path('deploy/', deploy_site),
    # the `sites/...` routes are also included under `/api/` for
    # convenience; the root URLconf mirrors them so both
    # `/sites/...` and `/api/sites/...` work.
    path('sites/<str:site_id>/', serve_site),
    path('sites/<str:site_id>/<path:path>', serve_site),
]