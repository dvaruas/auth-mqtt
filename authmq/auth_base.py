import socket
import threading


class AuthException(Exception):
    def __init__(self, reason):
        super().__init__()
        self.__r = reason

    def __str__(self):
        return "[{}] : {}".format(type(self).__name__, self.__r)


class AuthBase(threading.Thread):
    def __init__(self, host, port, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__host = host
        self.__port = port
        self.__client = None
        self.__exception = AuthException

    def set_exception(self, e_class):
        if isinstance(e_class, AuthException):
            self.__exception = e_class

    def create_client(self, *args, **kwargs):
        if not self.is_client_created():
            self.__client = mqtt.Client(*args, **kwargs)
        try:
            self.__client.connect(host=self.__host, port=self.__port)
        except (TimeoutError, ConnectionRefusedError):
            raise self.__exception(reason="The connection to Broker ({}:{}) "
                "was refused".format(host, port))
        except socket.gaierror:
            raise self.__exception(reason="The service was not found for ({}:{})"
                .format(host, port))

    def is_client_created(self):
        return isinstance(self.__client, mqtt.Client)

    def run(self):
        self.__client.loop_forever()
