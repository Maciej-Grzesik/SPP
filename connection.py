import serial
import re

from PyQt5.QtCore import QThread, pyqtSignal


class SerialThread(QThread):
    distance_signal = pyqtSignal(int)

    def __init__(self, port):
        super(SerialThread, self).__init__()
        self.ser = serial.Serial(port=port, baudrate=9600)
        self.running = False

    def close_connection(self):
        if self.ser.is_open:
            self.ser.close()

    def run(self):
        self.running = True
        try:
            while self.running:
                value = self.ser.readline()
                valueInString = str(value, 'UTF-8')
                distance = int(''.join(re.findall("\d", valueInString)))
                self.distance_signal.emit(distance)

        except serial.SerialException as e:
            print("Error reading serial port ", e)
        except UnicodeEncodeError as e:
            print("Error decoding serial port ", e)
        except KeyboardInterrupt:
            print("Closing connection")
        finally:
            self.close_connection()
