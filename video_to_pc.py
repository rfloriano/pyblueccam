import appuifw
import socket
import e32
import camera

def bt_connect():
    global sock
    sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
    target=''
    if not target:
        address,services=socket.bt_discover()
        if len(services)>1:
            import appuifw
            choices=services.keys()
            choices.sort()
            choice=appuifw.popup_menu([unicode(services[x])+": "+x for x in choices],u'Choose port:')
            target=(address,services[choices[choice]])
        else:
            target=(address,services.values()[0])
    sock.connect(target)

def redraw(r=(), img=None):
    if img:
        appuifw.app.body.blit(img)

def cb(img, bpp=1):
    img.save('D:\\pixels.jpg', bpp=24, quality=20)
    f = open('D:\\pixels.jpg', "rb")
    bt_send_something(f.read())
    f.close()
    redraw(img=img)

def bt_send_something(something):
    if something:
        sock.send(something)

def exit():
    camera.stop_finder()
    app_lock.signal()

appuifw.app.title = u"video to pc"

appuifw.app.exit_key_handler = exit

bt_connect()
appuifw.app.body = appuifw.Canvas(redraw)
camera.start_finder(cb)

app_lock = e32.Ao_lock()
app_lock.wait()
