import cv2
import numpy as np
import matplotlib.pylab as plt

cap = cv2.VideoCapture("Resources/raw_video_feed.mp4")
height = 240
width = 320
cap.set(3, width)  # 3 = width
cap.set(4, height)  # 4 = height
cap.set(10, 10)  # 10 = brightness

# need to define region of interest: bottom 100 pixels = 140:240
region_of_interest_vertices = [(0, height), (width, height), (width/2, height/2)]


# mask region outside
def region_of_interest(image, vertices):
    mask = np.zeros_like(image)  # blank matrix to be masked
    # channel_count = image.shape[2]  # find color channel
    match_mask_color = 255  # just passing a gray scale. Only one channel
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def draw_the_lines(image, lines):
    image = np.copy(image)
    blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blank_image, (x1,y1), (x2,y2), (0, 255, 0), thickness=5)

    img = cv2.addWeighted(image, 0.8, blank_image, 1, 0.0)
    return img


# def find_midpoint(img):
#     for point in img[230][:]:
#         total = 0
#         if point > 200:
#             total +=
#
#     return total/2

def find_midpoint(img, height):
    total = 0
    n = 0
    for idx, ele in enumerate(img[height][:]):
        if ele > 200:
            n += 1
            total += idx

    if n <= 1:
        return total
    else:
        return total/n


def find_midpoint_avg(img, height):
    n = 0
    midpt = 0
    while height < img.shape[0]:
        midpt += find_midpoint(img, height)
        height += 1
        n +=1

    return midpt/n


while True:
    success, img = cap.read()
    # print(img.shape)
    # cropped_img = region_of_interest(img,
    #                                  np.array([region_of_interest_vertices], np.int32))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny_img = cv2.Canny(gray_img, 100, 200)
    cropped_img = region_of_interest(canny_img,
                                     np.array([region_of_interest_vertices], np.int32), )
    # lines = cv2.HoughLinesP(cropped_img, rho=6, theta=np.pi/60, threshold=160, lines=np.array([]), minLineLength=40,
    #                         maxLineGap=25)
    lines = cv2.HoughLinesP(cropped_img,
                            lines=np.array([]),
                            rho=6,
                            theta=np.pi/180,
                            threshold=0,
                            minLineLength=0,
                            maxLineGap=1)

    image_w_lines = draw_the_lines(img, lines)
    red = (0,0, 255)
    circle = cv2.circle(image_w_lines, (int(find_midpoint_avg(cropped_img, 230)), 230), radius=20, color=red, thickness=-1)


    cv2.imshow("Video Output", circle)
    if cv2.waitKey(50) & 0xFF == ord('q'):  # adds a delay and looks for the key q to be pressed.
        break
