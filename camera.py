import cv2
from datetime import datetime 
import sys 
import os 

def start_camera():
    save_folder=sys.argv[1] if len(sys.argv)>1 else "unpublished videos"
    os.makedirs(save_folder, exist_ok=True)
    #timestamp = time.strftime("%Y%m%d_%H%M%S")
    #output_filename = f"recording_{timestamp}.avi"  # Unique file name
    filename=os.path.join(save_folder, f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    cap = cv2.VideoCapture(0)  # Start video capture

    if not cap.isOpened():
        print("Unable to access the camera.")
        return

    # Define the codec and create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec (use 'XVID' for .avi format)
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))  # Output file name, codec, FPS, frame size

    count = 0
    while True:
        ret, frame = cap.read()  # Capture frame
        if not ret:
            break

        text = str(count)
        org = (50, 100) # Position of the text (bottom-left corner)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255) # White color (BGR format)
        thickness = 2

        count +=1
        # Draw the text on the image
        cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)


        out.write(frame)  # Write the frame to the video file

        # Display the frame in a window
        cv2.imshow("Mac Camera Feed", frame)

        # Check for 'q' key press to stop the recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the camera
    out.release()  # Release the VideoWriter object
    cv2.destroyAllWindows()  # Close OpenCV windows
    print("Recording saved as 'recording.avi'.")

if __name__ == "__main__":
    start_camera()
