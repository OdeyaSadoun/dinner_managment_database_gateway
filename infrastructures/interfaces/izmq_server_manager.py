from abc import abstractmethod


class IZMQServerManager:
    @abstractmethod
    def _include_routers(self, routers):
        pass

    @abstractmethod
    def _connect(self, host, port):
        pass

    @abstractmethod
    def _start_recieving_requests(self):
        pass

    @abstractmethod
    def _handle_incoming_requests(self):
        pass
    
    @abstractmethod
    def _route_request(self, request):
        pass