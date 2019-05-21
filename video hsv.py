import cv2 #библиотека opencv
import numpy   #работа с массивами

#img = cv2.imread("8.jpg_640x640.jpg")   #читать изображение
cap = cv2.VideoCapture(2)             #читать видео поток

#cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) #0.25 - off, 0.75 - on
cap.set(cv2.CAP_PROP_CONTRAST, 0.25) #это помогает
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 1.55)
# cap.set(cv2.CAP_PROP_IRIS, 0.25)




handle = open(str(input()+'.txt'), "w")
cv2.namedWindow("hsv_bar")

def nothing(event):
    pass


cv2.createTrackbar("h_up", "hsv_bar", 255, 255, nothing)
cv2.createTrackbar("s_up", "hsv_bar", 255, 255, nothing)
cv2.createTrackbar("v_up", "hsv_bar", 255, 255, nothing)

cv2.createTrackbar("h_down", "hsv_bar", 0, 255, nothing)
cv2.createTrackbar("s_down", "hsv_bar", 0, 255, nothing)
cv2.createTrackbar("v_down", "hsv_bar", 0, 255, nothing)

while True:
    _, image = cap.read()
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    img_hsv = cv2.GaussianBlur(img_hsv, (5, 5), 2)


    h_up = cv2.getTrackbarPos("h_up", "hsv_bar")
    s_up = cv2.getTrackbarPos("s_up", "hsv_bar")
    v_up = cv2.getTrackbarPos("v_up", "hsv_bar")
    h_down = cv2.getTrackbarPos("h_down", "hsv_bar")
    s_down = cv2.getTrackbarPos("s_down", "hsv_bar")
    v_down = cv2.getTrackbarPos("v_down", "hsv_bar")
    mask = cv2.inRange(img_hsv, numpy.array([h_down, s_down, v_down]), numpy.array([h_up, s_up, v_up]))
    mask2 = cv2.bitwise_and(image,image,mask = mask)
    #mask = cv2.bitwise_and(image,mask)
    cv2.imshow("mask", mask2)
    if cv2.waitKey(1) == 27:
        handle.write(str(h_down)+'\n')
        handle.write(str(s_down)+'\n')
        handle.write(str(v_down)+'\n')
        handle.write(str(h_up)+'\n')
        handle.write(str(s_up)+'\n')
        handle.write(str(v_up)+'\n')
        handle.close()
        print(h_down, s_down, v_down, h_up, s_up, v_up)
        break
