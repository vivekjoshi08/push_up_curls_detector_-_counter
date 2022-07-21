import numpy as np

def pushup(angle):
    return (int(np.interp(angle, (70,170), (100, 0))))

def dumble_curl(angle):
    return (int(np.interp(angle, (200, 330), (0, 100) )))

def filling_bar(percent_check):
    return (int(np.interp(percent_check, (0, 100), (60+590,60))))
