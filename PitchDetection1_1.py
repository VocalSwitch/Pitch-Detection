import aubio #pitch detection
import numpy as np #math and matrix work
import pyaudio #audio input
import time

# PyAudio object.
p = pyaudio.PyAudio()

# Open stream.
stream = p.open(format=pyaudio.paFloat32,
    channels=1, rate=48000, input=True,
    frames_per_buffer=1024)

# Aubio's pitch detection.
pDetection = aubio.pitch("default", 2048,
    2048//2, 48000) #optimize for human range of fundemental frequencies
# Set units.
pDetection.set_unit("Hz")
pDetection.set_silence(-40)


def getpitch():
    data = stream.read(1024, exception_on_overflow = False)  # 1024 number of frames
    # Pull sample
    sample = np.fromstring(data,
                           dtype=aubio.float_type)

    pitch = pDetection(sample)[0]  # Pull current fundemental pitch from sample

    return pitch

def PitchAnalysis():
    # Initialize lists to hold values
    counters = []
    pitches = []

    # Inizalize counter as 0 and constants
    counter = 0
    testband_percent = .056
    sample_length = 10

    # Grab current pitch as test variable
    temp = getpitch()

    for i in range(1, 500):
        # Grab pitch
        pitch = getpitch()

        # test Pitch against the previous pitch, temp
        # if Pitch is within a range of Temp, consider it the same pitch and add 1 to the counter
        if ((pitch <= temp + (testband_percent * temp)) and (pitch >= temp - (testband_percent * temp))) and (
                pitch > 25):
            counter += 1
        else:
            counter = 0

        # if counter greater then the sample_length cause the switch to trip (program end)
        if (counter >= sample_length):
            return 1
            break

        # save all pitches and counters for debugging
        pitches.append(pitch)
        counters.append(counter)

        # save pitch as temp to test for next loop
        temp = pitch

        # print for debugging
        #print(counter, pitch)

    # Ending statement
    return 0

while True:
    buttonstatus = 0
    buttonstatus = PitchAnalysis()
    if buttonstatus == 1:
        print('button pushed')
        time.sleep(3)
