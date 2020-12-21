import cv2
import imutils
min_area = 500

# if the video argument is None, then we are reading from webcam
#if args.get("video", None) is None:
#    camera = cv2.VideoCapture(0)
#    time.sleep(0.25)
## otherwise, we are reading from a video file
#else:
#    camera = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = cv2.imread('image0.jpeg')
frame = cv2.imread('image1.jpeg')


# resize the frame, convert it to grayscale, and blur it
frame = imutils.resize(frame, width=500)
gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray  = cv2.GaussianBlur(gray, (21, 21), 0)

firstFrame = imutils.resize(firstFrame, width=500)
firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)

# compute the absolute difference between the current frame and
# first frame
frameDelta = cv2.absdiff(firstFrame, gray)
thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

# dilate the thresholded image to fill in holes, then find contours
# on thresholded image
thresh = cv2.dilate(thresh, None, iterations=2)
(__ , cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

# loop over the contours
for c in cnts:
    # if the contour is too small, ignore it
    if cv2.contourArea(c) < min_area :
        continue
    # compute the bounding box for the contour, draw it on the frame,
    # and update the text
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


# draw the text and timestamp on the frame
cv2.putText(frame, "object moving", (10, 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# show the frame and record if the user presses a key
cv2.imwrite("frame.jpeg", frame)
cv2.imwrite("thresh.jpeg", thresh)
cv2.imwrite("frameDelta.jpeg", frameDelta)

