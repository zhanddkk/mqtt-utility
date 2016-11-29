import paho.mqtt.client as mqtt
import cbor
from simulator.core.PayloadPackage import PayloadPackage


class DatagramServer:
    def __init__(self, datagram_manager):
        import os
        import threading
        self.__id = str(os.getppid()) + str(threading.get_ident())

        self.instance = mqtt.Client(self.__id, userdata=self)
        self.instance.on_message = self.mqtt_on_message
        self.instance.on_connect = self.mqtt_on_connect
        self.instance.on_publish = self.mqtt_on_publish
        self.instance.on_disconnect = self.mqtt_on_disconnect
        self.broker = 'localhost'
        self.port = 1883

        self.is_running = False
        self.datagram_manager = datagram_manager

        self.publish_lock = threading.Lock()

        self.record_message_callback = None
        self.record_message_user_data = None

        pass

    def run(self):
        try:
            self.instance.connect(self.broker, self.port, 60)
            self.instance.reconnect()
            self.instance.loop_start()
            return True
        except ConnectionRefusedError as e:
            print('ERROR:', e)
            self.is_running = False
            return False
        except TimeoutError as e:
            print('ERROR:', e)
            self.is_running = False
            return False
            pass

    def stop(self):
        self.instance.disconnect()
        self.instance.loop_stop(force=False)
        self.is_running = False
        pass

    def publish(self, package_msg):
        if self.is_running is False:
            print('WARNING:', 'The server is not running')
            return False
        self.publish_lock.acquire()
        hash_id = package_msg.hash_id
        instance = package_msg.device_instance_index - 1
        dg = self.datagram_manager.get_datagram(hash_id)
        if dg is None:
            print('ERROR:', 'Can\'t find any datagram')
            self.publish_lock.release()
            return False
        try:
            d = dg.data_list[instance]
        except IndexError:
            print('ERROR:', 'Can\'t find the data at datagram')
            self.publish_lock.release()
            return False
            pass

        try:
            payload = cbor.dumps(package_msg.dumps())
        except TypeError as e:
            print('ERROR:', e)
            self.publish_lock.release()
            return False
            pass
        rc = self.instance.publish(d.topic, payload)
        if rc[0] == mqtt.MQTT_ERR_SUCCESS:
            d.send_value(package_msg.value)
            ret = True
            pass
        else:
            print('WARNING:', 'Publish failed', rc)
            ret = False
        self.publish_lock.release()
        return ret
        pass

    def subscribe(self, topic):
        if self.is_running is False:
            print('WARNING:', 'The server is not running')
            return
        self.instance.subscribe(topic, 0)
        pass

    def mqtt_on_connect(self, mqttc, obj, flags, rc):
        print("connect rc: " + str(rc))
        self.is_running = True
        self.instance.subscribe('UPS_System/#', 0)

    def mqtt_on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        package_msg_cbor = cbor.loads(msg.payload)
        package_msg = PayloadPackage()
        if (self.record_message_callback is not None) and (not msg.topic.startswith('$sys')):
            msg_str = 'topic   : ' + msg.topic
            msg_str += '\nqos     : ' + str(msg.qos)
            msg_str += '\nretain  : ' + str(msg.retain)
            msg_str += '\npayload : ' + str(package_msg_cbor)
            self.record_message_callback(self.record_message_user_data, msg_str)
            pass

        if package_msg.loads(package_msg_cbor) is True:
            self.datagram_manager.on_message(msg.topic, package_msg)
            pass

    def mqtt_on_publish(self, mqttc, obj, mid):
        print("publish mid: " + str(mid))

    def mqtt_on_disconnect(self, mqttc, obj, rc):
        print("disconnect rc: " + str(rc))
        pass
    pass

if __name__ == '__main__':
    string_function = '''
def user_function(argc, argv):
    if argc is None:
        argc = 0
    argc += 1
    print(argc, argv)
    return argc'''
    from simulator.core.DatagramManager import DatagramManager
    from simulator.core.Repeater import Repeater
    import time

    dgm = DatagramManager()
    dgm.import_csv('../datadictionarysource/default_data_dictionary.CSV')
    server = DatagramServer(dgm)
    server.run()
    i = 0
    package = PayloadPackage()
    rep = Repeater(server, 0.1)
    rep.start()

    package.device_instance_index = 1
    while True:
        package.value = i
        # server.instance.publish('test', 'string')
        if i == 5:
            package.hash_id = 0x2AACED6A
            dg = dgm.get_datagram(package.hash_id)
            d = dg.data_list[0]
            d.repeater_info.tagger_count = 10
            d.repeater_info.exit_times = 15
            d.repeater_info.user_function_str = string_function
            rep.append_data([package.hash_id, 0], package)
            pass
        if i == 20:
            package.hash_id = 0x7641BE11
            dg = dgm.get_datagram(package.hash_id)
            d = dg.data_list[0]
            d.repeater_info.tagger_count = 15
            d.repeater_info.exit_times = 20
            d.repeater_info.user_function_str = string_function
            rep.append_data([package.hash_id, 0], package)
            pass
        if i > 60:
            rep.stop()
            server.stop()
            break
        i += 1
        time.sleep(1)
        pass
    print('ok')
    pass
