import os
import time
import cv2

#
# Video recorder class to create an MP4 file by adding images.
# The recorder is a simple state machine that records images passed for duration seconds after activation.
#
# This allows a triggering event to start a brief recording clip, that will automatically stop recording once duration is exceeded. (unless its reactivated)
# Calling activate_recording() when recording is already activated will reset the timer and extend the recording duration more seconds.
#
# This way you get the training few seconds after an recording event is started, and if more events come in during the duration, they can be added to the video 
#
#  resolution  default=480p, 720p, 1080p
#  path        default /tmp, location to create MP4 files
#  duration    default=10 seconds, record images added for this many seconds from when activate recording is called (it can be called multiple times to get longer clips)
#  frame_rate  default = 2, number of seconds for the frame to show in the mp4
#  trace       default=False, diagnostic print messages
#
# dvr = DVR(path=".", duration=5, trace=True)
# in while loop:
#    ...
#    if (record_event):     #if an event occurs, start recording it
#        dvr.activate_recording(10)
#    dvr.record_frame_if_active (img) # send image so its recorded if recording is active, else it no-ops
#
#  calling stop_recording is not required, but will immediately expire the duration and stop any active recording.
#
class DVR:
    def __init__(self, resolution='480p', path='/tmp', frame_rate=2, duration=10, trace=False):
        super(DVR, self).__init__()
        RESOLUTION = {'1080p' : (1920, 1080), '720p' : (1280, 720), '480p' : (858, 480)}
        if resolution not in RESOLUTION:
            raise Exception("Invalid resolution")
        self.resolution = RESOLUTION[resolution]
        self.fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        self.frame_rate = frame_rate
        self.video_writer = None
        self.path = path
        self.start_time = 0
        self.default_duration = duration   # default duration is 10 seconds
        self.clip_duration = duration
        self.trace = trace
        if self.trace:
            print (vars(self))
        
    # Open a file to write frames into
    def __start_writer (self):
        if self.video_writer is None:
            fname = os.path.join (self.path, 'recording-' + time.strftime("%Y-%m-%d--%H-%M-%S") + '.mp4') 
            self.video_writer = cv2.VideoWriter(fname, self.fourcc, self.frame_rate, self.resolution)
            self.start_time = time.time()
            if self.trace:
                print ('__start_writer: store in ', fname)

    # Record a frame IF the record_count is set
    def record_frame_if_active (self, frame):
        if time.time() < self.start_time + self.clip_duration:
            if self.trace:
                print ("record_frame_if_active: write image")        
            self.__start_writer ()
            self.video_writer.write(cv2.resize(frame, self.resolution))
        else:
            # if we are not in recording mode, then stop recording
            self.stop_recording ()

    def activate_recording (self, duration=-1):
        if self.trace:
            print ('activate_recording')
        if duration <= 0:
            self.clip_duration = self.default_duration
        else:
            self.clip_duration = duration
        self.start_time = time.time()    #reset the clock counter to extend any active recording session
        self.__start_writer()

    def stop_recording (self):
        if self.trace:
            print ('stop_recording')
        self.video_writer = None
        self.start_time = 0
        self.clip_duration = self.default_duration


if __name__ == '__main__':
    dvr = DVR(path=".", duration=5, trace=True)
    dvr.activate_recording()
    img1 = cv2.imread ('dog.jpg')
    img2 = cv2.imread ('cat.jpg')

    dvr.record_frame_if_active (img1)
    dvr.record_frame_if_active (img2)
    dvr.record_frame_if_active (img1)
    dvr.record_frame_if_active (img2)
    time.sleep (10)
    dvr.record_frame_if_active (img1)
    dvr.record_frame_if_active (img2)
    dvr.record_frame_if_active (img1)
    dvr.activate_recording(2)
    dvr.record_frame_if_active (img2)
    dvr.record_frame_if_active (img1)
    dvr.stop_recording()
    dvr.record_frame_if_active (img2)
    dvr.activate_recording()
    dvr.record_frame_if_active (img1)
    dvr.record_frame_if_active (img2)
    time.sleep(7)
    dvr.record_frame_if_active (img1)
    dvr.record_frame_if_active (img2)
