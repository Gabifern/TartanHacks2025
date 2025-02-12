import cv2
import numpy as np
import os
import sys
from datetime import datetime

def main():
    """
    main
    """
    print("EoF")
    print("I don't like this in another function lol")
    
def getWhiteboard(image):
    """
    Image is cv2.imread object
    """
    gaussian_kernel = (5, 5)
    # start by getting the whiteboard as a mask


    # # Load image
    # # bg_whiteboard is our buffer image
    # bg_whiteboard = cv2.imread('Background2.jpg')
    # print("image")

    #image = cv2.resize(image, (500,900))

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color range (example: detecting blue)
    lower_bound = np.array([0, 0, 100])  # Lower HSV threshold
    upper_bound = np.array([255, 100, 255]) # Upper HSV threshold

    hsv = cv2.GaussianBlur(hsv, gaussian_kernel, 0)

    # Create mask
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # I DON'T THINK THESE SHOULD BE HERE
    #blurred = cv2.GaussianBlur(mask, gaussian_kernel, 0)

    #Apply morphological operations
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, morphology_kernel)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, morphology_kernel)

    # Assume `mask` is your unfilled binary mask
    filled_mask = mask.copy()

    # Morphological closing to fill gaps
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours of the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Fill the detected contours
    #mask = cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

    # Get bounding box
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largest_contour = contours[0]

        # Get bounding box
        x, y, w, h = cv2.boundingRect(largest_contour)
        whiteboard = image[y:y+h, x:x+w]

        #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #filled_mask = mask.copy()
        #filled_mask = cv2.drawContours(filled_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
        #cv2.rectangle(filled_mask, (x, y), (x + w, y + h), 255, thickness=cv2.FILLED)

        return whiteboard, [x,y,w,h]
    print("no whiteboard, showing frame")
    return image, -1

def getWBForeground(whiteboard, bg_whiteboard):
    """
    Returns objects that stand out from the background image
    """
    # Get dimensions of the regular image
    height, width = whiteboard.shape[:2]

    # Resize the background to match the regular image
    bg_whiteboard = cv2.resize(bg_whiteboard, (width, height))

    # # Ensure the images are of the same size
    if whiteboard.shape != bg_whiteboard.shape:
        print("Images must be the same size!")
        exit()

    #Calculate the absolute difference
    difference = cv2.absdiff(bg_whiteboard, whiteboard)

    difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

    difference = cv2.GaussianBlur(difference, (5, 5), 0)

    # Apply thresholding to highlight differences
    _, thresholded = cv2.threshold(difference, 10, 255, cv2.THRESH_BINARY)  # Adjust the threshold value


    #this is a little high
    # kernel = np.ones((6, 6), np.uint8)
    # thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)
    # thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)  # Remove small noise

    # FINDING AND IGNORING SMALL WIDTH OBJECTS

    # # Find contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Define the minimum width threshold
    min_width = 40  # Adjust as needed

    # Create a copy of the mask to modify
    filtered_mask = thresholded.copy()

    # Iterate over contours
    for contour in contours:
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Check if the width is smaller than the threshold
        if w < min_width or h < min_width:
            # Remove the object by setting its pixels to 0
            cv2.drawContours(filtered_mask, [contour], -1, 0, thickness=cv2.FILLED)
    
    return filtered_mask

def replaceFG(fg_mask, bg_whiteboard, whiteboard):
    # Get dimensions of the regular image
    height, width = whiteboard.shape[:2]

    # Resize the background to match the regular image
    bg_whiteboard = cv2.resize(bg_whiteboard, (width, height))

    region_from_image1 = cv2.bitwise_and(bg_whiteboard, bg_whiteboard, mask=fg_mask)

    # if filtered_mask.shape[:2] != bg_whiteboard.shape[:2]:
    #     filtered_mask = cv2.resize(filtered_mask, (bg_whiteboard.shape[1], bg_whiteboard.shape[0]))

    #_, bmask = cv2.threshold(mask1, 1, 255, cv2.THRESH_BINARY)

    # Invert the mask to black-out the area on image2
    inverted_mask = cv2.bitwise_not(fg_mask)
    image2_background = cv2.bitwise_and(whiteboard, whiteboard, mask=inverted_mask)

    #cv2.imshow("i2bg", image2_background)
    # Combine the region from image1 with the background from image2
    return cv2.add(image2_background, region_from_image1)

def reattachBG(image, whiteboard, area):
    x, y, w, h = area
    whiteboard = cv2.resize(whiteboard, (w, h))

    # Place the cutout back into the original image
    restored_image = image.copy()
    restored_image[y:y+h, x:x+w] = whiteboard

    return restored_image    

if __name__ == "__main__":
    
    bg_whiteboard= None
    save_folder=sys.argv[1] if len(sys.argv)>1 else "unpublished_videos"
    os.makedirs(save_folder, exist_ok=True)
    #timestamp = time.strftime("%Y%m%d_%H%M%S")
    #output_filename = f"recording_{timestamp}.avi"  # Unique file name
    filename=os.path.join(save_folder, f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    cap = cv2.VideoCapture(0)  # Start video capture

    if not cap.isOpened():
        print("Unable to access the camera.")

    # Define the codec and create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec (use 'XVID' for .avi format) #SWITCHED THIS MP4 BY DEFAULT
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))  # Output file name, codec, FPS, frame size

    while True:
        ret, frame = cap.read()  # Capture frame
        if not ret:
            break

        if bg_whiteboard is None:
            bg_whiteboard, bufferArea = getWhiteboard(frame)
            continue

        #BUFFERAREA IS AREA CUTOUT FROM OG IMAGE
        try:
            bufferIm, bufferArea = getWhiteboard(frame)
        except:
            print("No whiteboard")
            continue
        
        if bufferArea == -1:
            continue

        fg_mask = getWBForeground(bufferIm, bg_whiteboard)
        display_wb = replaceFG(fg_mask,bg_whiteboard,bufferIm)
        bg_whiteboard = display_wb
        display_final = reattachBG(frame, bg_whiteboard, bufferArea)

        #last minute test job
        x, y, w, h = bufferArea

        #cv2.rectangle(display_final, (x, y), (x + w, y + h), (0, 255,0), thickness=3)

        out.write(display_final) 

        cv2.imshow("Camera Feed", display_final)

    # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    cap.release()  # Release the camera
    cv2.destroyAllWindows()  # Close OpenCV windows


    #FOR VIDEO LOOP: use latest display image as bg_whiteboard
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    main()