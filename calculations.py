import math

def get_results(transconfig, polarity, loadconfig, v_line, turns_ratio, z, r02, x02):
    
    vr = i_line_pri = i_line_sec = None

    if transconfig == ['d', 'd'] and loadconfig == 'd':
        v_ph_sec = [(v_line[0]), ((v_line[1])+polarity*30)]
        # print(v_ph_sec)
        i_ph = [(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                      turns_ratio[0]), ((v_ph_sec[1])-(z[1]))]
        # print ('angle is: ',phi)
        phi = v_ph_sec[1]-i_ph[1]
        vr = float(i_ph[0])*(((float(r02)*float(math.cos(phi*(math.pi)/180)))) +
                             (float(x02)*float(math.sin(phi*(math.pi)/180))))/float(turns_ratio[1])
        i_line_sec = [(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                            turns_ratio[0]), ((v_ph_sec[1])-(z[1]))]
        i_line_pri = [1.732*((turns_ratio[1]/turns_ratio[0])**2)
                      * v_line[0]/z[0], (v_line[1]-z[1])]
        # print (phi)

    elif transconfig == ['d', 'd'] and loadconfig == 'y':
        v_ph_sec = [(v_line[0]), ((v_line[1])+polarity*30)]
        # print(v_ph_sec)
        i_ph = [0.577*(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                            turns_ratio[0]), ((v_ph_sec[1])-(z[1])-30)]
        phi = v_ph_sec[1]-i_ph[1]
        vr = float(i_ph[0])*(((float(r02)*float(math.cos(phi*(math.pi)/180)))) +
                             (float(x02)*float(math.sin(phi*(math.pi)/180))))/float(turns_ratio[1])
        i_line_sec = i_ph
        i_line_pri = [((turns_ratio[1]/turns_ratio[0])**2)
                      * v_line[0]/z[0], (v_line[1]-z[1]-60)]
        # print ('angle is: ',phi)

    elif transconfig == ['y', 'y'] and loadconfig == 'd':
        v_ph_sec = [(v_line[0]), ((v_line[1])+polarity*30)]
        # print(v_ph_sec)
        i_ph = [0.577*(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                            turns_ratio[0]), ((v_ph_sec[1])-(z[1])+30)]
        phi = v_ph_sec[1]-i_ph[1]
        vr = float(i_ph[0])*(((float(r02)*float(math.cos(phi*(math.pi)/180)))) +
                             (float(x02)*float(math.sin(phi*(math.pi)/180))))/float(turns_ratio[1])
        i_line_sec = i_ph
        i_line_pri = [((turns_ratio[1]/turns_ratio[0])**2)
                      * v_line[0]/z[0], (v_line[1]-z[1]+30)]
        # print ('angle is: ',phi)

    elif transconfig == ['y', 'y'] and loadconfig == 'y':
        v_ph_sec = [(v_line[0]), ((v_line[1])+polarity*30)]
        # print(v_ph_sec)
        i_ph = [0.577*(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                            turns_ratio[0]), ((v_ph_sec[1])-(z[1]))]
        phi = v_ph_sec[1]-i_ph[1]
        vr = float(i_ph[0])*(((float(r02)*float(math.cos(phi*(math.pi)/180)))) +
                             (float(x02)*float(math.sin(phi*(math.pi)/180))))/float(turns_ratio[1])
        # print ('angle is: ',phi)
        i_line_sec = i_ph
        i_line_pri = [0.577*((turns_ratio[1]/turns_ratio[0])**2)
                      * v_line[0]/z[0], (v_line[1]-z[1])]

    elif transconfig == ['d', 'y'] and loadconfig == 'd':
        v_ph_sec = [(v_line[0]), ((v_line[1])+polarity*30)]
        # print(v_ph_sec)
        i_ph = [1.732*(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                            turns_ratio[0]), (-(v_ph_sec[1])-(z[1]))]
        phi = v_ph_sec[1]-i_ph[1]
        vr = float(i_ph[0])*(((float(r02)*float(math.cos(phi*(math.pi)/180)))) +
                             (float(x02)*float(math.sin(phi*(math.pi)/180))))/float(turns_ratio[1])
        print(vr)
        # print ('angle is: ',phi)
        i_line_sec = [3*(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                              turns_ratio[0]), (-(v_ph_sec[1])-(z[1])-30)]
        print(i_line_sec)
        i_line_pri = [5.196*((turns_ratio[1]/turns_ratio[0])**2)
                      * v_line[0]/z[0], (v_line[1]-z[1]-60)]
        print(i_line_pri)

    elif transconfig == ['d', 'y'] and loadconfig == 'y':
        v_ph_sec = [(v_line[0]), ((v_line[1])+polarity*30)]
        # print(v_ph_sec)
        i_ph = [(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                      turns_ratio[0]), (-(v_ph_sec[1])-(z[1]))]
        phi = v_ph_sec[1]-i_ph[1]
        vr = float(i_ph[0])*(((float(r02)*float(math.cos(phi*(math.pi)/180)))) +
                             (float(x02)*float(math.sin(phi*(math.pi)/180))))/float(turns_ratio[1])        # print ('angle is: ',phi)
        i_line_sec = i_ph        
        i_line_pri = [1.732*((turns_ratio[1]/turns_ratio[0])**2)
                      * v_line[0]/z[0], (v_line[1]-z[1]-30)]
    elif transconfig == ['y', 'd'] and loadconfig == 'd':
        v_ph_sec = [(v_line[0]), ((v_line[1])+polarity*30)]
        # print(v_ph_sec)
        i_ph = [0.577*(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                            turns_ratio[0]), (-(v_ph_sec[1])-(z[1]))]
        phi = v_ph_sec[1]-i_ph[1]
        vr = float(i_ph[0])*(((float(r02)*float(math.cos(phi*(math.pi)/180)))) +
                             (float(x02)*float(math.sin(phi*(math.pi)/180))))/float(turns_ratio[1])        # print ('angle is: ',phi)
        i_line_sec = [(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                            turns_ratio[0]), (-(v_ph_sec[1])-(z[1])-30)]        
        i_line_pri = [((turns_ratio[1]/turns_ratio[0])**2)
                      * v_line[0]/z[0], (v_line[1]-z[1]-30)]
    elif transconfig == ['y', 'd'] and loadconfig == 'y':
        v_ph_sec = [(v_line[0]), ((v_line[1])+polarity*30)]
        # print(v_ph_sec)
        i_ph = [0.333*(v_ph_sec[0])/(z[0])*(turns_ratio[1] /
                                            turns_ratio[0]), (-(v_ph_sec[1])-(z[1])-30)]
        phi = v_ph_sec[1]-i_ph[1]
        vr = float(i_ph[0])*(((float(r02)*float(math.cos(phi*(math.pi)/180)))) +
                             (float(x02)*float(math.sin(phi*(math.pi)/180))))/float(turns_ratio[1])        # print ('angle is: ',phi)
        i_line_sec = i_ph        
        i_line_pri = [0.333*((turns_ratio[1]/turns_ratio[0])**2)
                      * v_line[0]/z[0], (v_line[1]-z[1]-30)]

    return vr, i_line_pri, i_line_sec