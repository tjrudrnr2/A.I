import numpy as np
import cv2

ix, iy = -1, -1
mode = False
img1, img2 = None, None

def onMouse(event, x, y, flag, param):
    global ix, iy, mode, img1, img2
    if event == cv2.EVENT_LBUTTONDOWN:
        mode=True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if mode:
            img1 = img2.copy()
            cv2.rectangle(img1, (ix, iy), (x, y), (0, 0, 255), 2)
            cv2.imshow('original', img1)
    elif event == cv2.EVENT_LBUTTONUP:
        mode = False
        if ix >= x or iy >= y:
            return
        cv2.rectangle(img1, (ix,iy), (x,y), (0,0,255),2)
        roi = img1[iy:y, ix:x]
        backProjection(img2, roi)
    return

def backProjection(img, roi):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    hsvt = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 히스토그램 계산해주는 함수
    roihist = cv2.calcHist([hsv],[0,1],None,[180,256],[0,180,0,256])
    # 정규화 함수 norm_minmax는 히스토그램 스트레칭 해주는 정규화타입
    cv2.normalize(roihist, roihist, 0, 255, cv2.NORM_MINMAX)
    # 히스토그램 역투영 함수
    # 각 픽셀이 주어진 히스토그램 모델에 얼마나 일치하는지 검사
    dst = cv2.calcBackProject([hsvt], [0,1],roihist,[0,180,0,250],1)
    # 이미지 형태학적 변환 함수
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    # 필터링 적용
    cv2.filter2D(dst, -1, disc, dst)

    # 픽셀값이 문턱값보다 크면 고정된 값으로 할당, 작으면 다른 고정된 값으로 할당
    ret, thr = cv2.threshold(dst, 50, 255, 0)
    thr = cv2.merge((thr, thr, thr))
    res = cv2.bitwise_and(img, thr)

    cv2.imshow('backproj', res)

def main():
    global img1, img2

    img1 = cv2.imread('1.jpg')
    img2 = img1.copy()
    cv2.namedWindow('original'), cv2.namedWindow('backproj')
    cv2.setMouseCallback('original', onMouse, param=None)
    cv2.imshow('backproj', img2)

    while True:
        cv2.imshow('original', img1)

        k = cv2.waitKey(1) & 0xff
        if k==27:
            break
    cv2.destroyAllWindows()
main()