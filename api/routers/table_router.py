from api.routers.base_router import BaseRouter


class TableRouter(BaseRouter):
    def __init__(self, resource, ctrl):
        super().__init__(resource, ctrl)
        self._setup_operations()

    def _setup_operations(self):
        self._operations = {
        }