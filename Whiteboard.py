import cv2
import numpy as np

gaussian_kernel = (5, 5)
# start by getting the whiteboard as a mask


# Load image
image = cv2.imread('test_images/IMG_1890.jpg')
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
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    whiteboard = image[y:y+h, x:x+w]
    cv2.imwrite("whiteboard_extracted.jpg", whiteboard)
    cv2.imshow("Extracted Whiteboard", whiteboard)
    
    filled_mask = mask.copy()
    #filled_mask = cv2.drawContours(filled_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    cv2.rectangle(filled_mask, (x, y), (x + w, y + h), 255, thickness=cv2.FILLED)

# Show mask
cv2.imshow('Mask', filled_mask)
cv2.imshow("Bounding box", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
