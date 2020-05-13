from authmq.auth_base import AuthException, AuthBase
from authmq.globals import DEFAULT_BROKER_HOST, DEFAULT_BROKER_PORT


class AuthServerException(AuthException):
    pass


class AuthServer(threading.Thread):
    def __init__(self, host=DEFAULT_BROKER_HOST, port=DEFAULT_BROKER_PORT,
                 topic_prefix="", *args, **kwargs):
        super().__init__(host=host, port=port, *args, **kwargs)
        self.__prefix = "{}/".format(topic_prefix) if topic_prefix else ""
        self.__users_connected = {}
        self.set_exception(e_class=AuthServerException)
        self.module_setup()

    def client_setup(self, *args, **kwargs):
        self.create_client(*args, **kwargs)
        self.subscribe_to_topic(topic="{}channel/#".format(self.__prefix))
