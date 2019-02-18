# Proof of Concept for Rx UDP from XPLANE using Python 
# iflysims.com

# Need to tidy up at the moment every incoming UDP package is processed regardless of change
# Implement flag if package has changed
# Need to implement GPIO for Pi 




import socket
import struct
import RPi.GPIO as GPIO

# Local address of Pi
# Get the Local IP Address 
UDP_IP = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
UDP_PORT = 49005        # local port to listen - default xplane port
packetSize = 1


sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(11, GPIO.OUT)        # Setup PIN 11 aka GPIO 17
WBrakePin = 11                  # Define Pin 11 for Wheel Brakes 









while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    packetSize = len(data) # Set the packetSize to be the lengh of the data sentence expect 41 Bytes
    print("\nByte Length of Message :", len(data) , "\n")  # returns the size of the packet
    print("\nByte Length of Message from PS:", packetSize , "\n") 
    
    # This is to esnure the finite struc.unpack will work as it must be 41 Bytes
    if packetSize == 41:
        #print("Message :", struct.unpack('<41B',data) , "\n")  # 41 Bytes
        string = struct.unpack_from('<4s',data, 0)              # first 4 Bytes
        #print(string)
        NumPacket = 1
        if string == (b'DATA',):   # 
            #print("\nWORD DATA \n") # Test that i am in the loop
            offset = 5
            #print("Message Part :", offset, struct.unpack_from('B',data, offset) , "\n")  # 
            DataSet =  struct.unpack_from('B',data, 5)    # The Data Set is Byte 5
            #print("Data set expect 14 :" , DataSet)
            offset = 16
            #print("Message Part :", offset, struct.unpack_from('B',data, offset) , "\n")  # 
            DataElem16 = struct.unpack_from('B',data, 16)   # 16th Element
            #print("Message Part for Element16 :", DataElem16 , "\n")  # 

    else :
        #print("Data out of Range", "\n")
        NumPacket = 99

    if DataSet == (14,):        # X-Plane Data Set 14 gear/breakes
        #print("\nI am in the loop for Dataset 14 \n") # Test that i am in the loop
        if DataElem16 == (0,): # Wheel Brakes
            WheelBrakes = 0
            GPIO.output(WBrakePin,GPIO.LOW)
            print("\nWheel Brakes OFF \n") 
        if DataElem16 == (63,):
            WheelBrakes = 1
            GPIO.output(WBrakePin,GPIO.HIGH)
            print("\nWheel Brakes ON\n") 
        
            

        

 
 
        


    




    


