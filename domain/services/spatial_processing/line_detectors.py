import math
import statistics
from decimal import ROUND_HALF_UP, Decimal
import cv2
import numpy as np
from pylsd import lsd
from image_processor import Image

#TODO: add Line Detect Abstract class and define draw line functions
class HoughTransform(Image):
    def __init__(self, image: Image):
        self._title = self.set_title(image._title)
        self._gray_image = self.detect_lines(image._gray_image.copy())

    def set_title(self, title: str):
        return "Hough " + title.replace("Original ", "")

    def detect_lines(self, gray_image: np.ndarray):
        _lines = cv2.HoughLines(gray_image.astype(np.uint8), 1, np.pi/360, 200)
        detected_image = gray_image.copy()
        if _lines is not None:
            for line in _lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(detected_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
            return detected_image
        else:
            print("Can't draw ht lines")

class PHoughTransform(Image):
    def __init__(self, image: Image, threshold=200, minLineLength=50, maxLineGap=10):
        self._title = self.set_title(image._title)
        self._gray_image = self.detect_lines(image._gray_image.copy(), threshold, minLineLength, maxLineGap)

    def set_title(self, title: str):
        return "PHough " + title.replace("Original ", "")

    def detect_lines(self, gray_image: np.ndarray, threshold, minLineLength, maxLineGap):
        lines = cv2.HoughLinesP(gray_image.astype(np.uint8), 1, np.pi/180, threshold, minLineLength, maxLineGap)
        detected_image = gray_image.copy()
        if lines is not None:
            degs = []
            for line in lines:
                x1,y1,x2,y2 = line[0]
                rad = math.atan2(x2-x1, y2-y1)
                deg = rad*(180/np.pi)
                deg = int(Decimal(deg).quantize(Decimal('1E1'), rounding=ROUND_HALF_UP)) #10の位に丸める
                degs.append(deg)
            mode = statistics.mode(degs)
            for line in lines:
                x1,y1,x2,y2 = line[0]
                rad = math.atan2(x2-x1, y2-y1)
                deg = rad*(180/np.pi)
                deg = int(Decimal(deg).quantize(Decimal('1E1'), rounding=ROUND_HALF_UP))
                cv2.line(detected_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
                if deg <= mode+5 and deg >= mode-5:
                    cv2.line(detected_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
            return detected_image
        else:
            print("Can't draw pht lines")

class LineSegmentDetector(Image):
    def __init__(self, image: Image):
        self._title = self.set_title(image._title)
        self._gray_image = self.detect_lines(image._gray_image.copy())

    def set_title(self, title: str):
        return "LSD " + title.replace("Original ", "")

    def detect_lines(self, gray_image: np.ndarray):
        lines = lsd(gray_image)
        height, width = gray_image.shape[0], gray_image.shape[1]
        detected_image = np.ones([height, width], dtype=np.uint8)
        if lines is not None:
            degs = []
            line_infos = []
            for line in lines:
                x1, y1, x2, y2 = int(line[0]), int(line[1]), int(line[2]), int(line[3])
                rad = math.atan2(x2-x1, y2-y1)
                deg = rad*(180/np.pi)
                deg = int(Decimal(deg).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
                if deg <= 0:
                    deg += 180
                degs.append(deg)
                tmp_list = [x1, y1, x2, y2, deg]
                line_infos.append(tmp_list)

            for line_info in line_infos:
                x1, y1, x2, y2, deg = line_info
                mode = statistics.mode(degs)
                # mode_deg_lines = []
                if deg <= mode+50 and deg >= mode-50:
                    #pass
                    cv2.line(detected_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
                    # mode_deg_line = [x1, y1, x2, y2, deg]
                    # mode_deg_lines.append(mode_deg_line)
            return detected_image
        else:
            print("Can't draw lsd lines")

class FastLineDetector(Image): #ToDo
    def __init__(self):
        super().__init__(title, image)
        self._title = "LSD " + self._title
        self.detect_lines()

    def testFastLineDetector(fileImage):
        colorimg = cv2.imread(fileImage, cv2.IMREAD_COLOR)
        if colorimg is None:
            return -1
        image = cv2.cvtColor(colorimg.copy(), cv2.COLOR_BGR2GRAY)

        # FLDインスタンス生成
        length_threshold = 4 # 10
        distance_threshold = 1.41421356
        canny_th1 = 50.0
        canny_th2 = 50.0
        canny_aperture_size = 3
        do_merge = False

        # 高速ライン検出器生成
        fld = cv2.ximgproc.createFastLineDetector(length_threshold,distance_threshold,
                        canny_th1,canny_th2,canny_aperture_size,do_merge)
        #fld = cv2.createLineSegmentDetector(cv2.LSD_REFINE_STD) # LSD

        # ライン取得
        lines = fld.detect(image)
        #lines, width, prec, nfa = fld.detect(image) # LSD

        # 検出線表示
        drawnLines = np.zeros((image.shape[0],image.shape[1],3), np.uint8)
        fld.drawSegments(drawnLines, lines)
        cv2.imshow("Fast Line Detector(LINE)", drawnLines)

        # 検出線と処理画像の合成表示
        fld.drawSegments(colorimg, lines)
        cv2.imshow("Fast Line Detector", colorimg)
        cv2.waitKey()
        return 0

class DrawEdgeLine(Image):
    def __init__(self, title, image):
        super().__init__(title, image)
        self._title = "DrawEdgeLine" + self._title
        self.draw_lines()

    def draw_lines(self, ):
        w, h = self._image.shape[:2]
        source_color = (0, 0, 0)
        target_color = (255, 255, 255)
        change_color = (255, 0, 0)

        source_list = [(i, j) for j in range(h) for i in range(w) if tuple(self._image[i, j]) == source_color for l in range(j-1, j+2) for k in range(i-1, i+2) if 0 <= k < w and 0 <= l < h if tuple(self._image[k, l]) == target_color]
        for i, j in source_list:
            self._image[i, j] = change_color



if __name__ == '__main__':
    title = "NaCl"
    image = '10033_nacl\\10033_nacl 001.jpg'
