
import numpy as np

# angle input in radians
def coordError( h, angle):
    
    x_w = h*np.tan(angle + 0.1658) # 9.5 degrees = 0.1658 rads  
    x_l = h*np.tan(angle - 0.1658)
    x_c = h*np.tan(angle)
    #print("Xw: " + str(x_w) + " Xl: " + str(x_l) + " Xc: " + str(x_c))
    
    y_w = h*np.sqrt( 1 + np.power( np.tan(angle + 0.1658), 2) )*np.tan(0.21816) # 12.5 degrees = 0.21816 rads
    y_l = h*np.sqrt( 1 + np.power( np.tan(angle - 0.1658), 2) )*np.tan(0.21816)
    y_c = h*np.sqrt( 1 + np.power( np.tan(angle), 2) )*np.tan(0.21816)
    #print("Yw: " + str(y_w) + " Yl: " + str(y_l) + " Yc: " + str(y_c))
    
    return [x_w, y_w]
    
