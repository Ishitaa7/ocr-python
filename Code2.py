# Import the necessary packages
import cv2
import os
import argparse
import pytesseract
from PIL import Image

# Construct an Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image file")
ap.add_argument("-p", "--pre_processor", default="thresh", help="The preprocessor to use (thresh or blur)")
args = vars(ap.parse_args())

# Read the image with text
images = cv2.imread(args["image"])

# Convert to grayscale image
gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)

# Apply the preprocessor
if args["pre_processor"] == "thresh":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
elif args["pre_processor"] == "blur":
    gray = cv2.medianBlur(gray, 3)

# Memory usage with image i.e. adding image to memory
filename = "{}.jpg".format(os.getpid())
cv2.imwrite(filename, gray)
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)

# Check if any text is detected
if text:
    print("Detected Text:", text)
else:
    print("No text detected.")

# Show the output images
cv2.imshow("Image Input", images)
# cv2.imshow("Output In Grayscale", gray)
cv2.waitKey(0)
