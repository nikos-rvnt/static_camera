import math
import socket
import time
#import threading
#from multiprocessing import Process

UDP_IP = "192.168.2.233"
UDP_PORT = 5004

class Tonbo():

	def __init__( self, Zoom = 4, Brightness = 0, Gain = 0, initTheta  = 141,
				Latitude =  38.101849, Longitude =  21.345674):
		
		#self.setThermalZoom(Zoom)
		self.setThermalBrightness(0x7) # brghtns
		self.setThermalGain(0x16) # highest gain contrast
		#self.setThermalFocusFar()
		
		self.initTheta = initTheta
		self.Latitude = Latitude
		self.Longitude = Longitude

	def resetOptical2Default( self):
		self.sendToCam([ 255, 1, 0, 0x29, 0x00, 0x00])

	def resetThermal2Default( self):
		self.sendToCam([ 255, 2, 0, 0x29, 0x00, 0x00])

	def sendToCam( self, message1):
		message1.append((sum(message1)+1)%256)
		encodedMessage1 = bytes(message1)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(encodedMessage1, (UDP_IP, UDP_PORT))

    # turns off Auto Gain Control 
	def turnOffAGC( self):
		self.sendToCam([ 255, 2, 0, 0x2f, 0x00, 0x00])
		
    # turns on Auto Gain Control Mode 1 
	def turnOnAGC_1( self):
		self.sendToCam([ 255, 2, 0, 0x2f, 0x00, 0x01])

    # turns on Auto Gain Control Mode 2
	def turnOnAGC_2( self):
		self.sendToCam([ 255, 2, 0, 0x2f, 0x00, 0x02])

    # set brightness for theral camera - values: 0-62
	def setThermalBrightness( self, brightness):
		self.sendToCam([ 255, 2, 0, 0x7d, brightness, 0x00])

    # set gain for thermal camera - values: 0-62
	def setThermalGain( self, gain):
		self.sendToCam([ 255, 2, 0, 0x3f, gain, 0x00])

	def setThermalFocusFar(self):
		self.sendToCam([ 255, 2, 0x00, 0x80, 0x00, 0x00]) 

	def setThermalFocusNear(self):
		self.sendToCam([ 255, 2, 0x01, 0x00, 0x00, 0x00])

    # returns thermal cam digital zoom
	def getThermalZoom( self):

		import binascii        
		message2 = [ 255, 2, 0, 0x61, 0x00, 0x00, 0x63]
		encodedMessage2 = bytes(message2)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(encodedMessage2, (UDP_IP, UDP_PORT))
		a = sock.recv(7)
		b = binascii.hexlify(a)
		#print(b)
		Zoom = 0.01*(int(int(b,16)/pow(16,2))%pow(16,4))

		return Zoom

    # sets optical cam zoom
	def setThermalZoom( self, comval):
		lsb = int((comval*100)%256)
		msb = int((comval*100)/256)
		self.sendToCam([ 255, 2, 0, 0x5F, msb, lsb]) 

    # returns optical cam 
	def getZoom(self):

		import binascii        
		message2 = [255, 1, 0, 0x61, 0x00, 0x00, 0x62]
		encodedMessage2 = bytes(message2)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(encodedMessage2, (UDP_IP, UDP_PORT))
		a = sock.recv(7)
		b = binascii.hexlify(a)
		#print(b)
		Zoom = 0.01*(int(int(b,16)/pow(16,2))%pow(16,4))

		return Zoom
    
    # sets optical cam zoom
	def setZoom( self, comval):
		lsb = int((comval*100)%256)
		msb = int((comval*100)/256)
		self.sendToCam([ 255, 1, 0, 0x5F, msb, lsb]) 

	def setPanPos( self, ang):
		lsb = int((ang*100)%256)
		msb = int((ang*100)/256)
		self.sendToCam([255,1,0,0x4b, msb, lsb])
		
	def getPanPos(self):
		import binascii
		message2= [255, 1, 0, 0x51, 0, 0, 0x52]
		encodedMessage2 = bytes(message2)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(encodedMessage2, (UDP_IP, UDP_PORT))
		a = sock.recv(7)
		b = binascii.hexlify(a)
		#print(b)
		Pan = 0.01*(int(int(b,16)/pow(16,2))%pow(16,4))
		#print(Pan)
		return Pan
    
	def setTiltPos( self, ang):
		lsb = int((ang*100)%256)
		msb = int((ang*100)/256)
		self.sendToCam([0xFF,0x0,0x0,0x4d, msb, lsb])

	def getTiltPos(self):
		import binascii
		message2= [255, 1, 0, 0x53, 0, 0, 0x54]
		encodedMessage2 = bytes(message2)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(encodedMessage2, (UDP_IP, UDP_PORT))
		a = sock.recv(7)
		b = binascii.hexlify(a)
		Tilt = 0.01*(int(int(b,16)/pow(16,2))%pow(16,4))
		return Tilt

	def setZeroPos(self):
		self.sendToCam([0xFF,0x1,0x0,0x49, 0x0, 0x0])

	def StopRotation(self):
		self.sendToCam([255, 1, 0, 0, 0, 0])

	def MoveLeft( self, speed):
		self.sendToCam([255, 1, 0, 4, speed, 0])

	def MoveRight( self, speed):
		self.sendToCam([255, 1, 0, 2, speed, 0])

	def stopAllAction(self):
		self.sendToCam([ 255, 1, 0, 0, 0, 0])

	def getCoordinates(self, D, Pan):
        
		import numpy as np
		import math
		
		r_earth = 6378
		R = Pan - self.initTheta
		dx = D * np.cos(math.radians(R))
		dy = D * np.sin(math.radians(R))

		new_latitude  = self.Latitude  + (dx / r_earth) * (180 / np.pi)
		new_longitude = self.Longitude - (dy / r_earth) * (180 / np.pi) / np.cos(self.Latitude * np.pi/180);
		
		return new_latitude, new_longitude

	def imCoords2Angles( self, x, y):
		
		a1 = math.atand((x - 315.8608),3.5989)*180/pi
		a2 = math.atand((x - 451.5614),4.2493)*180/pi
		return(a1,a2)

