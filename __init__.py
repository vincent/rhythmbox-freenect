import zmq
import rb
import time
import threading
import simplejson

class RhythmboxFreenectPlugin (rb.Plugin):

    def __init__(self):
        rb.Plugin.__init__(self)


    def activate(self, shell):
        self.shell = shell
        context = zmq.Context()
        self.subscriber = context.socket (zmq.SUB)
        self.subscriber.connect ("tcp://*:14444")
        self.subscriber.setsockopt (zmq.SUBSCRIBE, "event")
        
        self.last_time = time.time()
        self.last_move_position = { 'x':50, 'y':50 }
        self.thread = threading.Thread(None, self.loop)
        self.thread.start()
        
        print dir(rb.LibraryBrowser)


    def deactivate(self, shell):
        self.thread.stop()
        self.subscriber.close()
        
    def loop(self):
        while True:
            now = time.time()
            try:
                message = self.subscriber.recv()
                message = simplejson.loads(message)
            except:
                message = "undefined"
            
            if now < self.last_time + .8:
                pass
                #continue;

            print message
            
            if  type(message).__name__=='str':
                pass

            elif message['type'] == "HandClick":
                print "PlayPause ?"
                self.shell.get_player().playpause()

            elif message['type'] == "SwipeRight":
                if now > self.last_time + .8:
                    # Next
                    if self.shell.get_player().get_playing():
                        self.shell.get_player().do_next()
                    else:
                        print "Play ?"
                        self.shell.get_player().play()
            
            elif message['type'] == "SwipeLeft":
                if now > self.last_time + .8:
                    # Previous
                    if self.shell.get_player().get_playing():
                        self.shell.get_player().do_previous()
                    else:
                        print "Play ?"
                        self.shell.get_player().play()

            elif message['type'] == "SwipeUp":
                if now > self.last_time + .5:
                    self.shell.get_player().set_volume_relative(.2)

            elif message['type'] == "SwipeDown":
                if now > self.last_time + .5:
                    self.shell.get_player().set_volume_relative(-0.2)

            # Make rhythmbox to crash :/
            elif False and message['type'] == "Move":
                if now > self.last_time + .05:
                    volume_relative = float(1) / float(100) * float(message['data']['y'])
                    print "change volume for " + str(volume_relative)
                    #self.shell.get_player().set_volume(volume_relative)
                    self.shell.get_player().set_volume_relative(volume_relative)

            if type(message).__name__ != 'str':
                self.last_move_position = message['data']
            self.last_time = now

