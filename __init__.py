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
        
        self.thread = threading.Thread(None, self.loop)
        self.thread.start()
        
    def loop(self):
        last_time = time.time()
        while True:
            now = time.time()
            
            try:
                message = self.subscriber.recv()
                message = simplejson.loads(message)
            except:
                message = "undefined"
            
            #print message
            
            if  type(message).__name__=='str':
                pass
            
            elif message['type'] == "SwipeRight":
                if now > last_time + .8:
                    # Next
                    if self.shell.props.shell_player.get_playing():
                        self.shell.props.shell_player.do_next()
                    else:
                        print "Play ?"
                        self.shell.props.shell_player.play()
            
            elif message['type'] == "SwipeLeft":
                if now > last_time + .8:
                    # Previous
                    if self.shell.props.shell_player.get_playing():
                        self.shell.props.shell_player.do_next()
                    else:
                        print "Play ?"
                        self.shell.props.shell_player.play()

            # Make rhythmbox to crash :/
            elif False and message['type'] == "Move":
                if now > last_time + .05:
                    volume_relative = float(1) / float(100) * float(message['data']['y'])
                    print "change volume for " + str(volume_relative)
                    self.shell.props.shell_player.set_volume(volume_relative)

            last_time = now

