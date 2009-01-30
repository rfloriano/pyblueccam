#!/usr/bin/env python

from bluetooth import *
from thread import start_new_thread
from select import select
from eagle import *

SIZE=1024*8

def create_server():
	server_sock = BluetoothSocket(RFCOMM)
	server_sock.bind(("",PORT_ANY))
	port = server_sock.getsockname()[1]

	print 'Waiting connection...'
	server_sock.listen(1)
	advertise_service( server_sock, "Serial Port2", 
		                            service_classes = [ SERIAL_PORT_CLASS ], 
		                            profiles = [ SERIAL_PORT_PROFILE ] )
	client_sock, client_info = server_sock.accept()
	print 'ok, from', client_info
	return client_sock
img = ''
i = 0 
def recebe(s):
	global img, i, t
	data = s.recv(SIZE)
	if 'conectado' in data:
		return
	if data.startswith('\xff'):
		img = ""
	img += data
	if  data.endswith('\xff\xd9'):
		f = open('/tmp/pixels.jpg', 'wb')	
		f.write(img)
		f.close()
		t += time.time()

		i+=1
  
def bt_server_mainloop():
    sockets = [create_server()]
    while True:
        r, w, e = select(sockets, [], [])
        for s in r:
            recebe(s)

def start_server(app, wid):
    start_new_thread(bt_server_mainloop, ())

def put_img(app):
    try:
        im=Image(filename='/tmp/pixels.jpg')
    except Exception, e:
        pass
    else:
        app['cv'].draw_image(im)
    return True
 
def capture(app, widi, filename='foto.jpg'):
    im = app['cv'].get_image()
    im.save(filename)

app = App(
    title='PyCam - S60',
    author='Bruno Gola',
    version='0.1',
    license='GPLv3',
    description='Mostra imagens capturadas pelo client em um celular serie 60 e transferida via bluetooth',
    window_size=(301, 355),
    center=(
            Canvas(id='cv', width=240, height=180, bgcolor='white'),
            Group(  id='botoes', label=None, border=None,
                    children=(  Button(id='botao_sv', label='Start server!', callback=start_server),
                                Button(id='botao_img', label='Capture image', callback=capture),
                    ),
            ),
            AboutButton(),
    )
)
import time
t = time.time()
app.timeout_add(50, put_img)
run()
