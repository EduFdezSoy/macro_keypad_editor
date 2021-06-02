import serial
import serial.tools.list_ports
import time


def main():
    global ser

    ports = list(serial.tools.list_ports.comports())
    serialPort = '/dev/ttyACM0'

    for p in ports:
        print(p)
        if "Arduino" in p.description:
            serialPort = p[0]

    ser = serial.Serial(serialPort, 9600)


def led_on_off():
    user_input = input("\n Type on / off / quit : ")
    if user_input == "on":
        print("LED is on...")
        time.sleep(0.1)
        ser.write(b'H')
        led_on_off()
    elif user_input == "off":
        print("LED is off...")
        time.sleep(0.1)
        ser.write(b'L')
        led_on_off()
    elif user_input == "quit" or user_input == "q":
        print("Program Exiting")
        time.sleep(0.1)
        ser.write(b'L')
        ser.close()
    else:
        print("Invalid input. Type on / off / quit.")
        led_on_off()


if __name__ == '__main__':
    main()