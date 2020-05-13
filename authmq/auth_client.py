import hashlib
import json
import secrets

from authmq.auth_base import AuthException, AuthBase
from authmq.globals import DEFAULT_BROKER_HOST, DEFAULT_BROKER_PORT


class AuthClientException(AuthException):
    pass


class AuthClient(AuthBase):
    def __init__(self, username, password, host=DEFAULT_BROKER_HOST,
                 port=DEFAULT_BROKER_PORT, topic_prefix="", *args, **kwargs):
        super().__init__(host=host, port=port, *args, **kwargs)
        self.__prefix = "{}/".format(topic_prefix) if topic_prefix else ""
        self.__userid = username
        self.__pwd = password
        self.__secret = None
        self.__receive_msg_handle = lambda msg : msg
        self.set_exception(e_class=AuthClientException)

    def client_setup(self, *args, **kwargs):
        self.create_client(*args, **kwargs)

    def authenticate_myself(self):
        if not self.is_client_created():
            raise AuthClientException(reason="client_setup needs to be done before "
                "authenticating")
        __topic = "{}channel/{}".format(self.__prefix, self.__userid)
        self.__client.message_callback_remove(sub=__topic)
        self.__client.unsubscribe(__topic)
        self.__client.message_callback_add(sub=__topic, callback=self.__handle_salt)
        self.__client.subscribe(__topic)
        self.__client.publish(topic="{}channel/auth", payload=self.__userid)

    def __handle_salt(self, _client, _userdata, _msg):
        if not isinstance(_msg.topic, str):
            self.authenticate_myself()
            raise AuthClientException(reason="Unable to recover userID while "
                "examining salt!")

        __userid = _msg.topic.split("/")[-1]
        if __userid != self.__userid:
            self.authenticate_myself()
            raise AuthClientException(reason="The userID retrieved did not match"
                " with our userID!")

        try:
            __payload = json.loads(_msg.payload.decode("utf-8"))
        except json.decoder.JSONDecodeError:
            self.authenticate_myself()
            raise AuthClientException(reason="Invalid JSON response received!")

        __status = __payload.get("status", None)
        __salt = __payload.get("salt", None)
        __code = __payload.get("code", None)
        if not __status:
            self.authenticate_myself()
            raise AuthClientException(reason="Invalid JSON response received!")
        elif __status == "DENY":
            _client.disconnect()
            raise AuthClientException(reason="Auth Server denied user {}".format(__userid))
        elif __status == "OK":
            self.__secret = hashlib.sha256("{}{}{}".format(
                __salt, __userid, self.__pwd).encode()).hexdigest()
            __send_topic = "{}channel/server/{}".format(self.__prefix,
                hashlib.sha256("{}{}".format(self.__secret, __code).encode()).hexdigest())
            _new_code = secrets.token_hex(10)
            __listen_topic = "{}channel/client/{}".format(self.__prefix,
                hashlib.sha256("{}{}".format(self.__secret, _new_code).encode()).hexdigest())
            _client.message_callback_add(sub=, callback=)
        _client.message_callback_remove(sub=_msg.topic)
        _client.unsubscribe(_msg.topic)

    def send_message(self):
        pass

    def set_receive_message_handle(self, f):
        self.__receive_msg_handle = f
