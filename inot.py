import pyinotify
from time import sleep
from time import time
from datetime import datetime
from os import system

source = '/home/vf-talent/Dropbox/Camera Uploads'
target_parent = '/home/vf-talent/Purgatory/Dropbox/'
seconds = -1
last_time = None
changed = set()



def fs_untouched_5():
    global seconds
    if seconds > 0:
        print("sleep" + str(seconds))
        sleep(1)
        if seconds > 0:
            seconds -= 1
            return fs_untouched_5()
        else:
            return False
    if seconds == 0:
        move_command()
    else:
        return False


def move_command():
    print("moving")
    command = 'cp'
    src = '/home/vf-talent/Dropbox/Camera\ Uploads/*'
    target = target_parent+datetime_to_name()
    print target
    system('mkdir '+ target)
    system(" ".join([command, src, target]))


def datetime_to_name():
    dt = datetime.now()
    dt = str(dt)
    dt = dt.replace(" ", "_")
    dt = dt.split(".")
    dt = dt[0] + "/"
    return dt

def pathname_is_file(p):
    """Check if p is a pathname to a file. """
    splitname = p.split("/")
    #print(splitname)
    if splitname[-1] == "Camera Uploads":
        return (False)
    else:
        return (True)



class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_ACCESS(self, event):
        pass
        #print "ACCESS event:", event.pathname

    def process_IN_ATTRIB(self, event):
        pass
        # print "ATTRIB event:", event.pathname

    def process_IN_CLOSE(self, event):
        global seconds,last_time
        print "CLOSE event:", event.pathname
        isfile = pathname_is_file(event.pathname)
        if isfile:
            pass
            changed.add(event.pathname)
            print ("\n", changed)
        now_time = time()
        if not last_time or last_time - now_time > 60:
            last_time = now_time
            if not isfile:
                seconds = 5
                fs_untouched_5()


    def process_IN_CLOSE_WRITE(self, event):
        pass
        # print "CLOSE_WRITE event:", event.pathname

    def process_IN_CREATE(self, event):
        pass
        # print "CREATE event:", event.pathname

    def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname

    def process_IN_MODIFY(self, event):
        pass
        # print "MODIFY event:", event.pathname

    def process_IN_OPEN(self, event):
        global seconds
        seconds = -1
        pass
        # print "OPEN event:", event.pathname

def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch(source, pyinotify.ALL_EVENTS, rec=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

"""
def main():
    # Instantiate a new WatchManager (will be used to store watches).
    wm = pyinotify.WatchManager()
    # Associate this WatchManager with a Notifier (will be used to report and
    # process events).
    notifier = pyinotify.Notifier(wm)
    # Add a new watch on /tmp for ALL_EVENTS.
    wm.add_watch(source, pyinotify.ALL_EVENTS)
    # Loop forever and handle events.
    notifier.loop()"""


if __name__=="__main__":
    # import IPython; IPython.embed()
    main()
