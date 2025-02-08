import cv2

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()  # Capture frame
    if not ret:
        break

    cv2.imshow("Mac Camera Feed", frame)

# Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close OpenCV windows
