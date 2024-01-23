import pyzipper
from django.http import FileResponse
from django.core.management import call_command
import os

def create_dumpdate_archive(password: str) -> FileResponse:
    json_file = 'db.json'
    archive_name = "database.zip"

    with open(json_file, 'w', encoding='utf-8') as f:
        call_command('dumpdata', format='json', stdout=f, exclude=["dumpdata"] )
    f.close()
    
    with pyzipper.AESZipFile(archive_name,
                            'w',
                            encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(bytes(password, encoding='utf-8'))
        zf.write(json_file)

    os.remove(json_file)

    return FileResponse(
        open(archive_name, 'rb'),
        as_attachment=True,
        filename=archive_name
    )