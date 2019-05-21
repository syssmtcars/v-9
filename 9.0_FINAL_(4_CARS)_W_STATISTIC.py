import cv2
import numpy
import paho.mqtt.client as mqtt
from tkinter import *
import sys
import pygame as pg
import threading
import os

cross_letter= 'ab'
root = Tk()
root.title('buttons')
root.geometry('300x500')


sound_flag = False
cap = cv2.VideoCapture(2)



# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75) #0.25 - off, 0.75 - on
# cap.set(cv2.CAP_PROP_GAIN, 1) #0.25 - off, 0.75 - on
# cap.set(cv2.CAP_PROP_CONVERT_RGB, 1) #0.25 - off, 0.75 - on
#cap.set(cv2.CAP_PROP_CONTRAST, 0.15)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,1000)
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)

# cap.set(cv2.CAP_PROP_EXPOSURE, -7.0)

com1Mas = []
crosses1Mas = []
com1 = open('motionYellow.txt')
crosses1 = open('crossesYellow.txt')
m_unit_1 = []
j=0






# root.update()






for line in com1:
    com1Mas.append(line[0])
#print(com1Mas)

for line in crosses1:
    m_unit_1.append([])
    for i in range(2):
        if i==0:
            m_unit_1[j].append(com1Mas[j])
        else:
            m_unit_1[j].append(line[0]+line[1])
    j=j+1
print(m_unit_1)

#            a1        a2        a3     b1     b2     b3
m_unit_yellow = m_unit_1#[['l','b3'],['l','a3'],['f','a2'],['l','a1'],['l','b1'],['l','b2'], ['r','a2'],['r','a3'],['r','b3'],['f','b2'],['r','b1'],['r','a1'],['r','a2'],['l','b2'],['cycle', 'b3']]#m_unit_1
# m_unit_yellow = ['none','left','left','none','left','left'] #a1 to b3
m_unit_blue = [['r', 'b1'], ['r', 'a1'], ['r', 'a2'], ['l', 'b2'],['l', 'b3'],['l', 'a3'],['l', 'a2'],['r', 'b2'],['cycle','b1']]
m_unit_red = [['r','b2'],['r','a2'],['r','a3'], ['r','b3'],['cycle', 'b2']]
m_unit_purple = [['l','b2'],['l','b3'],['l','a3'],['l','a2'],['cycle', 'b2']]
who_is_first=['','','','','',''] #number of crosses
old_who_is_first='hello'
flag_who_is_first='hello'
order_in_cross='haos'

handle = open("red.txt", "r")
h_down_g = int(handle.readline())
s_down_g = int(handle.readline())
v_down_g = int(handle.readline())
h_up_g = int(handle.readline())
s_up_g = int(handle.readline())
v_up_g = int(handle.readline())
print(h_down_g, s_down_g)
handle2 = open('cropMe.txt', 'r')
handle3 = open('a1.txt', 'r')
handle4 = open('a2.txt', 'r')
handle5 = open('a3.txt', 'r')
handle6 = open('b1.txt', 'r')
handle7 = open('b2.txt', 'r')
handle8 = open('b3.txt', 'r')
handle9 = open('yellow.txt', 'r')
handle10 = open('blue.txt', 'r')
handle11 = open('red.txt', 'r')
handle12 = open('purple.txt','r')

x = int(handle2.readline())
y = int(handle2.readline())
h = int(handle2.readline())
w = int(handle2.readline())

a11 = int(handle3.readline())
a12 = int(handle3.readline())
a13 = int(handle3.readline())
a14 = int(handle3.readline())

a21 = int(handle4.readline())
a22 = int(handle4.readline())
a23 = int(handle4.readline())
a24 = int(handle4.readline())

a31 = int(handle5.readline())
a32 = int(handle5.readline())
a33 = int(handle5.readline())
a34 = int(handle5.readline())

b11 = int(handle6.readline())
b12 = int(handle6.readline())
b13 = int(handle6.readline())
b14 = int(handle6.readline())

b21 = int(handle7.readline())
b22 = int(handle7.readline())
b23 = int(handle7.readline())
b24 = int(handle7.readline())

b31 = int(handle8.readline())
b32 = int(handle8.readline())
b33 = int(handle8.readline())
b34 = int(handle8.readline())

h_down_y = int(handle9.readline())
s_down_y = int(handle9.readline())
v_down_y = int(handle9.readline())
h_up_y = int(handle9.readline())
s_up_y = int(handle9.readline())
v_up_y = int(handle9.readline())

h_down_b = int(handle10.readline())
s_down_b = int(handle10.readline())
v_down_b = int(handle10.readline())
h_up_b = int(handle10.readline())
s_up_b = int(handle10.readline())
v_up_b = int(handle10.readline())

h_down_r = int(handle11.readline())
s_down_r = int(handle11.readline())
v_down_r = int(handle11.readline())
h_up_r = int(handle11.readline())
s_up_r = int(handle11.readline())
v_up_r = int(handle11.readline())

h_down_p = int(handle12.readline())
s_down_p = int(handle12.readline())
v_down_p = int(handle12.readline())
h_up_p = int(handle12.readline())
s_up_p = int(handle12.readline())
v_up_p= int(handle12.readline())
# !VAR
number_of_cars=3 #4 of course (0,1,2)
cross_letter= 'ab'


old_yellow_msg='r'
old_blue_msg='r'
old_red_msg='r'
old_purple_msg='r'
global_msg_yellow = ''
global_msg_blue = ''
global_msg_red = ''
global_msg_purple=''
old_message ='Privet'

global_msg = ''

cross_counter_of_cars = []
cross_counter_of_motion = [] #0123 = sflr

for i in range(6):
    cross_counter_of_cars.append(0)
    cross_counter_of_motion.append([0]*4)

print(cross_counter_of_motion)

red_inzone = (51, 0, 255)

CASE_SUBJECT='None'

n_yellow = 0
n_blue = 0
n_red = 0
n_purple = 0

f = 0

old_cross_yellow= 'notcross'
old_cross_blue = 'notcross'
old_cross_red= 'notcross'
old_cross_purple='notcross'



cross_yellow = 'notcross'
cross_blue = 'notcross'
cross_red= 'notcross'
cross_purple='notcross'
# !/VAR

flag_start = False
flag_start_yellow = False
flag_stop = False

client = mqtt.Client()
client.connect('192.168.1.2')

center_a1 = (int((a13 - a11) / 2) + a11, int((a14 - a12) / 2) + a12)
center_a2 = (int((a23 - a21) / 2) + a21, int((a24 - a22) / 2) + a22)
center_a3 = (int((a33 - a31) / 2) + a31, int((a34 - a32) / 2) + a32)
center_b1 = (int((b13 - b11) / 2) + b11, int((b14 - b12) / 2) + b12)
center_b2 = (int((b23 - b21) / 2) + b21, int((b24 - b22) / 2) + b22)
center_b3 = (int((b33 - b31) / 2) + b31, int((b34 - b32) / 2) + b32)

def flag_start_refactor(event):
    global flag_start
    flag_start = True
    print(global_msg)

def flag_start_refactor_yellow(event):
    global flag_start_yellow
    flag_start_yellow = True
    print(global_msg)

def flag_stop_refactor(event):
    global flag_stop
    flag_stop = True
    # global_msg = 'ssss'
    # print(global_msg)
    # client.publish('syssmtcars',global_msg)

btn = Button(root,text = 'start')
btn.grid(column = 1,row = 0)

btnyellow = Button(root,text = 'start yellow')
btnyellow.grid(column = 0,row = 0)

btnstop = Button(root,text = 'stop all')
btnstop.grid(column = 0,row = 1)

while True:

    _, image_original = cap.read()
    image = image_original[y:y + h, x:x + w]

    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)

    mask = cv2.inRange(img_hsv, numpy.array([h_down_y, s_down_y, v_down_y]), numpy.array([h_up_y, s_up_y, v_up_y]))
    mask_blue = cv2.inRange(img_hsv, numpy.array([h_down_b, s_down_b, v_down_b]), numpy.array([h_up_b, s_up_b, v_up_b]))
    mask_red = cv2.inRange(img_hsv, numpy.array([h_down_r, s_down_r, v_down_r]), numpy.array([h_up_r, s_up_r, v_up_r]))
    mask_purple = cv2.inRange(img_hsv, numpy.array([h_down_p, s_down_p, v_down_p]), numpy.array([h_up_p, s_up_p, v_up_p]))

    _, contours0_yellow, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    _, contours0_blue , hierarchy_blue = cv2.findContours(mask_blue.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    _, contours0_red , hierarchy_red = cv2.findContours(mask_red.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    _, contours0_purple, hierarchy_purple = cv2.findContours(mask_purple.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Yellow Unit1

    for cnt_yellow in contours0_yellow:

        rect = cv2.minAreaRect(cnt_yellow)
        box = cv2.boxPoints(rect)
        box = numpy.int0(box)
        area = int(rect[1][0] * rect[1][1])
        if area > 100:
            center_yellow = (int(rect[0][0]), int(rect[0][1]))
            ifA1 = center_yellow[0] > a11 and center_yellow[0] < a13 and center_yellow[1] > a12 and center_yellow[1] < a14
            ifA2 = center_yellow[0] > a21 and center_yellow[0] < a23 and center_yellow[1] > a22 and center_yellow[1] < a24
            ifA3 = center_yellow[0] > a31 and center_yellow[0] < a33 and center_yellow[1] > a32 and center_yellow[1] < a34
            ifB1 = center_yellow[0] > b11 and center_yellow[0] < b13 and center_yellow[1] > b12 and center_yellow[1] < b14
            ifB2 = center_yellow[0] > b21 and center_yellow[0] < b23 and center_yellow[1] > b22 and center_yellow[1] < b24
            ifB3 = center_yellow[0] > b31 and center_yellow[0] < b33 and center_yellow[1] > b32 and center_yellow[1] < b34
            k = center_yellow
            cv2.drawContours(image, [box], 0, (255, 0, 0), 2)
            cv2.circle(image, center_yellow, 2, (0, 255, 0), 1)
            # print(center_yellow)


            if ifA1:
                cv2.putText(image, "in zone a1", center_yellow, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_yellow = 'a1'

            elif ifA2:
                cv2.putText(image, "in zone a2", center_yellow, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_yellow = 'a2'

            elif ifA3:
                cv2.putText(image, "in zone a3", center_yellow, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_yellow = 'a3'

            elif ifB1:
                cv2.putText(image, "in zone b1", center_yellow, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_yellow = 'b1'

            elif ifB2:
                cv2.putText(image, "in zone b2", center_yellow, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_yellow = 'b2'

            elif ifB3:
                cv2.putText(image, "in zone b3", center_yellow, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_yellow = 'b3'
            else:
                cross_yellow = 'notcross'

                # logic step

            # if ifA1 or ifA2 or ifA3 or ifB1 or ifB2 or ifB3:
            if cross_yellow == m_unit_yellow[n_yellow][1]:
                global_msg_yellow = m_unit_yellow[n_yellow][0]
                #print('command: ' + m_unit_yellow[n_yellow][0])
                #print('n_yellow: ' + str(n_yellow))
                old_yellow_msg=global_msg_yellow
                old_cross_yellow = cross_yellow
                #print({'cross_yellow': str(cross_yellow), 'old_cross_yellow': str(old_cross_yellow)})

            elif m_unit_yellow[n_yellow + 1][0] == 's':
                #print('stop')
                global_msg_yellow = 's'

            elif m_unit_yellow[n_yellow + 1][0] == 'cycle':
                n_yellow = 0


            elif cross_yellow == m_unit_yellow[n_yellow + 1][1]:
                n_yellow += 1


            elif cross_yellow == 'notcross':
                global_msg_yellow = old_yellow_msg
                #client.publish('syssmtcars', 'forward')
                #print('forward')
                #print({'cross_yellow': str(cross_yellow), 'old_cross_yellow': str(old_cross_yellow)})

            # else:
        #       client.publish('syssmtcars', 'forward')
        #       print('forward')
        #       old_cross_yellow = cross_yellow

        # client.publish('syssmtcars', 'forward')


    # Blue Unit 2

    for cnt_blue in contours0_blue:

        rect = cv2.minAreaRect(cnt_blue)
        box = cv2.boxPoints(rect)
        box = numpy.int0(box)
        area = int(rect[1][0] * rect[1][1])
        if area > 100:
            center_blue = (int(rect[0][0]), int(rect[0][1]))
            ifA1 = center_blue[0] > a11 and center_blue[0] < a13 and center_blue[1] > a12 and center_blue[1] < a14
            ifA2 = center_blue[0] > a21 and center_blue[0] < a23 and center_blue[1] > a22 and center_blue[1] < a24
            ifA3 = center_blue[0] > a31 and center_blue[0] < a33 and center_blue[1] > a32 and center_blue[1] < a34
            ifB1 = center_blue[0] > b11 and center_blue[0] < b13 and center_blue[1] > b12 and center_blue[1] < b14
            ifB2 = center_blue[0] > b21 and center_blue[0] < b23 and center_blue[1] > b22 and center_blue[1] < b24
            ifB3 = center_blue[0] > b31 and center_blue[0] < b33 and center_blue[1] > b32 and center_blue[1] < b34
            cv2.drawContours(image, [box], 0, (255, 255, 0), 2)
            cv2.circle(image, center_blue, 2, (0, 255, 0), 1)
            # print(center, a11, a12, a13, a14)

            if ifA1:
                cv2.putText(image, "in zone a1", center_blue, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_blue = 'a1'

            elif ifA2:
                cv2.putText(image, "in zone a2", center_blue, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_blue  = 'a2'

            elif ifA3:
                cv2.putText(image, "in zone a3", center_blue, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_blue  = 'a3'

            elif ifB1:
                cv2.putText(image, "in zone b1", center_blue, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_blue  = 'b1'

            elif ifB2:
                cv2.putText(image, "in zone b2", center_blue, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_blue = 'b2'

            elif ifB3:
                cv2.putText(image, "in zone b3", center_blue, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_blue = 'b3'
            else:
                cross_blue = 'notcross'


            #logic step

            if cross_blue == m_unit_blue[n_blue][1]:
                global_msg_blue = m_unit_blue[n_blue][0]
                #print('command: ' + m_unit_blue[n_blue][0])
                #print('n_blue: ' + str(n_yellow))
                old_blue_msg=global_msg_blue
                old_cross_blue = cross_blue
                #print({'cross_blue': str(cross_blue), 'old_cross_blue': str(old_cross)})

            elif m_unit_blue[n_blue + 1][1] == 'lastcross':
                #print('stop')
                global_msg_blue = 's'

            elif m_unit_blue[n_blue + 1][0] == 'cycle':
                n_blue = 0

            elif cross_blue == m_unit_blue[n_blue + 1][1]:
                n_blue += 1


            elif cross_blue == 'notcross':
                global_msg_blue = old_blue_msg
                #print('forward')
             # print({'cross_blue': str(cross_blue), 'old_cross_blue': str(old_cross_blue)})

        ################################################################
        ################################################################
        ################################################################
        # Red Unit 3

    for cnt_red in contours0_red:

        rect = cv2.minAreaRect(cnt_red)
        box = cv2.boxPoints(rect)
        box = numpy.int0(box)
        area = int(rect[1][0] * rect[1][1])
        if area > 300:
            center_red = (int(rect[0][0]), int(rect[0][1]))
            ifA1 = center_red[0] > a11 and center_red[0] < a13 and center_red[1] > a12 and center_red[1] < a14
            ifA2 = center_red[0] > a21 and center_red[0] < a23 and center_red[1] > a22 and center_red[1] < a24
            ifA3 = center_red[0] > a31 and center_red[0] < a33 and center_red[1] > a32 and center_red[1] < a34
            ifB1 = center_red[0] > b11 and center_red[0] < b13 and center_red[1] > b12 and center_red[1] < b14
            ifB2 = center_red[0] > b21 and center_red[0] < b23 and center_red[1] > b22 and center_red[1] < b24
            ifB3 = center_red[0] > b31 and center_red[0] < b33 and center_red[1] > b32 and center_red[1] < b34
            cv2.drawContours(image, [box], 0, (0, 0, 0), 2)
            cv2.circle(image, center_red, 2, (0, 0, 0), 1)
            # print(center, a11, a12, a13, a14)

            if ifA1:
                cv2.putText(image, "in zone a1", center_red, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_red = 'a1'

            elif ifA2:
                cv2.putText(image, "in zone a2", center_red, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_red  = 'a2'

            elif ifA3:
                cv2.putText(image, "in zone a3", center_red, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_red  = 'a3'

            elif ifB1:
                cv2.putText(image, "in zone b1", center_red, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_red  = 'b1'

            elif ifB2:
                cv2.putText(image, "in zone b2", center_red, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_red = 'b2'

            elif ifB3:
                cv2.putText(image, "in zone b3", center_red, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_red = 'b3'
            else:
                cross_red = 'notcross'


            #logic step

            if cross_red == m_unit_red[n_red][1]:
                global_msg_red = m_unit_red[n_red][0]
                #print('command: ' + m_unit_blue[n_blue][0])
                #print('n_blue: ' + str(n_yellow))
                old_red_msg=global_msg_red
                old_cross_red = cross_red
                #print({'cross_red': str(cross_red), 'old_cross_red': str(old_cross)})

            elif m_unit_red[n_red + 1][1] == 'lastcross':
                #print('stop')
                global_msg_red = 's'

            elif m_unit_red[n_red + 1][0] == 'cycle':
                n_red = 0

            elif cross_red == m_unit_red[n_red + 1][1]:
                n_red += 1


            elif cross_red == 'notcross':
                global_msg_red = old_red_msg
                #print('forward')
    
    
    
    
    ##############################################3
    #TODO Purple
    
    for cnt_purple in contours0_purple:

        rect = cv2.minAreaRect(cnt_purple)
        box = cv2.boxPoints(rect)
        box = numpy.int0(box)
        area = int(rect[1][0] * rect[1][1])
        if area > 200:
            center_purple = (int(rect[0][0]), int(rect[0][1]))
            ifA1 = center_purple[0] > a11 and center_purple[0] < a13 and center_purple[1] > a12 and center_purple[1] < a14
            ifA2 = center_purple[0] > a21 and center_purple[0] < a23 and center_purple[1] > a22 and center_purple[1] < a24
            ifA3 = center_purple[0] > a31 and center_purple[0] < a33 and center_purple[1] > a32 and center_purple[1] < a34
            ifB1 = center_purple[0] > b11 and center_purple[0] < b13 and center_purple[1] > b12 and center_purple[1] < b14
            ifB2 = center_purple[0] > b21 and center_purple[0] < b23 and center_purple[1] > b22 and center_purple[1] < b24
            ifB3 = center_purple[0] > b31 and center_purple[0] < b33 and center_purple[1] > b32 and center_purple[1] < b34
            cv2.drawContours(image, [box], 0, (0, 100, 0), 2)
            cv2.circle(image, center_purple, 2, (0, 0, 0), 1)
            # print(center, a11, a12, a13, a14)

            if ifA1:
                cv2.putText(image, "in zone a1", center_purple, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_purple = 'a1'

            elif ifA2:
                cv2.putText(image, "in zone a2", center_purple, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_purple  = 'a2'

            elif ifA3:
                cv2.putText(image, "in zone a3", center_purple, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_purple  = 'a3'

            elif ifB1:
                cv2.putText(image, "in zone b1", center_purple, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_purple  = 'b1'

            elif ifB2:
                cv2.putText(image, "in zone b2", center_purple, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_purple = 'b2'

            elif ifB3:
                cv2.putText(image, "in zone b3", center_purple, cv2.FONT_HERSHEY_SIMPLEX, 0.4, red_inzone, 2)
                cross_purple = 'b3'
            else:
                cross_purple = 'notcross'


            #logic step

            if cross_purple == m_unit_purple[n_purple][1]:
                global_msg_purple = m_unit_purple[n_purple][0]
                #print('command: ' + m_unit_blue[n_blue][0])
                #print('n_blue: ' + str(n_yellow))
                old_purple_msg=global_msg_purple
                old_cross_purple = cross_purple
                #print({'cross_purple': str(cross_purple), 'old_cross_purple': str(old_cross)})

            elif m_unit_purple[n_purple + 1][1] == 'lastcross':
                #print('stop')
                global_msg_purple = 's'

            elif m_unit_purple[n_purple + 1][0] == 'cycle':
                n_purple = 0

            elif cross_purple == m_unit_purple[n_purple + 1][1]:
                n_purple += 1


            elif cross_purple == 'notcross':
                global_msg_purple = old_purple_msg
                #print('forward')
    
    
    #TODO END OF purple 
    
    
    
    
    
    
    
    # CROSSROAD LOGISTIC

    CASE_SUBJECT = 'None'



    ############# What unit is the first in a cross

    #Создаем очередь

    old_who_is_first = flag_who_is_first
    flag_who_is_first=''
    number_of_cross = 0
    for i in range(len(cross_letter)):
        for j in range(1,4):
            cross_name=cross_letter[i]+str(j)

            if cross_name==cross_yellow and who_is_first[number_of_cross].find('YL')<0:
                who_is_first[number_of_cross]=who_is_first[number_of_cross]+'YL:'+m_unit_yellow[n_yellow][0]+';'

            if cross_name!=cross_yellow and who_is_first[number_of_cross].find('YL')>=0:
                l = who_is_first[number_of_cross].find('YL')
                who_is_first[number_of_cross]=str(who_is_first[number_of_cross][:l]+who_is_first[number_of_cross][l+5:])


            if cross_name==cross_blue and who_is_first[number_of_cross].find('BL')<0:
                who_is_first[number_of_cross]=who_is_first[number_of_cross]+'BL:'+m_unit_blue[n_blue][0]+';'

            if cross_name != cross_blue and who_is_first[number_of_cross].find('BL') >= 0:

                l = who_is_first[number_of_cross].find('BL')
                who_is_first[number_of_cross] = str(
                    who_is_first[number_of_cross][:l] + who_is_first[number_of_cross][l + 5:])


            if cross_name==cross_red and who_is_first[number_of_cross].find('RD')<0:
                who_is_first[number_of_cross]=who_is_first[number_of_cross]+'RD:'+m_unit_red[n_red][0]+';'

            if cross_name != cross_red and who_is_first[number_of_cross].find('RD') >= 0:
                l = who_is_first[number_of_cross].find('RD')
                who_is_first[number_of_cross] = str(
                    who_is_first[number_of_cross][:l] + who_is_first[number_of_cross][l + 5:])
                
                
            if cross_name==cross_purple and who_is_first[number_of_cross].find('PP')<0:
                who_is_first[number_of_cross]=who_is_first[number_of_cross]+'PP:'+m_unit_purple[n_purple][0]+';'

            if cross_name != cross_purple and who_is_first[number_of_cross].find('PP') >= 0:
                l = who_is_first[number_of_cross].find('PP')
                who_is_first[number_of_cross] = str(
                    who_is_first[number_of_cross][:l] + who_is_first[number_of_cross][l + 5:])
                
                
            flag_who_is_first = flag_who_is_first+str(number_of_cross) + who_is_first[number_of_cross]

            number_of_cross += 1




    # Конец создания очереди





# Логика разъезда на перекрестках
    if m_unit_yellow[0][1] == cross_yellow and sound_flag == False:

        pg.init()
        pg.mixer.Sound('audio.wav').play()
        sound_flag = True


    number_of_cross = 0
    for i in range(len(cross_letter)):
        for j in range(1, 4):
            cross_name = cross_letter[i] + str(j)

            order_in_cross=who_is_first[number_of_cross]

            if order_in_cross.find('YL')>=5 :# if secorder_in_crossnd unit is yellow
                decision_var=order_in_cross[3]+order_in_cross[8]
                # print(decision_var)

                if decision_var=='lr' or decision_var=='fr' or decision_var == 'rl':
                    if m_unit_yellow[n_yellow + 1][1] == m_unit_blue[n_blue + 1][1] \
                            or m_unit_yellow[n_yellow + 1][
                                1] == m_unit_red[n_red + 1][1] \
                            or m_unit_yellow[n_yellow + 1][1] == m_unit_purple[n_purple + 1][1]:  # Т.е.следующие cross совпадают
                                global_msg_yellow='s'
                                CASE_SUBJECT=decision_var
                        
                if decision_var == 'lf' or decision_var == 'fl':
                    global_msg_yellow = 's'
                    CASE_SUBJECT = decision_var
                if decision_var == 'll':
                    global_msg_yellow = 's'
                    CASE_SUBJECT = decision_var

                if decision_var == 'ff':
                    if (m_unit_yellow[n_yellow][1][1] != m_unit_yellow[n_yellow+1][1][1] and m_unit_blue[n_blue][1][1] != m_unit_blue[n_blue+1][1][1]):
                        global_msg_yellow='s'
                        CASE_SUBJECT=decision_var

                    if (m_unit_yellow[n_yellow][1][1] != m_unit_yellow[n_yellow+1][1][1] and m_unit_purple[n_purple][1][1] != m_unit_purple[n_purple+1][1][1]):
                        global_msg_yellow='s'
                        CASE_SUBJECT=decision_var
                        

            if order_in_cross.find('BL')>=5:
                decision_var = order_in_cross[3] + order_in_cross[8]
                # print(decision_var)
                if decision_var == 'lr' or decision_var == 'fr'or decision_var == 'rl':
                    if m_unit_blue[n_blue + 1][1] == m_unit_yellow[n_yellow + 1][1] or m_unit_blue[n_blue + 1][
                        1] == m_unit_red[n_red + 1][1] or m_unit_blue[n_blue + 1][1] == m_unit_purple[n_purple + 1][1]:  # Т.е.следующие cross совпадают
                        global_msg_blue = 's'
                        CASE_SUBJECT = decision_var

                if decision_var == 'lf' or decision_var == 'fl':
                    global_msg_blue = 's'
                    CASE_SUBJECT = decision_var
                if decision_var == 'll':
                    global_msg_blue = 's'
                    CASE_SUBJECT = decision_var

                if decision_var == 'ff':
                    if (m_unit_blue[n_blue][1][1] != m_unit_blue[n_blue + 1][1][1] and m_unit_yellow[n_yellow][1][1] != m_unit_yellow[n_yellow + 1][1][1]):
                        global_msg_blue = 's'
                        CASE_SUBJECT = decision_var
                    
                    if (m_unit_blue[n_blue][1][1] != m_unit_blue[n_blue + 1][1][1] and m_unit_purple[n_purple][1][1] != m_unit_purple[n_purple + 1][1][1]):
                        global_msg_blue = 's'
                        CASE_SUBJECT = decision_var
                global_msg_purple='s'
                CASE_SUBJECT = 'LOW Priority of purple'
                        

            if order_in_cross.find('RD')>=5:
                global_msg_red='s'
                CASE_SUBJECT = 'LOW Priority of red'


            #Чтобы юниты не догоняли друг друга



            if m_unit_yellow[n_yellow] == m_unit_blue[n_blue+1] and cross_blue =='notcross':
                global_msg_blue='s'
            if m_unit_yellow[n_yellow] == m_unit_red[n_red+1] and cross_red=='notcross':
                global_msg_red='s'
            if  m_unit_yellow[n_yellow] == m_unit_purple[n_purple+1]and cross_purple=='notcross':
                global_msg_purple='s'

            if m_unit_blue[n_blue] == m_unit_yellow[n_yellow+1] and cross_yellow=='notcross':
                global_msg_yellow='s'
            if m_unit_blue[n_blue] == m_unit_red[n_red+1] and cross_red=='notcross':
                global_msg_red='s'
            if  m_unit_blue[n_blue] == m_unit_purple[n_purple+1] and cross_purple=='notcross':
                global_msg_purple='s'

            if m_unit_red[n_red] == m_unit_yellow[n_yellow+1] and cross_yellow=='notcross':
                   global_msg_yellow='s'
            if m_unit_red[n_red] == m_unit_blue[n_blue+1] and cross_blue=='notcross':
                   global_msg_blue='s'
            if  m_unit_red[n_red] == m_unit_purple[n_purple+1] and cross_purple=='notcross':
                   global_msg_purple='s'

            if m_unit_purple[n_purple] == m_unit_yellow[n_yellow+1] and cross_yellow=='notcross':
                   global_msg_yellow='s'
            if m_unit_purple[n_purple] == m_unit_blue[n_blue+1] and cross_blue=='notcross':
                   global_msg_blue='s'
            if  m_unit_purple[n_purple] == m_unit_red[n_red+1] and cross_red=='notcross':
                   global_msg_red='s'




            #Стоп если впереди юнит в нейтральной зоне
            #
            # if m_unit_yellow[n_yellow] == m_unit_blue[n_blue] and cross_blue == 'notcross':
            #     global_msg_yellow = 's'
            # if m_unit_yellow[n_yellow] == m_unit_red[n_red] and cross_red == 'notcross':
            #     global_msg_yellow = 's'
            # if m_unit_yellow[n_yellow] == m_unit_purple[n_purple] and cross_purple == 'notcross':
            #     global_msg_yellow = 's'
            #
            # if m_unit_blue[n_blue] == m_unit_yellow[n_yellow] and cross_yellow == 'notcross':
            #     global_msg_blue = 's'
            # if m_unit_blue[n_blue] == m_unit_red[n_red] and cross_red == 'notcross':
            #     global_msg_blue = 's'
            # if m_unit_blue[n_blue] == m_unit_purple[n_purple] and cross_purple == 'notcross':
            #     global_msg_blue = 's'
            #
            # if m_unit_red[n_red] == m_unit_yellow[n_yellow] and cross_yellow == 'notcross':
            #     global_msg_red = 's'
            # if m_unit_red[n_red] == m_unit_blue[n_blue] and cross_blue == 'notcross':
            #     global_msg_red = 's'
            # if m_unit_red[n_red] == m_unit_purple[n_purple] and cross_purple == 'notcross':
            #     global_msg_red = 's'
            #
            # if m_unit_purple[n_purple] == m_unit_yellow[n_yellow] and cross_yellow == 'notcross':
            #     global_msg_purple = 's'
            # if m_unit_purple[n_purple] == m_unit_blue[n_blue] and cross_blue == 'notcross':
            #     global_msg_purple = 's'
            # if m_unit_purple[n_purple] == m_unit_red[n_red] and cross_red == 'notcross':
            #     global_msg_purple = 's'











            number_of_cross += 1

    #Printing of massive 'who is first'
    if flag_who_is_first != old_who_is_first:
        client.publish('statistic', str(who_is_first))
        print(str(who_is_first)+ ' '+ str(CASE_SUBJECT)+'F1')

        # statistic counter
        number_of_cross=0
        for i in range(len(cross_letter)):
            for j in range(1, 4):
                cross_name = cross_letter[i] + str(j)

                if who_is_first[number_of_cross].find(':') == 2:
                    cross_counter_of_cars[number_of_cross] = cross_counter_of_cars[number_of_cross] + 1

                if who_is_first[number_of_cross].find('s')== 3:
                    cross_counter_of_motion[number_of_cross][0]=cross_counter_of_motion[number_of_cross][0]+1

                if who_is_first[number_of_cross].find('f')== 3:
                    cross_counter_of_motion[number_of_cross][1]=cross_counter_of_motion[number_of_cross][1]+1

                if who_is_first[number_of_cross].find('l')== 3:
                    cross_counter_of_motion[number_of_cross][2]=cross_counter_of_motion[number_of_cross][2]+1

                if who_is_first[number_of_cross].find('r')==3:
                    cross_counter_of_motion[number_of_cross][3]=cross_counter_of_motion[number_of_cross][3]+1







                number_of_cross +=1


    #Кнопки в TKINTER

    btnyellow.bind('<Button-1>',flag_start_refactor_yellow)
    btn.bind('<Button-1>',flag_start_refactor)
    btnstop.bind('<Button-1>',flag_stop_refactor)
    root.update()

    if flag_start_yellow != True:
        global_msg_yellow = 's'

    if flag_start != True:
        global_msg_blue = 's'
        global_msg_red = 's'
        global_msg_purple = 's'

    if flag_stop==True:
        global_msg_yellow = 's'
        global_msg_blue = 's'
        global_msg_red = 's'
        global_msg_purple = 's'




        # end statistic counter












        # old_who_is_first = flag_who_is_first
    # flag_who_is_first = ''





    #TODO MARSHRUTIZER
    #TODO S
    #TODO 4 CARS





    #############END OF: What unit is the first in a cross





    #end of CROSSROAD LOGIC


    global_msg = str(global_msg_yellow+global_msg_blue+global_msg_red+global_msg_purple)
    # print(global_msg+' '+str(n_yellow)+' '+str(m_unit_yellow[n_yellow+1][1])+' '+str(n_blue)+' '+m_unit_blue[n_blue+1][1]+' '+CASE_SUBJECT)

    # print (abs(center[0]-center_blue[0]),abs(center[1]-center_blue[1]))






    if global_msg != old_message:
        client.publish('syssmtcars',global_msg)
        old_message = global_msg




        print(global_msg + ' ' + 'Yl:' + str(m_unit_yellow[n_yellow]) + ' ' + 'BL:' + str(m_unit_blue[n_blue]) + ' ' + 'RD' + str(m_unit_red[n_red])+' '+'PP'+str(m_unit_purple[n_purple]) +' '+CASE_SUBJECT + ' ' )

    else:
        pass
                            
    cv2.rectangle(image, (a11, a12), (a13, a14), (255, 0, 0))
    cv2.rectangle(image, (a21, a22), (a23, a24), (255, 0, 0))
    cv2.rectangle(image, (a31, a32), (a33, a34), (255, 0, 0))
    cv2.rectangle(image, (b11, b12), (b13, b14), (255, 0, 0))
    cv2.rectangle(image, (b21, b22), (b23, b24), (255, 0, 0))
    cv2.rectangle(image, (b31, b32), (b33, b34), (255, 0, 0))

    cv2.putText(image, "a1", center_a1, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "a2", center_a2, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "a3", center_a3, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "b1", center_b1, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "b2", center_b2, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)
    cv2.putText(image, "b3", center_b3, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 2, 2)

    ###cv2.imshow("mask", mask)


    cv2.imshow("original", image)




    if cv2.waitKey(1) == 27:
        client.publish('ssss')
        client.disconnect()
        break


                                  