import cv2
import numpy as np

"""

PART ONE: Getting whiteboard mask
(Imagine defining methods)
"""

gaussian_kernel = (5, 5)
# start by getting the whiteboard as a mask


# Load image
image = cv2.imread('../hand.jpg')
# bg_whiteboard is our buffer image
bg_whiteboard = cv2.imread('Background2.jpg')
print("image")

image = cv2.resize(image, (500,900))

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define color range (example: detecting blue)
lower_bound = np.array([0, 0, 175])  # Lower HSV threshold
upper_bound = np.array([255, 30, 255]) # Upper HSV threshold

# Create mask
mask = cv2.inRange(hsv, lower_bound, upper_bound)

#blurred = cv2.GaussianBlur(mask, gaussian_kernel, 0)

# Apply morphological operations
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

    filled_mask = mask.copy()
    #filled_mask = cv2.drawContours(filled_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    cv2.rectangle(filled_mask, (x, y), (x + w, y + h), 255, thickness=cv2.FILLED)

cv2.imshow("Extracted Whiteboard", whiteboard)
#cv2.imwrite("Background2.jpg", whiteboard)

"""

PART TWO: SEGMENTING OBJECTS ON THE IMAGE

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

blurred_mask = cv2.GaussianBlur(difference, (5, 5), 0)

# Apply thresholding to highlight differences
_, thresholded = cv2.threshold(blurred_mask, 50, 255, cv2.THRESH_BINARY)  # Adjust the threshold value


#this is a little high
kernel = np.ones((6, 6), np.uint8)
thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_CLOSE, kernel)
thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)  # Remove small noise

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



#Display the results
cv2.imshow("Difference", difference)
cv2.imshow("Thresholded Difference", filtered_mask)

"""

PART 3: Overlaying buffer

"""
# Ensure the images and mask have the same size
# if image1.shape[:2] != image2.shape[:2] or image1.shape[:2] != mask.shape[:2]:
#     print("All inputs must have the same dimensions!")
#     exit()

# Extract the region from image1 using the mask
region_from_image1 = cv2.bitwise_and(bg_whiteboard, bg_whiteboard, mask=filtered_mask)

if filtered_mask.shape[:2] != bg_whiteboard.shape[:2]:
    filtered_mask = cv2.resize(filtered_mask, (bg_whiteboard.shape[1], bg_whiteboard.shape[0]))

_, filtered_mask = cv2.threshold(filtered_mask, 1, 255, cv2.THRESH_BINARY)

# Invert the mask to black-out the area on image2
inverted_mask = cv2.bitwise_not(filtered_mask)
image2_background = cv2.bitwise_and(image, image, mask=inverted_mask)

# Combine the region from image1 with the background from image2
result = cv2.add(image2_background, region_from_image1)

#cv2.imshow("Result", result)

# CHRISTIAN EDGE DETECTION
#edges = cv2.Canny(whiteboard,100,200)
# Show mask
#cv2.imwrite("Background.jpg",whiteboard)
#cv2.imshow("Edges", edges)
#cv2.imshow('Mask', filled_mask)
#cv2.imshow("Bounding box", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
