import zipfile
import uuid
import os

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Site
from .storage import upload_folder


@api_view(['POST'])
def deploy_site(request):

    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file provided"}, status=400)

    site_id = str(uuid.uuid4())[:8]
    zip_path = f"/tmp/{site_id}.zip"
    extract_path = f"/tmp/{site_id}"

    # save uploaded stream to disk first
    with open(zip_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    # attempt to open and extract, returning a clear error on failure
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        return Response({"error": "Uploaded file is not a valid ZIP archive"}, status=400)

    # copy extracted files into our local "sites" directory
    upload_folder(site_id, extract_path)

    subdomain = f"site{site_id}"

    Site.objects.create(
        site_name=subdomain,
        subdomain=subdomain,
        storage_path=site_id
    )

    # return a URL that actually works in development; we serve
    # contents through /sites/<id>/
    return Response({"url": f"http://127.0.0.1:8000/sites/{site_id}/"})


def serve_site(request, site_id, path=""):
    """Django view used in development to serve the uploaded files.

    The front end requests URLs like `/sites/abcd1234/` or
    `/sites/abcd1234/foo/bar.png`.  We delegate to
    ``django.views.static.serve`` but compute the document root
    dynamically based on the site_id.
    """
    from django.views.static import serve as static_serve

    document_root = os.path.join(settings.SITES_ROOT, site_id)
    if not path:
        path = "index.html"
    # let Django handle 404s, mime types, etc.
    return static_serve(request, path, document_root=document_root)
