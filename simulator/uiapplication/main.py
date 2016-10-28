from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
from PyQt5.QtWidgets import QApplication, QMainWindow
from simulator.uiform.SimulatorUI import Ui_SimulatorUI
from simulator.datadictionary.DatagramManager import DatagramManager
import paho.mqtt.client as data_client
import datetime
import cbor


class TreeItem(object):
    def __init__(self, data=[], parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            self.parentItem.childItems.index(self)

        return 0

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value

        return True


class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem()
        self.import_data(data)

    def import_data(self, data):
        pass

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result


class DatagramManagerThread(QThread):
    signal_connect = pyqtSignal(list)
    signal_publish = pyqtSignal(list)
    signal_subscribe = pyqtSignal(list)
    signal_log = pyqtSignal(list)
    signal_message = pyqtSignal(list)

    is_connected = False

    def __init__(self, datagram_manager, parent=None):
        super(DatagramManagerThread, self).__init__(parent)
        self.dgm = datagram_manager
        self.client = None
        pass

    def create_client(self):
        self.client = data_client.Client(self.dgm.client_name, userdata=self)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_log = self.on_log
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.dgm.data_broker, 1883, 60)
            self.is_connected = True
        except:
            print("Can't connect", self.dgm.data_broker)
            self.is_connected = False

    @staticmethod
    def on_connect(client, obj, flag, rc):
        print("OnConnect, rc: " + str(flag) + " " + str(rc))
        f_send_signal = obj.send_update_signal
        f_send_signal(obj.signal_connect, [flag, rc])

    @staticmethod
    def on_publish(client, obj, mid):
        print("OnPublish, mid: " + str(mid))
        f_send_signal = obj.send_update_signal
        f_send_signal(obj.signal_publish, [mid])

    @staticmethod
    def on_subscribe(client, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
        f_send_signal = obj.send_update_signal
        f_send_signal(obj.signal_subscribe, [mid, granted_qos])

    @staticmethod
    def on_log(client, obj, level, string):
        print("Log:" + string)
        f_send_signal = obj.send_update_signal
        f_send_signal(obj.signal_log, [level, string])

    @staticmethod
    def on_message(client, obj, msg):
        current_time = datetime.datetime.now()
        str_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(str_current_time + ": " + msg.topic + " " + str(msg.qos) + "{" + str(msg.payload) + "}")
        f_send_signal = obj.send_update_signal
        f_send_signal(obj.signal_message, [msg.topic, msg.qos, msg.payload])

    def run(self):
        self.client.loop_forever()
        print("Exit the " + self.dgm.client_name + " thread")
        pass

    def stop(self):
        self.client.disconnect()

    def send_update_signal(self, signal, dat):
        self.dgm
        signal.emit(dat)
        pass

'''
E_PAYLOAD_TYPE = 0
E_PAYLOAD_VERSION = 1
E_HASH_ID = 2
E_PRODUCER_MASK = 3
E_ACTION = 4
E_TIMESTAMP_SECOND = 5
E_TIMESTAMP_MS = 6
E_DEVICE_INSTANCE_INDEX = 7
E_DATA_OBJECT_REFERENCE_TYPE = 8
E_DATA_OBJECT_REFERENCE_VALUE = 9
E_VALUE = 10
'''


class MainApp(QMainWindow):
    E_PAYLOAD_TYPE = 0
    E_PAYLOAD_VERSION = 1
    E_HASH_ID = 2
    E_PRODUCER_MASK = 3
    E_ACTION = 4
    E_TIMESTAMP_SECOND = 5
    E_TIMESTAMP_MS = 6
    E_DEVICE_INSTANCE_INDEX = 7
    E_DATA_OBJECT_REFERENCE_TYPE = 8
    E_DATA_OBJECT_REFERENCE_VALUE = 9
    E_VALUE = 10

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.ui = Ui_SimulatorUI()
        self.ui.setupUi(self)

        self.datagram = DatagramManager()
        self.datagram.client_name = "DatagramClient"
        self.datagram.data_broker = "localhost"

        self.datagram_thread = DatagramManagerThread(self.datagram)
        self.datagram_thread.create_client()
        self.datagram_thread.start()

        self.load_csv('../datadictionarysource/default_data_dictionary.csv')
        self.data_dictionary = TreeModel(None)
        self.import_datagram(self.data_dictionary, self.datagram, ("Topic Node", "Value", "Hash ID"))

        self.ui.treeViewDataDictionary.setModel(self.data_dictionary)
        self.ui.treeViewDataDictionary.selectionModel().selectionChanged.connect(
            self.update_datagram_property_display)

        self.datagram_thread.signal_message.connect(self.update_value)

    def update_value(self, message_list):
        msg = cbor.loads(message_list[-1])
        dg = self.datagram.datagram_dict[msg[self.E_HASH_ID]]
        dev_index = msg[self.E_DEVICE_INSTANCE_INDEX] - 1
        dg.set_value(msg[self.E_VALUE], dev_index)
        row = self.datagram.get_row(msg[self.E_HASH_ID], dev_index)
        model = self.ui.treeViewDataDictionary.model()
        index = model.index(row, 0)
        # index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        child = model.index(row, 1, model.parent(index))
        model.setData(child, str(msg[self.E_VALUE]), Qt.EditRole)
        self.ui.treeViewDataDictionary.closePersistentEditor(index)

        # index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        # model = self.ui.treeViewDataDictionary.model()
        # a = model.parent(index)
        # child = model.index(index.row(), 1, a)
        # model.setData(child, self.ui.textEditValue.toPlainText(), Qt.EditRole)
        # self.ui.treeViewDataDictionary.closePersistentEditor(index)
        pass

    def load_csv(self, filename=""):
        self.datagram.import_datagram(filename)
        pass

    # @staticmethod
    def import_datagram(self, tree_model=TreeModel(None), dg_m=DatagramManager(), header=()):
        tree_model.rootItem = TreeItem(header)
        parent = [tree_model.rootItem]

        for this_index in dg_m.index_list:
            dg = dg_m.get_datagram(this_index[0])
            item = TreeItem([dg.get_topic(this_index[1]), dg.data_property.default, this_index[0], this_index[1]],
                            parent[-1])
            self.datagram_thread.client.subscribe(dg.get_topic(this_index[1]), 0)
            parent[-1].appendChild(item)
        pass

    @pyqtSlot()
    def on_pushButtonPublish_clicked(self):
        sender = self.sender()
        index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        row = index.row()
        if row >= 0:
            # topic = index.sibling(row, 0).data()
            # hash_id = index.sibling(row, 2).data()
            model = self.ui.treeViewDataDictionary.model()
            item = model.getItem(index)
            topic = item.itemData[0]
            hash_id = item.itemData[2]
            dev_index = item.itemData[3]
            try:
                payload = {
                    self.E_PAYLOAD_TYPE: 0,
                    self.E_PAYLOAD_VERSION: 0,
                    self.E_HASH_ID: hash_id,
                    self.E_PRODUCER_MASK: 0,
                    self.E_ACTION: 0,
                    self.E_TIMESTAMP_MS: 0,
                    self.E_TIMESTAMP_SECOND: 0,
                    self.E_DEVICE_INSTANCE_INDEX: dev_index + 1,
                    self.E_VALUE: "I am zhan lei"
                }
                payload = cbor.dumps(payload)
                self.datagram_thread.client.publish(topic, payload)
                result = "Publish OK"
            except ValueError:
                result = "Publish Failed"
        else:
            result = "No Topic"

        # index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        # model = self.ui.treeViewDataDictionary.model()
        # a = model.parent(index)
        # child = model.index(index.row(), 1, a)
        # model.setData(child, self.ui.textEditValue.toPlainText(), Qt.EditRole)
        # self.ui.treeViewDataDictionary.closePersistentEditor(index)
        self.statusBar().showMessage(sender.text() + ' was pressed: ' + result)

    def update_datagram_property_display(self):
        current_index = self.ui.treeViewDataDictionary.selectionModel().currentIndex()
        row = current_index.row()
        topic = current_index.sibling(row, 0).data()
        hash_id = current_index.sibling(row, 2).data()
        dg = self.datagram.get_datagram(hash_id)
        self.ui.treeWidgetDataInfo.topLevelItem(0).setText(1, dg.data_property.sub_system)
        self.ui.treeWidgetDataInfo.topLevelItem(1).setText(1, dg.data_property.data_path)
        self.ui.treeWidgetDataInfo.topLevelItem(2).setText(1, dg.data_property.name)
        self.ui.treeWidgetDataInfo.topLevelItem(3).setText(1, dg.data_property.description)
        self.ui.treeWidgetDataInfo.topLevelItem(4).setText(1, dg.data_property.type)
        self.ui.treeWidgetDataInfo.topLevelItem(5).setText(1, dg.data_property.format)
        self.ui.treeWidgetDataInfo.topLevelItem(6).setText(1, str(dg.data_property.max_size))
        self.ui.treeWidgetDataInfo.topLevelItem(7).setText(1, dg.data_property.default)
        self.ui.treeWidgetDataInfo.topLevelItem(8).setText(1, str(dg.data_property.min))
        self.ui.treeWidgetDataInfo.topLevelItem(9).setText(1, str(dg.data_property.max))
        str_list = []
        str_tmp = ""
        choice_list = dg.data_property.choice_list
        if choice_list != {}:
            for (k, d) in choice_list.items():
                str_list.append(k + "\t: " + str(d))
            str_list.sort()
            for s in str_list:
                str_tmp = str_tmp + s + '\n'
            str_tmp = str_tmp.rstrip('\n')
        self.ui.treeWidgetDataInfo.topLevelItem(10).setText(1, str_tmp)
        self.ui.treeWidgetDataInfo.topLevelItem(11).setText(1, dg.data_property.scale_unit)
        self.ui.treeWidgetDataInfo.topLevelItem(12).setText(1, str(dg.data_property.precision))
        self.ui.treeWidgetDataInfo.topLevelItem(13).setText(1, str(dg.data_property.is_alarm))
        self.ui.treeWidgetDataInfo.topLevelItem(14).setText(1, str(dg.data_property.is_evt_log))

        self.ui.treeWidgetDataInfo.topLevelItem(15).setText(1, str(dg.data_property.producer))
        self.ui.treeWidgetDataInfo.topLevelItem(16).setText(1, str(dg.data_property.consumer))

        self.ui.treeWidgetDataInfo.topLevelItem(17).setText(1, hex(dg.data_property.hash_id))
        self.statusBar().showMessage("Clicked: " + topic + " @ " + hex(hash_id))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
