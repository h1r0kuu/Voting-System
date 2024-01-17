# import zipfile
import pyminizip
from django.http import FileResponse


def create_dumpdate_archive(password: str) -> FileResponse:
    archive_name = "database.zip"
    pyminizip.compress("db.sqlite3", None, archive_name, password, 8)

    return FileResponse(
        open(archive_name, 'rb'),
        as_attachment=True, 
        filename=archive_name
    )