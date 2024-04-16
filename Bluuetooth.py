from pyblue import bluetooth
import time
import serial 

# Bluetooth MAC address of the HC-05 module
class Bluetooth_device():
    def __init__(self):
        self.hc05_mac_address = '00:00:13:10:40:E6'  # Replace with your HC-05's MAC address

    def send_data_over_bluetooth(self,data):
        try:
            # Connect to HC-05 module
            socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            socket.connect((self.hc05_mac_address, 1))

            # Send data
            socket.send(data)
            print("Data sent successfully over Bluetooth")

            # Close connection
            socket.close()
        except Exception as e:
            print("Error sending data over Bluetooth:", e)

    def read_device_data(self):
        # Example function to read data from connected devices
        # Modify this function according to your setup
        data_to_send = [0, 1, 0, 1, 1]  # Example data
        return data_to_send

    def receive_data_from_bluetooth(self):
        try:
            # Connect to HC-05 module
            socket = self.bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            socket.connect((self.hc05_mac_address, 1))

            # Receive data
            data = socket.recv(1024)
            print("Received data:", data.decode())

            # Close connection
            socket.close()
        except Exception as e:
            pass
            # print("Error receiving data from Bluetooth:", e)


    # def main(self):
    #     while True:
    #         data_to_send = self.read_device_data()
    #         self.send_data_over_bluetooth(data_to_send)
    #         time.sleep(1)  # Adjust delay as needed


# Replace 'COMX' with the COM port of your HC-05 module
HC05_COM_PORT = 'COMX'

def send_command(command):
    try:
        # Create a serial connection
        ser = serial.Serial(HC05_COM_PORT, 9600, timeout=1)
        
        # Wait for the connection to be established
        time.sleep(2)
        
        # Send the command
        ser.write(command.encode())
        
        # Close the serial connection
        ser.close()
        
        print("Command '{}' sent successfully.".format(command))
    except Exception as e:
        print("Error:", e)

# Example command to send
command = 'F'  # Replace 'A' with your desired command

send_command(command)
