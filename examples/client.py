from authmq.auth_client import AuthClient


def received_message_checkout(msg):
    print("Received new message : {}".format(msg))


if __name__ == "__main__":
    client_obj = AuthClient(host="localhost", port=1883, topic_prefix="atman/backdoor/")
    client_obj.set_receive_message_handle(f=received_message_checkout)
    client_obj.start()

    client_obj.authenticate_myself(username="testuser", password="testpassword")
    client_obj.send_message(topic="Topic1", msg="First message")
    client_obj.send_message(topic="Topic2", msg="Second message")
    client_obj.join()
