#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 11:17:59 2018

@author: meghanfickett
"""

#This is Version 1.0 of the full Instrumentation Calibration test code for the WQM system.
#This will be a user-prompted and user-controlled script that will perform only the functions that the user wishes to complete.

#Import libraries:
import serial
import time
import numpy
import re
from matplotlib import pyplot

#First, the user must choose the process that they wish to complete:

WQM_SN=str(input('What is the WQM serial Number? (###)'))
t_0=time.time()
#Define the date and time for logging purposes:
tlocal=time.localtime(t_0)
Date=time.strftime('%m/%d/%Y', tlocal)
Date_no_slash=time.strftime('%m%d%Y', tlocal)
ESTTime=time.strftime('%H:%M:%S', tlocal)
Name=str("WQM"+WQM_SN+Date_no_slash+'.txt')
    
print("The following are the processes that are completed by this code.\n")
print("Process 1: Temperature, Conductivity, and Salinity for WQM and SeaBird - Main Tank \n")
print("Process 2: Old Dissolved Oxygen values - Main Tank \n")
print("Process 3: New Dissolved Oxygen values, with new Scale Factor - Main Tank \n")
print("Process 4: FLNTUS and Old WQM Chlorophyll and Turbidity values - Small Tanks \n")
print("Process 5: New WQM Chlorophyll and Turbidity values, with new Scale Factor - Small Tanks \n")

Process=int(input("Please select the process you wish to complete (1-5): \n"))

if Process == 1:
    print('You have selected Process 1 -Temperature, Conductivity, and Salinity for WQM and SeaBird - Main Tank ')
    print('\n Check that the instruments are properly plugged in before starting! \n')
    COM_WQM=(input('What is the COM port for the WQM? (COM#)'))
    COM_SB=(input('What is the COM port for the SeaBird? (COM#)'))
    #Have user initialize code:
    input('Press enter to collect the data: ')
    
    #Define function for the WQM serial:
    WQMser=serial.Serial(
        port=(COM_WQM),
        baudrate=19200,
        timeout=0
    )

    #Define function for the SeaBird serial:
    SBser=serial.Serial(
            port=(COM_SB),
            baudrate=9600,
            timeout=0
    )
    
    #Creating lists for things to be stored in - Time for each one is defined as a numpy array bc all values will be known floats.
    WQM=list()
    SB=list()
    WQMTime=numpy.array([])
    SBTime=numpy.array([])
    
    #define time as counter variable
    t=tOpt=t0=int(time.time())
    print('Data is being collected: ')
    #While loop for data collection and storage only. All processing, including decoding and parsing, will be done after the ports have been closed.
    while t<=t0+120:
        
        if WQMser.inWaiting()>0:
            WQM.append(WQMser.read())
            WQMTime=numpy.append(WQMTime, int(t))
        if SBser.inWaiting()>0:
            SB.append(SBser.read())
            SBTime=numpy.append(SBTime, int(t))
        t=time.time()

    WQMser.close()
    SBser.close()
    
    #Print statements to check that data collection was completed properly.
    print("WQM:",WQM)
    print("SB:",SB)
    print("WQM Time:", WQMTime)
    print("SB Time:", SBTime)
    
    #decoding and joining the long lists into one string:
    WQM_data=(b''.join(WQM)).decode('utf-8')
    print(WQM_data)
    SB_data=(b''.join(SB)).decode('utf-8')
    print(SB_data)
    
    #WQM data processing:
    WQM_data=re.findall(r'\d+[.]\d*|\d+', WQM_data)
    print(WQM_data)
    
   
    print(len(WQM_data))
    WQMRemain=int(len(WQM_data)%14)
    if WQMRemain !=0:
        del WQM_data[0:int(WQMRemain)]
        print(len(WQM_data))
    WQMCol=14
    WQMRow=int((len(WQM_data)/14))
    print(WQM_data)
    print(WQMCol)
    print(WQMRow)  
    WQM_data=numpy.asarray(WQM_data, dtype=numpy.float32)
    #reshape the array so it's not 1D:
    WQM_data=numpy.reshape(WQM_data, (WQMRow,WQMCol))
    #Now, transpose:
    WQM_data=numpy.transpose(WQM_data)
    print(WQM_data)
    #Doing the math:
    WQM_mean_T=numpy.mean(WQM_data[4])
    WQM_mean_C=numpy.mean(WQM_data[3])
    WQM_mean_S=numpy.mean(WQM_data[6])
    print(WQM_mean_T)
    print(WQM_mean_C)
    print(WQM_mean_S)
    
    #Make them into lists, to make them into arrays for plotting
    WQM_mean_T=[WQM_mean_T]*len(WQMTime)
    WQM_mean_C=[WQM_mean_C]*len(WQMTime)
    WQM_mean_S=[WQM_mean_S]*len(WQMTime)
    
    #Now, make them into arrays
    WQM_mean_T=numpy.asarray(WQM_mean_T, dtype=numpy.float32)
    WQM_mean_C=numpy.asarray(WQM_mean_C, dtype=numpy.float32)
    WQM_mean_S=numpy.asarray(WQM_mean_S, dtype=numpy.float32)
    
    #SeaBird data processing:
    SB_data=re.findall(r'\d+[.]\d+', SB_data)
    print(SB_data)
    print(len(SB_data))
    SBRemain=int(len(SB_data)%3)
    if SBRemain !=0:
        del SB_data[0:int(SBRemain)]
        print(len(SB_data))
    SB_data=numpy.asarray(SB_data, dtype=numpy.float32)
    SBCol=3
    SBRow=int(len(SB_data)/3)
    SB_data=numpy.reshape(SB_data, (SBRow,SBCol))
    print(SB_data)
    
    #Doing the math:
    SB_data=numpy.transpose(SB_data)
    print(SB_data)
    SB_mean_T=numpy.mean(SB_data[0])
    SB_mean_C=numpy.mean(SB_data[1])
    SB_mean_S=numpy.mean(SB_data[2])
    print(SB_mean_T)
    print(SB_mean_C)
    print(SB_mean_S)
    
    #Make them into lists:
    SB_mean_T=[SB_mean_T]*len(SBTime)
    SB_mean_C=[SB_mean_C]*len(SBTime)
    SB_mean_S=[SB_mean_S]*len(SBTime)
    
    #Now, into arrays:
    SB_mean_T=numpy.asarray(SB_mean_T, dtype=numpy.float32)
    SB_mean_C=numpy.asarray(SB_mean_C, dtype=numpy.float32)
    SB_mean_S=numpy.asarray(SB_mean_S, dtype=numpy.float32)
    
    #Print all of the values out:
    print("Date of collection:",Date )
    print("WQM Serial #:", WQM_SN)
    print("WQM Temperature:", WQM_mean_T[0])
    print("SeaBird Temperature:", SB_mean_T[0])
    print("WQM Conductivity:", WQM_mean_C[0])
    print("SeaBird Conductivity:", SB_mean_C[0])
    print("WQM Salinity:", WQM_mean_S[0])
    print("SeaBird Salinity:", SB_mean_S[0])
    
    #WQM vs. SeaBird:
    #making the axis:
    fig1=pyplot.figure(figsize=[9,12])
    
    #set the plot axis grids:
    #distance between graphs set to 1, graph height set to 3
    ax1=pyplot.subplot2grid((12,1), (0,0), rowspan=3)
    pyplot.setp(ax1.get_xticklabels())
    ax2=pyplot.subplot2grid((12,1), (4,0), rowspan=3)
    pyplot.setp(ax2.get_xticklabels())
    ax3=pyplot.subplot2grid((12,1), (8,0), rowspan=3)
    pyplot.setp(ax3.get_xticklabels())
    #leave out statement regarding x-ticks on last one so they show up
    
    #New time arrays to get the real-time WQM data and plot it versus a time array of the same length:
    WQM_time=numpy.linspace(WQMTime[0], WQMTime[-1], num=int(len(WQM_data[0])))
    
    SB_time=numpy.linspace(SBTime[0], SBTime[-1], num=int(len(SB_data[0])))
    
    #Plotting data:
    #Temperature:
    ax1.plot(WQM_time, WQM_data[4], color='blue', label = 'WQM')
    ax1.plot(WQMTime, WQM_mean_T, color='red', label='WQM Mean={0:4.2f}'.format(WQM_mean_T[0]))
    ax1.plot(SB_time, SB_data[0], color='green', label = 'SeaBird')
    ax1.plot(SBTime, SB_mean_T, color='orange', label='SB Mean={0:4.2f}'.format(SB_mean_T[0]))
    #Conductivity:
    ax2.plot(WQM_time, WQM_data[3], color = 'blue', label = 'WQM')
    ax2.plot(WQMTime, WQM_mean_C, color = 'red', label = 'WQM Mean={0:6.2f}'.format(WQM_mean_C[0]))
    ax2.plot(SB_time, SB_data[1], color = 'green', label = 'SeaBird')
    ax2.plot(SBTime, SB_mean_C, color = 'orange', label = 'SB Mean={0:6.2f}'.format(SB_mean_C[0]))
    #Salinity:
    ax3.plot(WQM_time, WQM_data[6], color = 'blue', label = 'WQM')
    ax3.plot(WQMTime, WQM_mean_S, color = 'red', label = 'WQM Mean={0:4.2f}'.format(WQM_mean_S[0]))
    ax3.plot(SB_time, SB_data[2], color = 'green', label = 'SeaBird')
    ax3.plot(SBTime, SB_mean_S, color = 'orange', label = 'SB Mean={0:6.2f}'.format(SB_mean_S[0]))
    
    #Setting titles and axis labels:
    ax1.set_title('Temperature') 
    ax1.set_ylabel('$^\circ$ C')
    
    ax1.legend(loc='best')
    
    ax2.set_title('Conductivity')
    ax2.set_ylabel('S/m')
    
    ax2.legend(loc='best')
    
    ax3.set_title('Salinity')
    ax3.set_ylabel('PSU')
    ax3.set_xlabel('Time - s')
    ax3.legend(loc='best')
    
    #Show plot:
    pyplot.show()
    
    
    #Writing out to a text file:
    
    text=open(Name, 'w+')
    text.write('Date of collection: ')
    text.write(Date)
    text.write('\n')
    text.write('WQM Serial #: ')
    text.write(WQM_SN)
    text.write('\n')
    text.write('WQM Mean Temperature: ')
    text.write(str(WQM_mean_T[0]))
    text.write(' degrees Celsius')
    text.write('\n')
    text.write('SeaBird Mean Temperature: ')
    text.write(str(SB_mean_T[0]))
    text.write(' degrees Celsius')
    text.write('\n')
    text.write('WQM Mean Conductivity: ')
    text.write(str(WQM_mean_C[0]))
    text.write(' S/m')
    text.write('\n')
    text.write('SeaBird Mean Conductivity: ')
    text.write(str(SB_mean_C[0]))
    text.write(' S/m')
    text.write('\n')
    text.write('WQM Mean Salinity: ')
    text.write(str(WQM_mean_S[0]))
    text.write(' PSU')   
    text.write('\n')
    text.write('SeaBird Mean Salinity: ')
    text.write(str(SB_mean_S[0]))
    text.write(' PSU') 
    text.write('\n')
    text.close()
    
    #We need to have an if statement in all subsequent statements that asks the user if they have created the text file yet, asks for the name of the text file, and then either writes or appends so it doesn't write over text that has already been created.
    
    
    
if Process ==2: #Old DO values
    print('You have selected Process 2 - Old Dissolved Oxygen values - Main Tank')
    print('\n Check that the instruments are properly plugged in before starting! \n')
    COM_WQM=(input('What is the COM port for the WQM? (COM#)'))
    COM_Opt=(input('What is the COM port for the Optode? (COM#)'))
    
    SBE_SOC_Old=str(input('Please Enter the WQM Settings menu. Enter the SBE52.SOC value: '))
    
    #Have user initialize code:
    input('Press enter to collect the data: ')
    #Define function for the WQM serial:
    WQMser=serial.Serial(
        port=(COM_WQM),
        baudrate=19200,
        timeout=0
    )
    
    #Define function for the Optode:
    Optser=serial.Serial(
            port=(COM_Opt),
            baudrate=9600,
            timeout=0
    )
    
    #Creating lists for things to be stored in - Time for each one is defined as a numpy array bc all values will be known floats.
    WQM=list()
    Opt=list()
    WQMTime=numpy.array([])
    OptTime=numpy.array([])
    
    #define time as counter variable
    t=tOpt=t0=int(time.time())
    print('Data is being collected: ')
    while t<=t0+120:
        if WQMser.inWaiting()>0:
            WQM.append(WQMser.read())
            WQMTime=numpy.append(WQMTime, int(t))
        if Optser.inWaiting()>0:
            Opt.append(Optser.read())
            OptTime=numpy.append(OptTime, int(t))
        t=time.time()
    WQMser.close()
    Optser.close()
    
    #Print statements to check that data collection was completed properly.
    print("WQM:",WQM)
    print("Opt:",Opt)
    print("WQM Time:", WQMTime)
    print("Opt Time:", OptTime)
    #decoding and joining the long lists into one string:
    WQM_data=(b''.join(WQM)).decode('utf-8')
    print(WQM_data)
    Opt_data=(b''.join(Opt)).decode('utf-8', 'ignore')
    print(Opt_data)

    
    #WQM data processing:
    WQM_data=re.findall(r'\d+[.]\d*|\d+', WQM_data)
    print(WQM_data)

    
    print(len(WQM_data))
    WQMRemain=int(len(WQM_data)%14)
    if WQMRemain !=0:
        del WQM_data[0:int(WQMRemain)]
        print(len(WQM_data))
    WQMCol=14
    WQMRow=int((len(WQM_data)/14))
    print(WQM_data)
    print(WQMCol)
    print(WQMRow)
    WQM_data=numpy.asarray(WQM_data, dtype=numpy.float32)
    #reshape the array so it's not 1D:
    WQM_data=numpy.reshape(WQM_data, (WQMRow,WQMCol))
    #Now, transpose:
    WQM_data=numpy.transpose(WQM_data)
    print(WQM_data)
    
    #Calculating oxygen values
    WQM_old_DO=numpy.mean(WQM_data[9])
    WQM_old_OxSat=numpy.mean(WQM_data[8])
    
    print(WQM_old_DO)
    print(WQM_old_OxSat)
    
    #Make them into lists to make into arrays for possible plotting if we wish to include it
    WQM_old_DO=[WQM_old_DO]*len(WQMTime)
    WQM_old_OxSat=[WQM_old_OxSat]*len(WQMTime)
    WQM_old_DO=numpy.asarray(WQM_old_DO, dtype=numpy.float32)
    WQM_old_OxSat=numpy.asarray(WQM_old_OxSat, dtype=numpy.float32)
    
    #Optode data processing:
    Opt_data=re.findall(r'\d+[.]\d*|\d+', Opt_data)
    Opt_data=numpy.asarray(Opt_data, dtype=numpy.float32)
    print(Opt_data)
    OptRow=int(len(Opt_data)/12)
    OptCol=12
    Opt_data=numpy.reshape(Opt_data, (OptRow, OptCol))
    Opt_data=numpy.transpose(Opt_data)
    Opt_SatOpt=numpy.mean(Opt_data[3])
    print(Opt_SatOpt)
    
    #Opt_SatOpt=[Opt_SatOpt]*len(WQMTime)
    #Opt_SatOpt=numpy.asarray(Opt_SatOpt, dtype=numpy.float32)
    #Now, after we have the values for each of the tests that we need, we display them, and do the extra math on them...
    #Optode math:
    Old_DO_percent=(WQM_old_DO/WQM_old_OxSat)*100
    Old_SOC=(((Opt_SatOpt)/100)*WQM_old_OxSat)/WQM_old_DO
    
    print("Old DO:", WQM_old_DO[0])
    print("Old Oxsat:", WQM_old_OxSat[0])
    print("Old SAT Opt %:", Opt_SatOpt)
    print("Old DO%:", Old_DO_percent[0])
    print("Old SOC:", Old_SOC[0])
    '''
    #Plotting data:
    
    pyplot.plot(WQMTime, WQM_old_OxSat, label = 'WQM')
    pyplot.plot(WQMTime, Opt_SatOpt, label = 'Optode' )
    pyplot.title('Oxygen Saturation Levels - Old')
    pyplot.ylabel('Saturation (%)')
    pyplot.xlabel('Time - s')
    pyplot.legend(loc='best')
    pyplot.show()
    '''
    #Include a text file write-up
    #We need an if statement so we know if this text file has been created yet or if it hasn't
    text_choice_2=input('Has a text file been made for this WQM test for this date? (y/n)')
    if text_choice_2 == 'y':
        #If there has already been a text file created, we can go ahead and just open it and append to it.
        text=open(Name, 'a')
        text.write('Old WQM Dissolved Oxygen level: ')
        text.write(str(WQM_old_DO[0]))
        text.write(' mg/L')
        text.write('\n')
        text.write('Old WQM OxSat: ')
        text.write(str(WQM_old_OxSat[0]))
        text.write(' mg/L')
        text.write('\n')
        text.write('Old Optode Sat Opt: ')
        text.write(str(Opt_SatOpt))
        text.write(' %')
        text.write('\n')
        text.write('Old WQM DO %: ')
        text.write(str(Old_DO_percent[0]))
        text.write(' %')
        text.write('\n')
        text.write('Old SOC: ')
        text.write(str(Old_SOC[0]))
        text.write('\n')
        text.write('Old SBE52.SOC: ')
        text.write(SBE_SOC_Old)
        text.write('\n')
        text.close()
    if text_choice_2 == 'n':
        text=open(Name, 'w+')
        text.write('Date of collection: ')
        text.write(Date)
        text.write('\n')
        text.write('WQM Serial #: ')
        text.write(WQM_SN)
        text.write('\n')
        text.write('Old WQM Dissolved Oxygen level: ')
        text.write(str(WQM_old_DO[0]))
        text.write(' mg/L')
        text.write('\n')
        text.write('Old WQM OxSat: ')
        text.write(str(WQM_old_OxSat[0]))
        text.write(' mg/L')
        text.write('\n')
        text.write('Old Optode Sat Opt: ')
        text.write(str(Opt_SatOpt))
        text.write(' %')
        text.write('\n')
        text.write('Old WQM DO %: ')
        text.write(str(Old_DO_percent[0]))
        text.write(' %')
        text.write('\n')
        text.write('Old SOC factor: ')
        text.write(str(Old_SOC[0]))
        text.write('\n')
        text.write('Old SBE52.SOC: ')
        text.write(SBE_SOC_Old)
        text.write('\n')
        text.close()
        
        
    #End of process 2.

    
if Process ==3:
    print('You have selected Process 3 - New Dissolved Oxygen values, with new Scale Factor - Main Tank')
    #New Dissolved Oxygen
    
    print('Please enter the settings menu for the WQM device and change the SBE52.SOC value to what you would like it to be.' )
    SBE_SOC_New=str(input('What is the new SBE52.SOC value? '))
    print('\n Check that the instruments are properly plugged in before starting! \n')
    COM_WQM=(input('What is the COM port for the WQM? (COM#)'))
    COM_Opt=(input('What is the COM port for the Optode? (COM#)'))
    
    
    #Have user initialize code:
    input('Press enter to collect the data: ')
    #Define function for the WQM serial:
    WQMser=serial.Serial(
        port=(COM_WQM),
        baudrate=19200,
        timeout=0
    )
    
    #Define function for the Optode:
    Optser=serial.Serial(
            port=(COM_Opt),
            baudrate=9600,
            timeout=0
    )
    
    #Creating lists for things to be stored in - Time for each one is defined as a numpy array bc all values will be known floats.
    WQM=list()
    Opt=list()
    WQMTime=numpy.array([])
    OptTime=numpy.array([])
    
    #define time as counter variable
    t=tOpt=t0=int(time.time())
    print('Data is being collected:')
    while t<=t0+120:
        if WQMser.inWaiting()>0:
            WQM.append(WQMser.read())
            WQMTime=numpy.append(WQMTime, int(t))
        if Optser.inWaiting()>0:
            Opt.append(Optser.read())
            OptTime=numpy.append(OptTime, int(t))
        t=time.time()
    WQMser.close()
    Optser.close()
    
    #Print statements to check that data collection was completed properly.
    print("WQM:",WQM)
    print("Opt:",Opt)
    print("WQM Time:", WQMTime)
    print("Opt Time:", OptTime)
    #decoding and joining the long lists into one string:
    WQM_data=(b''.join(WQM)).decode('utf-8')
    print(WQM_data)
    Opt_data=(b''.join(Opt)).decode('utf-8', 'ignore')
    print(Opt_data)

    
    #WQM data processing:
    WQM_data=re.findall(r'\d+[.]\d*|\d+', WQM_data)
    print(WQM_data)

    
    print(len(WQM_data))
    WQMRemain=int(len(WQM_data)%14)
    if WQMRemain !=0:
        del WQM_data[0:int(WQMRemain)]
        print(len(WQM_data))
    WQMCol=14
    WQMRow=int((len(WQM_data)/14))
    print(WQM_data)
    print(WQMCol)
    print(WQMRow)
    WQM_data=numpy.asarray(WQM_data, dtype=numpy.float32)
    #reshape the array so it's not 1D:
    WQM_data=numpy.reshape(WQM_data, (WQMRow,WQMCol))
    #Now, transpose:
    WQM_data=numpy.transpose(WQM_data)
    print(WQM_data)
    
    #Calculating oxygen values
    WQM_new_DO=numpy.mean(WQM_data[9])
    WQM_new_OxSat=numpy.mean(WQM_data[8])
    
    print(WQM_new_DO)
    print(WQM_new_OxSat)
    
    #Make them into lists to make into arrays for possible plotting if we wish to include it
    WQM_new_DO=[WQM_new_DO]*len(WQMTime)
    WQM_new_OxSat=[WQM_new_OxSat]*len(WQMTime)
    WQM_new_DO=numpy.asarray(WQM_new_DO, dtype=numpy.float32)
    WQM_new_OxSat=numpy.asarray(WQM_new_OxSat, dtype=numpy.float32)
    
    #Optode data processing:
    Opt_data=re.findall(r'\d+[.]\d*|\d+', Opt_data)
    Opt_data=numpy.asarray(Opt_data, dtype=numpy.float32)
    print(Opt_data)
    OptRow=int(len(Opt_data)/12)
    OptCol=12
    Opt_data=numpy.reshape(Opt_data, (OptRow, OptCol))
    Opt_data=numpy.transpose(Opt_data)
    New_Opt_SatOpt=numpy.mean(Opt_data[3])
    print(New_Opt_SatOpt)
    
    #Now, after we have the values for each of the tests that we need, we display them, and do the extra math on them...
    #Optode math:
    New_DO_percent=(WQM_new_DO/WQM_new_OxSat)*100
    
    
    print("New DO:", WQM_new_DO[0])
    print("New Oxsat:", WQM_new_OxSat[0])
    print("New SAT Opt %:", New_Opt_SatOpt)
    print("New DO%:", New_DO_percent[0])
    
    '''
    #Plotting data:
    Opt_time=numpy.linspace(OptTime[0], OptTime[-1], num=int(len(Opt_data[0])))
    pyplot.plot(Opt_time, WQM_new_OxSat, label = 'WQM')
    pyplot.plot(Opt_time, New_Opt_SatOpt, label = 'Optode' )
    pyplot.title('Oxygen Saturation Levels - New')
    pyplot.ylabel('Saturation (%)')
    pyplot.xlabel('Time - s')
    pyplot.legend(loc='best')
    pyplot.show()
    '''
    #Include a text file write-up
    #We need an if statement so we know if this text file has been created yet or if it hasn't
    text_choice_3=input('Has a text file been made for this WQM test for this date? (y/n)')
    if text_choice_3 == 'y':
        #If there has already been a text file created, we can go ahead and just open it and append to it.
        text=open(Name, 'a')
        text.write('New WQM Dissolved Oxygen level: ')
        text.write(str(WQM_new_DO[0]))
        text.write(' mg/L')
        text.write('\n')
        text.write('New WQM OxSat: ')
        text.write(str(WQM_new_OxSat[0]))
        text.write(' mg/L')
        text.write('\n')
        text.write('New Optode Sat Opt: ')
        text.write(str(New_Opt_SatOpt))
        text.write(' %')
        text.write('\n')
        text.write('New WQM DO %: ')
        text.write(str(New_DO_percent[0]))
        text.write(' %')
        text.write('\n')
        text.write('New SBE52.SOC: ')
        text.write(SBE_SOC_New)
        text.write('\n')
        text.close()
    if text_choice_3 == 'n':
        text=open(Name, 'w+')
        text.write('Date of collection: ')
        text.write(Date)
        text.write('\n')
        text.write('WQM Serial #: ')
        text.write(WQM_SN)
        text.write('\n')
        text.write('New WQM Dissolved Oxygen level: ')
        text.write(str(WQM_new_DO[0]))
        text.write(' mg/L')
        text.write('\n')
        text.write('New WQM OxSat: ')
        text.write(str(WQM_new_OxSat[0]))
        text.write(' mg/L')
        text.write('\n')
        text.write('New Optode Sat Opt: ')
        text.write(str(New_Opt_SatOpt))
        text.write(' %')
        text.write('\n')
        text.write('New WQM DO %: ')
        text.write(str(New_DO_percent[0]))
        text.write(' %')
        text.write('\n')
        text.write('New SBE52.SOC: ')
        text.write(SBE_SOC_New)
        text.write('\n')
        text.close()
        
        
    #End of process 3.

    
if Process ==4: 
    print('You have selected Process 4 - FLNTUS and Old WQM Chlorophyll and Turbidity values - Small Tanks ')
    #Old FLNTUS and WQM data collection and processing
    input('Press ENTER to define the FLNTUS serial port')

    #Now, we define and open the FLNTUS serial port to collect Chlorophyll data:
    FLNTser=serial.Serial(
        port=('COM5'),
        baudrate=19200,
        timeout=0
    )
    FLNTser.close()

    #Define FLNTUS Chloro list:
    FChlor=list()
    FChlorTime=numpy.array([])

    input('Press Enter to collect FLNTUS Chlorophyll data: 1 min after stirring')
    
    #define time as a counter variable:
    t=t0=int(time.time())
    
    print('Data is being collected: ')
    
    FLNTser.open()
    #Collection loop for FLNTUS Chloro:
    while t<=t0+120:
        if FLNTser.inWaiting()>0:
            FChlor.append(FLNTser.read())
            FChlorTime=numpy.append(FChlorTime, int(t))
        t=time.time()

    FLNTser.close()

    print(FChlor)
    
    #Turbidity data collection:
    print("\n Place the FLNTUS into the Turbidity tank after stirring \n")
    input('Press Enter to collect FLNTUS Turbidity data: 1 min after stirring')

    #open the FLNTUS serial port:
    FLNTser.open()
    #define the FLNTUS Turbidity list:
    FTurb=list()
    FTurbTime=numpy.array([])
    #define time as a counter variable:
    t=t2=int(time.time())

    print('Data is being collected: ')
    
    #Collection loop for FLNTUS Turb:

    while t<=t2+120:
        if FLNTser.inWaiting()>0:
            FTurb.append(FLNTser.read())
            FTurbTime=numpy.append(FTurbTime, int(t))
        t=time.time()
    FLNTser.close()
    print(FTurb)
    
    #Now, we have data collected for the FLNTUS device. Now, we need to parse things and determine the length of the arrays.
    #decode lists
    FChlor_data=(b''.join(FChlor)).decode('utf-8', errors ='ignore')
    print(FChlor_data)
    FTurb_data=(b''.join(FTurb)).decode('utf-8', errors='ignore')
    print(FTurb_data)
    #extract digits
    FChlor_data=re.findall(r'\d+[.]\d*|\d+', FChlor_data)
    print(FChlor_data)
    FTurb_data=re.findall(r'\d+[.]\d*|\d+', FTurb_data)
    print(FTurb_data)
    
    #With the date and time included there are 11 columns
    print(len(FChlor_data))
    print(len(FTurb_data))
    FChlorRemain=int(len(FChlor_data)%11)
    if FChlorRemain !=0:
        del FChlor_data[0:int(FChlorRemain)]
        print(FChlor_data)
        print(len(FChlor_data))
    FTurbRemain=int(len(FTurb_data)%11)
    if FTurbRemain !=0:
        del FTurb_data[0:int(FTurbRemain)]
        print(FTurb_data)
        print(len(FTurb_data))
        
    #Make them numpy arrays:
    FChlor_data=numpy.asarray(FChlor_data, dtype=numpy.float32)
    FTurb_data=numpy.asarray(FTurb_data, dtype=numpy.float32)

    FCol=11
    FChlorRow=int((len(FChlor_data)/11))
    print(FCol)
    print(FChlorRow)
    FTurbRow=int((len(FTurb_data)/11))
    print(FTurbRow)
    FChlor_data=numpy.reshape(FChlor_data, (FChlorRow,FCol))
    FTurb_data=numpy.reshape(FTurb_data, (FTurbRow,FCol))

    FChlor_data=numpy.transpose(FChlor_data)
    FTurb_data=numpy.transpose(FTurb_data)

    F_Chlor_counts=numpy.mean(FChlor_data[7])
    F_Turb_counts=numpy.mean(FTurb_data[9])

    print(F_Chlor_counts)
    print(F_Turb_counts)
    
    #Now, we can calculate the values for things:
    ChlorSF=float(input('What is the scaling factor for the Chlorophyll test?'))
    TurbSF=float(input('What is the scaling factor for the Turbidity test?'))
    FChlor_dark=float(input('What is the value of FLNTUS Chlorophyll dark counts?'))
    FTurb_dark=float(input('What is the value of FLNTUS Turbidity dark counts?'))
    
    FChlA=(F_Chlor_counts-FChlor_dark)*ChlorSF   
    FTurbNTU=(F_Turb_counts-FTurb_dark)*TurbSF
    
    #WQM Section:
    print('Do not turn on the WQM device until you are ready to take data. Wait to turn on the device until prompted to do so.\n')
    
    time.sleep(5)

    input('Once you are ready to take data, turn on the device. Press ENTER to define the WQM serial port and change to optics mode.Do this immediately after stirring, it will take 1 min for this process to be completed.\n')

    #Define the WQM serial port:
    time.sleep(30)
    print('Defining the serial port')
    time.sleep(5)
    WQMser=serial.Serial(
        port=('COM4'),
        baudrate=19200,
        timeout=0
    )
    print('Entering Standby Mode')
    WQMser.write("!!!!!".encode('utf-8'))
    time.sleep(10)
    print('Entering Optics Mode')
    WQMser.write("$ECO\r\n".encode('utf-8'))
    time.sleep(5)
    WQMser.write("$PKT 0\r\n$run\r\n".encode('utf-8'))

    time.sleep(5)

    WQMser.close()
    time.sleep(5)
    print('WQM serial port is now available for data collection\n')
    input("Press Enter to collect WQM Chlorophyll data: Immediately")
    WQMser.open()
    #Define WQM Chloro list:
    WQMChlor=list()
    WQMChlorTime=numpy.array([])
    #define time as a counter variable:
    t=t1=int(time.time())

    print('Data is being collected: ')
    
    #Collection loop for WQM Chloro:
    while t<=t1+120:
        if WQMser.inWaiting()>0:
            WQMChlor.append(WQMser.read())
            WQMChlorTime=numpy.append(WQMChlorTime, int(t))
        t=time.time()
    
    WQMser.write("**********".encode('utf-8'))
    time.sleep(15)
    WQMser.write("$MVS 0\r\n".encode('utf-8')) #Closes the biowiper
    time.sleep(10)
    WQMser.close()
    print(WQMChlor)
    
    input('Press Enter to collect WQM Turbidity data: 40 seconds after stirring')
    WQMser.open()
    time.sleep(10)
    print('Entering Optics Mode')
    WQMser.write("$ECO\r\n".encode('utf-8'))
    time.sleep(5)
    WQMser.write("$PKT 0\r\n$run\r\n".encode('utf-8'))
    time.sleep(5)
    #define the WQM Turbidity list:
    WQMTurb=list()
    WQMTurbTime=numpy.array([])
    #define time as a counter variable:
    t=t3=int(time.time())

    print('Data is being collected: ') #20 sec after pressing enter
    
    #Collection loop for WQM Turb:

    while t<=t3+120:
        if WQMser.inWaiting()>0:
            WQMTurb.append(WQMser.read())
            WQMTurbTime=numpy.append(WQMTurbTime, int(t))
        t=time.time()
    time.sleep(10)
    WQMser.write("**********".encode('utf-8')) #Standby mode in Optics
    time.sleep(15)
    WQMser.write("$MVS 0\r\n".encode('utf-8')) #Closes the biowiper
    time.sleep(10)
    WQMser.close()
    print(WQMTurb)
    
    print('\n\n\n Check that the biowiper has closed on the WQM. If it has not closed, enter TeraTerm upon completion of this run and close the biowiper before turning off the device.')
    
    #Decoding all of the lists:
    WQMChlor_data=(b''.join(WQMChlor)).decode('utf-8', errors='ignore')
    print(WQMChlor_data)
    WQMTurb_data=(b''.join(WQMTurb)).decode('utf-8', errors ='ignore')
    print(WQMTurb_data)
    
    #Parse the WQM data:
    WQMChlor_data=WQMChlor_data.split()
    WQMTurb_data=WQMTurb_data.split()
    del WQMChlor_data[0:30]
    del WQMTurb_data[0:30]
    WQMChlor_num=list()
    WQMTurb_num=list()
    for x in WQMChlor_data:
        if x.isdigit()==True:
            WQMChlor_num.append(x)
    for x in WQMTurb_data:
        if x.isdigit()==True:
            WQMTurb_num.append(x)
    WQMChlor_data=WQMChlor_num
    WQMTurb_data=WQMTurb_num
    
    #Now, they should each be lists of digits. Make them into numpy arrays now:
    WQMChlor_data=numpy.asarray(WQMChlor_data, dtype=numpy.float32)
    WQMTurb_data=numpy.asarray(WQMTurb_data, dtype=numpy.float32)
    
    #They are 1D arrays, they need to be reshaped so we can extract the digits.
    WQMCol=5
    WQMChlorRow=int((len(WQMChlor_data)/5))
    print(WQMCol)
    print(WQMChlorRow)
    WQMTurbRow=int((len(WQMTurb_data)/5))
    print(WQMTurbRow)
    WQMChlor_data=numpy.reshape(WQMChlor_data, (WQMChlorRow,WQMCol))
    WQMTurb_data=numpy.reshape(WQMTurb_data, (WQMTurbRow,WQMCol))
    
    #Need to transpose them in order to do the math:
    WQMChlor_data=numpy.transpose(WQMChlor_data)
    WQMTurb_data=numpy.transpose(WQMTurb_data)
    
    #Need to extract the mean number of counts of Chlorophyll and Turbidity for each of them
    #For the WQM:
    WQM_Chlor_counts=numpy.mean(WQMChlor_data[1])
    WQM_Turb_counts=numpy.mean(WQMTurb_data[3])
    WQMChlor_dark=float(input('What is the value of WQM Chlorophyll dark counts?'))
    WQMTurb_dark=float(input('What is the value of WQM Turbidity dark counts?'))
    
    Old_WQMChlA=(WQM_Chlor_counts-WQMChlor_dark)*ChlorSF
    Old_WQMTurbNTU=(WQM_Turb_counts-WQMTurb_dark)*TurbSF
    
    #Now we have all of the values, so we can add them to the text file.
####Don't forget to close the WQM and put it back into standby mode in between stuff!!! After testing, close the bio wiper.

    text_choice_4=input('Has a text file been made for this WQM test for this date? (y/n)')
    if text_choice_4 == 'y':
        #If there has already been a text file created, we can go ahead and just open it and append to it.
        text=open(Name, 'a')
        text.write('FLNTUS Chlorophyll counts: ')
        text.write(str(F_Chlor_counts))
        text.write(' counts')
        text.write('\n')
        text.write('FLNTUS Turbidity counts: ')
        text.write(str(F_Turb_counts))
        text.write(' counts')
        text.write('\n')
        text.write('WQM Chlorophyll counts: ')
        text.write(str(WQM_Chlor_counts))
        text.write(' counts')
        text.write('\n')
        text.write('WQM Turbidity counts: ')
        text.write(str(WQM_Turb_counts))
        text.write(' counts')
        text.write('\n')
        text.write('FLNTUS ChlA: ')
        text.write(str(FChlA))
        text.write(' (ug/L)')
        text.write('\n')
        text.write('FLNTUS Turbidity NTU: ')
        text.write(str(FTurbNTU))
        text.write(' NTU')
        text.write('\n')
        text.write('Old WQM ChlA: ')
        text.write(str(Old_WQMChlA))
        text.write(' (ug/L)')
        text.write('\n')
        text.write('Old WQM Turbidity (NTU): ')
        text.write(str(Old_WQMTurbNTU))
        text.write(' NTU')
        text.write('\n')
        text.write('Old Chlorophyll Scaling Factor: ')
        text.write(str(ChlorSF))
        text.write('\n')
        text.write('Old Turbidity Scaling Factor: ')
        text.write(str(TurbSF))
        text.write('\n')
        text.close()
        
    if text_choice_4 == 'n':
        text=open(Name, 'w+')
        text.write('Date of collection: ')
        text.write(Date)
        text.write('\n')
        text.write('WQM Serial #: ')
        text.write(WQM_SN)
        text.write('\n')
        text.write('FLNTUS Chlorophyll counts: ')
        text.write(str(F_Chlor_counts))
        text.write(' counts')
        text.write('\n')
        text.write('FLNTUS Turbidity counts: ')
        text.write(str(F_Turb_counts))
        text.write(' counts')
        text.write('\n')
        text.write('WQM Chlorophyll counts: ')
        text.write(str(WQM_Chlor_counts))
        text.write(' counts')
        text.write('\n')
        text.write('WQM Turbidity counts: ')
        text.write(str(WQM_Turb_counts))
        text.write(' counts')
        text.write('\n')
        text.write('FLNTUS ChlA: ')
        text.write(str(FChlA))
        text.write(' (ug/L)')
        text.write('\n')
        text.write('FLNTUS Turbidity NTU: ')
        text.write(str(FTurbNTU))
        text.write(' NTU')
        text.write('\n')
        text.write('Old WQM ChlA: ')
        text.write(str(Old_WQMChlA))
        text.write(' (ug/L)')
        text.write('\n')
        text.write('Old WQM Turbidity (NTU): ')
        text.write(str(Old_WQMTurbNTU))
        text.write(' NTU')
        text.write('\n')
        text.write('Old Chlorophyll Scaling Factor: ')
        text.write(str(ChlorSF))
        text.write('\n')
        text.write('Old Turbidity Scaling Factor: ')
        text.write(str(TurbSF))
        text.write('\n')
        text.close()
 #End of Process 4
    print('Please turn off the WQM device, after closing the biowiper if it has not been closed.')
    
    
    
    
    
if Process ==5:
    print('You have selected Process 5 - New WQM Chlorophyll and Turbidity values, with new Scale Factor - Small Tanks')
    print('Please turn on the WQM, and immediately enter Standby mode.')
    New_ChlorSF=float(input('Please enter the settings menu and adjust the Cholorphyll scaling factor. What is the new scaling factor for the Chlorophyll test?'))
    New_TurbSF=float(input('Please enter the settings menu and adjust the Turbidity scaling factor. What is the new scaling factor for the Turbidity test?'))
    print('Please turn off the WQM device.')
    #WQM Section:
    #print('Do not turn on the WQM device until you are ready to take data. Wait to turn on the device until prompted to do so.\n')
    
    time.sleep(5)

    input('Once you are ready to take data, turn on the device. Press ENTER to define the WQM serial port and change to optics mode.Do this immediately after stirring, it will take 1 min for this process to be completed.\n')

    #Define the WQM serial port:
    time.sleep(30)
    print('Defining the serial port')
    time.sleep(5)
    WQMser=serial.Serial(
        port=('COM4'),
        baudrate=19200,
        timeout=0
    )
    print('Entering Standby Mode')
    WQMser.write("!!!!!".encode('utf-8'))
    time.sleep(10)
    print('Entering Optics Mode')
    WQMser.write("$ECO\r\n".encode('utf-8'))
    time.sleep(5)
    WQMser.write("$PKT 0\r\n$run\r\n".encode('utf-8'))

    time.sleep(5)

    WQMser.close()
    
    time.sleep(5)
    print('WQM serial port is now available for data collection\n')
    input("Press Enter to collect WQM Chlorophyll data: Immediately")
    WQMser.open()
    #Define WQM Chloro list:
    WQMChlor=list()
    WQMChlorTime=numpy.array([])
    #define time as a counter variable:
    t=t1=int(time.time())

    print('Data is being collected: ')
    
    #Collection loop for WQM Chloro:
    while t<=t1+120:
        if WQMser.inWaiting()>0:
            WQMChlor.append(WQMser.read())
            WQMChlorTime=numpy.append(WQMChlorTime, int(t))
        t=time.time()
    
    WQMser.write("**********".encode('utf-8'))
    time.sleep(15)
    WQMser.write("$MVS 0\r\n".encode('utf-8')) #Closes the biowiper
    time.sleep(10)
    WQMser.close()
    print(WQMChlor)
    
    input('Press Enter to collect WQM Turbidity data: 40 seconds after stirring')
    WQMser.open()
    time.sleep(10)
    print('Entering Optics Mode')
    WQMser.write("$ECO\r\n".encode('utf-8'))
    time.sleep(5)
    WQMser.write("$PKT 0\r\n$run\r\n".encode('utf-8'))
    time.sleep(5)
  
    #define the WQM Turbidity list:
    WQMTurb=list()
    WQMTurbTime=numpy.array([])
    #define time as a counter variable:
    t=t3=int(time.time())

    print('Data is being collected: ')#20 sec after pressing enter
    
    #Collection loop for WQM Turb:

    while t<=t3+120:
        if WQMser.inWaiting()>0:
            WQMTurb.append(WQMser.read())
            WQMTurbTime=numpy.append(WQMTurbTime, int(t))
        t=time.time()
    time.sleep(10)
    WQMser.write("**********".encode('utf-8')) #Standby mode in Optics
    time.sleep(15)
    WQMser.write("$MVS 0\r\n".encode('utf-8')) #Closes the biowiper
    time.sleep(10)
    WQMser.close()
    print(WQMTurb)
    
    print('\n\n\n Check that the biowiper has closed on the WQM. If it has not closed, enter TeraTerm upon completion of this run and close the biowiper before turning off the device.')
    
    #Decoding all of the lists:
    WQMChlor_data=(b''.join(WQMChlor)).decode('utf-8', errors='ignore')
    print(WQMChlor_data)
    WQMTurb_data=(b''.join(WQMTurb)).decode('utf-8', errors ='ignore')
    print(WQMTurb_data)
    
    #Parse the WQM data:
    WQMChlor_data=WQMChlor_data.split()
    WQMTurb_data=WQMTurb_data.split()
    del WQMChlor_data[0:30]
    del WQMTurb_data[0:30]
    WQMChlor_num=list()
    WQMTurb_num=list()
    for x in WQMChlor_data:
        if x.isdigit()==True:
            WQMChlor_num.append(x)
    for x in WQMTurb_data:
        if x.isdigit()==True:
            WQMTurb_num.append(x)
    WQMChlor_data=WQMChlor_num
    WQMTurb_data=WQMTurb_num
    
    #Now, they should each be lists of digits. Make them into numpy arrays now:
    WQMChlor_data=numpy.asarray(WQMChlor_data, dtype=numpy.float32)
    WQMTurb_data=numpy.asarray(WQMTurb_data, dtype=numpy.float32)
    
    #They are 1D arrays, they need to be reshaped so we can extract the digits.
    WQMCol=5
    WQMChlorRow=int((len(WQMChlor_data)/5))
    print(WQMCol)
    print(WQMChlorRow)
    WQMTurbRow=int((len(WQMTurb_data)/5))
    print(WQMTurbRow)
    WQMChlor_data=numpy.reshape(WQMChlor_data, (WQMChlorRow,WQMCol))
    WQMTurb_data=numpy.reshape(WQMTurb_data, (WQMTurbRow,WQMCol))
    
    #Need to transpose them in order to do the math:
    WQMChlor_data=numpy.transpose(WQMChlor_data)
    WQMTurb_data=numpy.transpose(WQMTurb_data)
    
    #Need to extract the mean number of counts of Chlorophyll and Turbidity for each of them
    #For the WQM:
    WQM_Chlor_counts=numpy.mean(WQMChlor_data[1])
    WQM_Turb_counts=numpy.mean(WQMTurb_data[3])
    WQMChlor_dark=float(input('What is the value of WQM Chlorophyll dark counts?'))
    WQMTurb_dark=float(input('What is the value of WQM Turbidity dark counts?'))
    
    New_WQMChlA=(WQM_Chlor_counts-WQMChlor_dark)*ChlorSF
    New_WQMTurbNTU=(WQM_Turb_counts-WQMTurb_dark)*TurbSF
    
    #Now we have all of the values, so we can add them to the text file.
####Don't forget to close the WQM and put it back into standby mode in between stuff!!! After testing, close the bio wiper.

    text_choice_5=input('Has a text file been made for this WQM test for this date? (y/n)')
    if text_choice_5 == 'y':
        #If there has already been a text file created, we can go ahead and just open it and append to it.
        text=open(Name, 'a')
        
        text.write('WQM Chlorophyll counts: ')
        text.write(str(WQM_Chlor_counts))
        text.write(' counts')
        text.write('\n')
        text.write('WQM Turbidity counts: ')
        text.write(str(WQM_Turb_counts))
        text.write(' counts')
        text.write('\n')
        
        text.write('New WQM ChlA: ')
        text.write(str(New_WQMChlA))
        text.write(' (ug/L)')
        text.write('\n')
        text.write('New WQM Turbidity (NTU): ')
        text.write(str(New_WQMTurbNTU))
        text.write(' NTU')
        text.write('\n')
        text.write('New Chlorophyll Scaling Factor: ')
        text.write(str(New_ChlorSF))
        text.write('\n')
        text.write('New Turbidity Scaling Factor: ')
        text.write(str(New_TurbSF))
        text.write('\n')
        text.close()
        
    if text_choice_5 == 'n':
        text=open(Name, 'w+')
        text.write('Date of collection: ')
        text.write(Date)
        text.write('\n')
        text.write('WQM Serial #: ')
        text.write(WQM_SN)
        text.write('\n')
        text.write('FLNTUS Chlorophyll counts: ')
        text.write(str(F_Chlor_counts))
        text.write(' counts')
        text.write('\n')
        text.write('FLNTUS Turbidity counts: ')
        text.write(str(F_Turb_counts))
        text.write(' counts')
        text.write('\n')
        text.write('WQM Chlorophyll counts: ')
        text.write(str(WQM_Chlor_counts))
        text.write(' counts')
        text.write('\n')
        text.write('WQM Turbidity counts: ')
        text.write(str(WQM_Turb_counts))
        text.write(' counts')
        text.write('\n')
        text.write('FLNTUS ChlA: ')
        text.write(str(FChlA))
        text.write(' (ug/L)')
        text.write('\n')
        text.write('FLNTUS Turbidity NTU: ')
        text.write(str(FTurbNTU))
        text.write(' NTU')
        text.write('\n')
        text.write('New WQM ChlA: ')
        text.write(str(New_WQMChlA))
        text.write(' (ug/L)')
        text.write('\n')
        text.write('New WQM Turbidity (NTU): ')
        text.write(str(New_WQMTurbNTU))
        text.write(' NTU')
        text.write('\n')
        text.write('New Chlorophyll Scaling Factor: ')
        text.write(str(ChlorSF))
        text.write('\n')
        text.write('New Turbidity Scaling Factor: ')
        text.write(str(TurbSF))
        text.write('\n')
        text.close()
 #End of Process 5
    print('Please turn off the WQM device, after closing the biowiper if it has not been closed.')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#end code!