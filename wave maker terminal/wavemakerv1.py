# Wave generator

import math
from termsize import get_terminal_size

waveType_d = "sin"
amplitude_d = 1
displacement_verti_d = 0
displacement_horiz_d = 0
period_d = 1
max_i_d = 10

waveType = ""
amplitude = 0
displacement_verti = 0
displacement_horiz = 0
period = 0
max_i = 0


def question():
    global waveType
    global amplitude
    global displacement_verti
    global displacement_horiz
    global period
    global max_i
    waveType = str(raw_input("Options: cos sin\nWhat type of wave? "))
    if(waveType == "sin" or waveType == "cos"):
        pass
    elif(waveType == ""):
        waveType = waveType_d
        #print "Defaulting to %s" % waveType
    else:
        question()
        sys.exit()

    amplitude = raw_input("\nOptions: Any integer within half the width of the console\nAmplitude: ")
    if amplitude:
        try:
            amplitude = int(amplitude)
        except:
            print "Please enter an integer"
            question()
            sys.exit()
    else:
        amplitude = amplitude_d
        print "Using %s for amplitude" % str(amplitude)

    displacement_verti = raw_input("\nOptions: Any integer within half the width of the console\nVertical displacement: ")
    if displacement_verti:
        try:
            displacement_verti = int(displacement_verti)
        except:
            print "Please enter an integer"
            question()
            sys.exit()
    else:
        displacement_verti = displacement_verti_d
        print "Using %s for vertical displacement" % str(displacement_verti)

    displacement_horiz = raw_input("\nOptions: Any integer within half the height of the console\nHorizontal displacement: ")
    if displacement_horiz:
        try:
            displacement_horiz = int(displacement_horiz)
        except:
            print "Please enter an integer"
            question()
            sys.exit()
    else:
        displacement_horiz = displacement_horiz_d
        print "Using %s for horizontal displacement" % str(displacement_horiz)

    period = raw_input("\nOptions: Be reasoanble\nPeriod: ")
    if period:
        try:
            period = float(period)
        except:
            print "Enter a number please"
            question()
            sys.exit()
    else:
        period = period_d
        print "Using %s for horizontal displacement" % str(period)

    max_i = raw_input("\nOptions: A number above 0\nmax_i: ")
    if max_i:
        try:
            #print "gg"
            max_i = int(max_i)
        except:
            print "Please enter an integer"
            question()
            sys.exit()
    else:
        max_i = max_i_d
        print "Using %s for max_i" % str(max_i)

question()

for i in range(0, max_i*10):
    i = i/10.0
    if waveType == "sin":
        f = math.sin
    else:
        f = math.cos
    b = (2*math.pi)/period
    pos = amplitude * f(i*((2*math.pi)/period) - displacement_horiz) + displacement_verti
    width = get_terminal_size()[0]
    print " " * int(pos*10 + width/2), "*"
