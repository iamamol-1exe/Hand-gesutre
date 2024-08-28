import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
fingerCordinators = [(8,6),(12,10),(16,14),(20,18)] # Thumb, Index, Middle, Ring, Pinky
thumbCordinators =(4,2)
cap = cv2.VideoCapture(0)

def new_func(mpHands, mpDraw, img, results):
    if results.multi_hand_landmarks:  # Add a colon at the end of the line
        pass  # Add an indented block to avoid the "Expected indented block" error
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

while True:
    HandPoints = []
    success, img = cap.read()
    if not success:
        break
    #print("Success")
    # Convert the BGR image to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiLandmarks = results.multi_hand_landmarks
    #print(multiLandmarks)
    if multiLandmarks:
        for handLms in multiLandmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for idx, lm in enumerate(handLms.landmark):
               #print(idx, lm)
               h, w, c = img.shape
               cx, cy = int(lm.x *w), int(lm.y * h)
               #print(cx, cy)
               HandPoints.append((cx, cy))

    # Draw red dots on the hand landmarks
        for point in HandPoints:
            cv2.circle(img, point, 5,(0,0,255),  cv2.FILLED)
        upCount = 0
        for coordinates in fingerCordinators:
            if HandPoints[coordinates[0]][1] < HandPoints[coordinates[1]][1]:
                upCount += 1
        if HandPoints[thumbCordinators[0]][0] > HandPoints[thumbCordinators[1]][0]:
            upCount += 1
        cv2.putText(img, str(upCount), (150, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 255), 12)

    # Display the image with hand landmarks
    cv2.imshow("Hand Gesture", img)

    # Exit the loop when 'Esc' key is pressed
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

     
