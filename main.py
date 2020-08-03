import serial
#import serial.tools
import serial.tools.list_ports
from enum import Enum
from time import sleep


#Végül az állapotgépet nem használtam
class StateMachine_enum(Enum):
    Start       =   0
    CEREG       =   1
    QICSGP      =   2
    QIACT       =   3
    QIOPEN      =   4
    QISEND      =   5
    TEXT        =   6
    QICLOSE     =   7
    QPOWD       =   8


#USB portra való felcsatlakozás, ha bekapcsoljuk a modult
def porting():
    y = 0
    while y != 1:                                                   #addig járatom a ciklust, amíg nem kapcsolom be a modult
        portlist = (serial.tools.list_ports.comports())             #soros porton lévő eszközök összessége
        for x in portlist:
            if x.device == "COM17":                                 #COM18-as portot nem listázza ki, viszont a Quectel modul a COM17 és COM16-ot is lefoglalja
                y = 1
    print("COM port found")
    return

def AT_COMMAND(command, modul_respond):
        serialPort.write(command)                                       #Beadott AT parancs lefuttatása
        loop_end = 1
        while loop_end:                                                 #Amíg nem kapunk választ, addig folyamatosan figyeljük a soros portot
            reading = serialPort.read(10000)
            if reading != b'':                                          #Ha nem küld üzenetet, akkor üres szöveget ne jelenítsen meg nekünk a terminálon
                print(command.decode())
                print(reading.decode())
                print(reading)                                          #debuggolásra
                #print(reading.find(modul_respond))                     #deguggolásra
                if reading.find(modul_respond) >= 0:                    #Ha kaptunk választ, ami a megadott szavakat tartalmazza, akkor kilépünk a ciklusból és mehetünk a következő AT parancsra
                    loop_end = 0



if __name__ == '__main__':
    cycles = 0
    while True:

        #SOROS PORTRA CSATLAKOZÁS
        porting()                                                                                                   #soros port keresése
        sleep(1)                                                                                                    #COM17 portot hamarabb csatlakozik, mint a COM18-as port
        if cycles == 0:                                                                                             #csak első alkalommal kell csatlakozni a soros portra
            serialPort = serial.Serial('COM18', 115200, timeout=0)


        #AT PARANCSOK
        #bájtos formában kell megadni a kiküldött parancsokat!
        #első attribútumba a kiküldendő parancsot adjuk meg (mindegyik parancs végén egy entert kell megadni)
        #második attribútum pedig a várt válaszban megtalálható szavakat adjuk meg (van, hogy a szavak sorrendje nem egyezik meg
        #                                                                           ENTERT válaszba ne adjunk meg a sorrend miatt!)
        #ha AT parancshívás közben elakad, akkor az egész kódot újra kell indítani

        app_ready = 0
        while app_ready == 0:
            reading = serialPort.read(10000)
            if reading != b'':
                print(reading)
                if reading.find(b'APP RDY') >= 0:
                    app_ready = 1
        AT_COMMAND(b'AT+CEREG=1\r\n', b'OK')
        AT_COMMAND(b'AT+QICSGP=1,1,"","","",1\r\n', b'OK')
        AT_COMMAND(b'AT+QIACT=1\r\n', b'OK')
        AT_COMMAND(b'AT+QIOPEN=1,0,"TCP","192.168.221.241",54321,0,0\r\n', b'+QIOPEN: 0,0')
        AT_COMMAND(b'AT+QISEND=0,1400\r\n', b'AT+QISEND')                                                           #akkor futtatom tovább, ha az üzenetküldés rendben volt
        AT_COMMAND(b'Entrust Root Certification Authority - G4=========================================-----BEGIN CERTIFICATE-----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-----END CERTIFICATE-----\r\n',b'+QIURC: "recv",0')
                                                                                                                    #A kiküldött 1400 bájt egy részlete a szabadon letölthető cacert.pem szabványból
        AT_COMMAND(b'AT+QICLOSE=0\r\n', b'OK')


        #MODUL LEÁLLÍTÁSA

        serialPort.write(b'AT+QPOWD\r\n')
        print("loop ended")
        cycles =+ 1
        sleep(10)






