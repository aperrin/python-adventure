import serial
import time

ser = serial.Serial('COM1', 9600, timeout = 1)
print ser.portstr
i = 0
res = []
temp_moy = []
restime = []
res_moy = []
n_moy = 10

old_time = time.clock()
while len(temp_moy) < n_moy:
    data = ser.readline()
    if data :
        _time = time.clock()
        temp_moy.append(_time - old_time)

old_time = time.clock()
while i < 100:
    data=ser.readline()
    data = data.strip('0').strip()
    if data :
        _time = time.clock()
        if (_time - old_time) > 4e-2 :
            i +=1
            print i, _time - old_time, len(temp_moy)
            temp_moy = temp_moy[1:]
            temp_moy.append(_time - old_time)
            restime.append(time.clock())
            res.append(_time-old_time)
            print temp_moy
            res_moy.append(sum(temp_moy)/len(temp_moy))
        old_time = _time
        
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    print len(res)
    #plt.plot(restime, res)
    plt.plot(res)
    plt.plot(res_moy)
    plt.show()