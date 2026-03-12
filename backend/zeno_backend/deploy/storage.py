import os
import shutil
from django.conf import settings


# During development we simply copy the extracted directory into a
# `sites/<site_id>` folder under the project root.  This avoids
# needing an external storage service such as MinIO.
#
# The frontend can then be served by a small Django view that uses
# `django.views.static.serve`.

def upload_folder(site_id, folder):
    dest = os.path.join(settings.SITES_ROOT, site_id)

    # remove any previous contents so redeploy works cleanly
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)

    # if the archive unpacked to a single directory, treat that as the
    # real root – avoids URLs containing an extra folder layer.
    entries = os.listdir(folder)
    if len(entries) == 1:
        candidate = os.path.join(folder, entries[0])
        if os.path.isdir(candidate):
            folder = candidate

    # copy everything *inside* the (possibly replaced) folder.
    for name in os.listdir(folder):
        src_path = os.path.join(folder, name)
        dst_path = os.path.join(dest, name)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
