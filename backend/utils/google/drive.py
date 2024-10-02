from utils.google.service import build_service
from config_global import MEETINGS_EMAIL


class DriveApi:
    def __init__(self):
        scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
        self.service = build_service(
            service_name="drive",
            service_version="v3",
            on_behalf_of=MEETINGS_EMAIL,
            scopes=scopes,
        )

    def _search(self, query: str):
        results = (
            self.service.files()
            .list(
                q=query,
                spaces="drive",
                fields="files(id, name, webContentLink)",
                pageSize=1000,
            )
            .execute()
        )

        return results.get("files", [])

    def _set_file_permissions(self, file_id: str, permissions):
        return (
            self.service.permissions()
            .create(
                fileId=file_id, body=permissions, fields="id", supportsAllDrives=True
            )
            .execute()
        )

    def get_recordings(self, query):
        return self._search(query=query)

    def set_permissions(self, file_id: str, permissions):
        return self._set_file_permissions(file_id=file_id, permissions=permissions)
