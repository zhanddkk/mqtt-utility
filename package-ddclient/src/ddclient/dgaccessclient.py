import cbor
import paho.mqtt.client as datagram_client


class DatagramAccessClient:
    def __init__(self, client_name='', datagram_manager=None):
        import threading
        import uuid
        self.__id = uuid.uuid4().hex[0:8]
        self.__name = client_name
        self.__client_id = 'Simulator_{name}_{_uuid}'.format(name=self.__name, _uuid=self.__id)

        self.__user_password = {
            "Simulator1": "3279",
            "Simulator2": "be95",
            "Simulator3": "98d7",
            "Simulator4": "9f02",
        }
        self.__instance = datagram_client.Client(self.__client_id, userdata=datagram_manager)
        self.__instance.username_pw_set(username='Simulator4', password='9f02')
        self.__instance.on_message = self.__on_message
        self.__instance.on_connect = self.__on_connect
        self.__instance.on_publish = self.__on_publish
        self.__instance.on_disconnect = self.__on_disconnect
        self.__broker_ip = 'localhost'
        self.__broker_ip_port = 1883

        self.__is_running = False
        self.__publish_lock = threading.Lock()

        pass

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def client_full_id(self):
        return self.__client_id
        pass

    @property
    def is_running(self):
        return self.__is_running

    @property
    def ip(self):
        return self.__broker_ip

    @property
    def port(self):
        return self.__broker_ip_port

    def start(self):
        try:
            if self.__is_running:
                self.__instance.reconnect()
                pass
            else:
                self.__instance.connect(self.__broker_ip, self.__broker_ip_port, 60)
            self.__instance.loop_start()
            return True
        except ConnectionRefusedError as exception:
            print('ERROR:', exception)
            self.__is_running = False
            return False
        except TimeoutError as exception:
            print('ERROR:', exception)
            self.__is_running = False
            return False
        except Exception as exception:
            print('ERROR:', 'Invalid IP, Exception type = ', type(exception).__name__, exception)
            self.__is_running = False
            return False
            pass

    def stop(self):
        if self.__is_running is True:
            self.__instance.disconnect()
            self.__instance.loop_stop(force=False)
        pass

    def publish(self, package, topic, qos=0, retain=False):
        if self.__is_running is False:
            print('WARNING:', 'The client is not running')
            return False
        self.__publish_lock.acquire()
        try:
            payload = cbor.dumps(package)
        except TypeError as exception:
            print('ERROR:', exception)
            self.__publish_lock.release()
            return False
            pass
        rc = self.__instance.publish(topic, payload, qos, retain)
        if rc[0] == datagram_client.MQTT_ERR_SUCCESS:
            ret = True
            pass
        else:
            print('WARNING:', 'Publish failed', rc)
            ret = False
        self.__publish_lock.release()
        return ret
        pass

    def subscribe(self, topic, qos=0):
        if self.__is_running is False:
            print('WARNING:', 'The client is not running')
            return
        self.__instance.subscribe(topic, qos)
        pass

    def config(self, broker_address, port):
        self.__broker_ip = broker_address
        self.__broker_ip_port = port

        if self.__is_running is True:
            self.stop()
            self.start()
        pass

    def __on_connect(self, mqttc, obj, flags, rc):
        print('''[{id}]Datagram access client: connected
        |->rc = {rc}
        |->flag = {flags}'''.format(id=self.__client_id, rc=rc, flags=flags))
        self.__is_running = True
        self.__instance.subscribe('#', 0)

    def __on_message(self, mqttc, obj, msg):
        # print('''[{id}]Datagram access client: received
        # |->timestamp = {timestamp}
        # |->qos = {qos}
        # |->retain = {retain}
        # |->topic = {topic}
        # |->payload = {payload}'''.format(id=self.__client_id,
        #                                  timestamp=msg.timestamp,
        #                                  qos=msg.qos,
        #                                  retain=msg.retain,
        #                                  topic=msg.topic,
        #                                  payload=msg.payload))
        if obj is not None:
            obj.record_message(msg)
        pass

    def __on_publish(self, mqttc, obj, mid):
        # print('''[{id}]Datagram access client: published
        # |->mid = {mid}'''.format(id=self.__client_id, mid=mid))
        pass

    def __on_disconnect(self, mqttc, obj, rc):
        print('''[{id}]Datagram access client: disconnected
        |->rc = {rc}'''.format(id=self.__client_id, rc=rc))
        self.__is_running = False
        pass
    pass


if __name__ == '__main__':
    pass
