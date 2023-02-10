import network
import socket
import time
from machine import Pin
import temperature as t
import blinkOnBoardLED as blink

led = Pin("LED", Pin.OUT)

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1.5)
    
    ip = wlan.ifconfig()[0]
    
    print(f'Connected on {ip}')
    return wlan


def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


def webpage(temperature, state):
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            <form action="./refresh">
            <input type="submit" value="Refresh" />
            </form>
            </body>
            </html>
            """
    return str(html)
    

def start_server(connection):
    state = 'OFF'
    led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            led.on()
            state = 'ON'
        elif request =='/lightoff?':
            led.off()
            state = 'OFF'
        elif request =='/refresh?':
            pass
        temperature = t.getTemperature()
        html = webpage(temperature, state)
        client.send(html)
        client.close()

class Server():
    
    def serve(self,network_ssid,network_password):
        try:
            ip = connect_to_wifi(network_ssid,network_password).ifconfig()[0]
            connection = open_socket(ip)
            start_server(connection)
        except KeyboardInterrupt:
            machine.reset()
