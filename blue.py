import bluetooth

def receiveMessages():
	print('Start receiveMessages()!')
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	port = 1
	server_sock.bind(("B8:27:EB:7C:E0:A0",port)) # write raspi mac address
	server_sock.listen(1)
	client_sock,address = server_sock.accept()
	print "Accepted connection from " + str(address)
	while True:
		data = client_sock.recv(1024)
		print "received [%s]" % data
		if data == "fire":
			break

	client_sock.close()
	server_sock.close()
	print('End receiveMessages()!')

def sendMessageTo(targetBluetoothMacAddress):
	print('Start sendMessageTo()!')
	port = 1
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((targetBluetoothMacAddress, port))
	sock.send("hello!!")
	sock.close()
	print('End sendMessageTo()!')

def lookUpNearbyBluetoothDevices():
	nearby_devices = bluetooth.discover_devices()
	for bdaddr in nearby_devices:
		print str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]"

lookUpNearbyBluetoothDevices()
receiveMessages()
#sendMessageTo('A0:91:69:92:31:82')
