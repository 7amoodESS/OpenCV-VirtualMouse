import cv2
import numpy as np
import math
import pyautogui as pag

cap = cv2.VideoCapture(0)

# Green - Light
#lower_range = np.array([80, 60, 120])
#upper_range = np.array([100, 255, 220])

# Green - No Light
#lower_range = np.array([80, 60, 120])
#upper_range = np.array([100, 255, 220])

# Green - Mixed
#lower_range = np.array([30, 20, 60])
#upper_range = np.array([120, 255, 220])

#green_boundaries = ([80, 80, 100], [100, 255, 200])

while cap.isOpened():
    _, frame = cap.read()

    # BGR - (blue, green, red)
    lower_range = np.array([30, 20, 60])
    upper_range = np.array([120, 255, 220])

    cv2.rectangle(frame, (100, 100), (400, 400), (0, 0, 255), 2)
    small_frame = frame[100:400, 100:400]

    blur_image = cv2.medianBlur(small_frame, 15)
    blur_image2 = cv2.GaussianBlur(blur_image, (25, 25), 0)

    hsv_image = cv2.cvtColor(blur_image2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_range, upper_range)

    output = cv2.bitwise_and(small_frame, small_frame, mask=mask)

    # cv2.circle(frame, (200, 200), 80, (0, 0, 255), 2)
    _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_list = []

    for contour in contours:
        area = cv2.contourArea(contour)

        if 700 < area < 3000:
            # Add filtered contour to list
            contour_list.append(contour)
            
            (x, y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            cv2.circle(output, center, 5, (0, 0, 255), -1)
            # Draw contour around object
            #cv2.drawContours(output, contour, -1, (0, 0, 255), 1)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output, (x, y), ((x+w), (y+h)), (0, 0, 255), 1)
            cv2.putText(output, "ON", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)

            try:
                (x1, y1), radius1 = cv2.minEnclosingCircle(contour_list[0])
                (x2, y2), radius2 = cv2.minEnclosingCircle(contour_list[1])

                center1 = (int(x1), int(y1))
                center2 = int(x2), int(y2)

                cv2.line(output, center1, center2, (0, 0, 255), 2)
            except IndexError as e:
                pass

            distance = 100
            try:
                # Calculate distance
                # (x2−x1)2+(y2−y1)2
                distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                #print("Distance: ", distance)

                # Click
                if 50 < distance < 70:
                    if not click:
                        pag.click(None, None, 1, 0.0)
                        click = True
                        print("Click")
                else:
                    click = False
            except NameError as e:
                pass

            try:
                # Calculate middle point
                mid_x = int((x1 + x2) / 2)
                mid_y = int((y1 + y2) / 2)

                cv2.circle(output, (mid_x, mid_y), int(distance / 6), (0, 255, 0), 1)
            except NameError as e:
                pass



    cv2.imshow('Live Webcam', frame)
    cv2.imshow('Output', output)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()