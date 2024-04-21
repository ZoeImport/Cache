#include "opencv2/imgcodecs.hpp"
#include <algorithm>
#include <iostream>
#include <iterator>
#include <opencv2/core.hpp>
#include <opencv2/core/hal/interface.h>
#include <opencv2/core/mat.hpp>
#include <opencv2/core/matx.hpp>
#include <opencv2/core/types.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

void singlePic() {
  string path = "./pictures/girl.jpg";
  Mat img = imread(path);
  imshow("title", img);
  waitKey(0);
}

void pics2Vid() {
  string path = "./pictures/pubu.mp4";
  VideoCapture cap(path);
  Mat img;
  while (1) {
    cap.read(img);
    imshow("title", img);
    waitKey(1);
  }
}

void camera2Vid() {
  VideoCapture cap(0);
  Mat img;
  while (1) {
    cap.read(img);
    imshow("title", img);
    waitKey(1);
  }
}

void singlePicButcolor() {
  string path = "./pictures/girl.jpg";
  Mat img = imread(path);
  Mat colorImg;
  cvtColor(img, colorImg, COLOR_BGR2GRAY);
  imshow("source", img);
  imshow("gray", colorImg);
  waitKey(0);
}

void singlePicButGasBlur() {
  string path = "./pictures/girl.jpg";
  Mat img = imread(path);
  Mat blurimg;
  // cvtColor(img, colorImg, COLOR_BGR2GRAY);
  GaussianBlur(img, blurimg, Size(111, 9), 5, 0);
  // imshow("source", img);
  imshow("blur", blurimg);
  waitKey(0);
}

void singlePicButCanny() {
  string path = "./pictures/girl.jpg";
  Mat img = imread(path);
  Mat imgCanny;
  // GaussianBlur(img,blurimg,Size(111,9),5,0);
  Canny(img, imgCanny, 50, 150);

  imshow("blur", imgCanny);
  waitKey(0);
}

void singlePicButDilate() {
  string path = "./pictures/girl.jpg";
  Mat img = imread(path);
  Mat imgCanny, imgdilate;

  Canny(img, imgCanny, 50, 150);

  Mat kernelDilate = getStructuringElement(MORPH_RECT, Size(5, 5));
  dilate(imgCanny, imgdilate, kernelDilate);
  imshow("dilate", imgdilate);
  waitKey(0);
}
void singlePicButErode() {
  string path = "./pictures/girl.jpg";
  Mat img = imread(path);
  Mat imgCanny, imgdilate, imgerode;

  Mat kernelDilate = getStructuringElement(MORPH_RECT, Size(9, 9));
  Canny(img, imgCanny, 50, 150);
  dilate(imgCanny, imgdilate, kernelDilate);
  erode(imgdilate, imgerode, kernelDilate);

  imshow("imgerode", imgerode);
  waitKey(0);
}

void singlePicResize() {
  string path = "./pictures/girl.jpg";
  Mat img = imread(path);
  Mat imgResize;
  cout << img.size << endl; // 1232 x 928
  // resize(img, imgResize, Size(600, 600));
  resize(img, imgResize, Size(), 0.5, 0.5);
  imshow("imgResize", imgResize);
  waitKey(0);
}

void singlePicCrop() {
  string path = "./pictures/girl.jpg";
  Mat img = imread(path);
  Mat imgCrop;
  Rect rec(300, 300, 200, 200);
  imgCrop = img(rec);

  imshow("imgResize", imgCrop);
  waitKey(0);
}

void drawImg() {
  Mat img(512, 512, CV_8UC3, Scalar(255, 255, 255));

  circle(img, Point(256, 256), 100, Scalar(100, 192, 80), 20);
  // circle(img, Point(256, 256), 100, Scalar(100, 192, 80),FILLED);

  Rect rec(20, 492, 472, 10);
  rectangle(img, rec, Scalar(100, 100, 30), FILLED);

  line(img, Point(20, 20), Point(492, 20), Scalar(255, 255, 100), 3);

  putText(img, "hello opencv", Point(128, 128), FONT_HERSHEY_SCRIPT_SIMPLEX,
          2.2, Scalar(100, 192, 80), 2);

  imshow("img", img);
  waitKey(0);
}

void singleWrapImage() {
  string path = "./pictures/Paidaxin.jpg";

  Mat img = imread(path);
  Mat imgResize, transMat, imgWrap;
  // cout << img.size << endl;//3468 x 4624
  Point p(400, 400);
  resize(img, imgResize, Size(1200, 1387));
  Point2f src[4]{{415, 335}, {820, 342}, {380, 965}, {865, 960}};
  Point2f dst[4]{{0.0f, 0.0f}, {400, 0.0f}, {0.0f, 400}, {400, 400}};
  transMat = getPerspectiveTransform(src, dst);
  warpPerspective(imgResize, imgWrap, transMat, p);
  for (auto index = 0; index < 4; ++index) {
    circle(imgResize, src[index], 5, Scalar(0, 0, 255), FILLED);
  }
  imshow("img", imgResize);
  imshow("wrapimg", imgWrap);
  waitKey(0);
}

void singlePic2HSV() {
  Mat imgHSV, mask, imgresize;
  string path = "./pictures/005.png";
  Mat img = imread(path);
  resize(img, imgresize, Size(), 0.5, 0.5);
  cvtColor(img, imgHSV, COLOR_BGR2HSV);
  int hmin = 0, smin = 110, vmin = 153;
  int hmax = 20, smax = 240, vmax = 255;
  Scalar lower(hmin, smin, vmin);
  Scalar upper(hmax, smax, vmax);
  inRange(imgHSV, lower, upper, mask);

  imshow("img", imgresize);
  imshow("mask", mask);
  imshow("imgHSV", imgHSV);
  waitKey(0);
}

void singlePic2HSVBytarckBar() {
  int hmin = 0, smin = 110, vmin = 153;
  int hmax = 20, smax = 240, vmax = 255;
  Mat imgHSV, mask, imgresize;
  string path = "./pictures/005.png";
  Mat img = imread(path);
  resize(img, imgresize, Size(), 0.5, 0.5);

  cvtColor(imgresize, imgHSV, COLOR_BGR2HSV);

  namedWindow("tarckBars", (640, 200));
  createTrackbar("hmin bar", "tarckBars", &hmin, 180);
  createTrackbar("smin bar", "tarckBars", &smin, 180);
  createTrackbar("vmin bar", "tarckBars", &vmin, 255);
  createTrackbar("hmax bar", "tarckBars", &hmax, 255);
  createTrackbar("smax bar", "tarckBars", &smax, 255);
  createTrackbar("vmax bar", "tarckBars", &vmax, 255);
  while (1) {

    Scalar lower(hmin, smin, vmin);
    Scalar upper(hmax, smax, vmax);
    inRange(imgHSV, lower, upper, mask);

    // imshow("img", imgresize);
    imshow("mask", mask);
    // imshow("imgHSV", imgHSV);
    waitKey(1);
  }
}

void shapeDetect() {
  Mat img(512, 512, CV_8UC3, Scalar(255, 255, 255));

  circle(img, Point(100, 100), 100, Scalar(100, 192, 80), FILLED);
  circle(img, Point(50, 250), 10, Scalar(100, 192, 80), 3);
  rectangle(img, Point(100, 400), Point(500, 500), Scalar(255, 0, 0), FILLED);
  vector<Point> vertices = {cv::Point(100, 300), cv::Point(300, 100),
                            cv::Point(500, 300)};
  polylines(img, vertices, true, Scalar(255, 255, 0), 3);

  Mat imgGray, imgBlur, imgCanny, imgDilate;
  Mat *imgs[5] = {&img, &imgGray, &imgBlur, &imgCanny, &imgDilate};
  cvtColor(img, imgGray, COLOR_BGR2GRAY);
  GaussianBlur(imgGray, imgBlur, Size(3, 3), 3, 0);
  Canny(imgBlur, imgCanny, 25, 75);
  Mat kernel = getStructuringElement(MORPH_RECT, Size(3, 3));
  dilate(imgCanny, imgDilate, kernel);

  vector<vector<Point>> contours;
  vector<Vec4i> hierarchy;

  findContours(imgDilate, contours, hierarchy, RETR_EXTERNAL,
               CHAIN_APPROX_SIMPLE);

  vector<vector<Point>> conpoly(contours.size());
  vector<Rect> boundRect(contours.size());
  string objectType;

  for (auto index = 0; index < contours.size(); ++index) {
    auto area = contourArea(contours[index]);
    if (area > 1000) {
      auto peri = arcLength(contours[index], true);
      approxPolyDP(contours[index], conpoly[index], 0.02 * peri, true);
      boundRect[index] = boundingRect(conpoly[index]);

      switch (int objCor = conpoly[index].size()) {
      case 3:
        objectType = "Tri";
        break;
      case 4: {
        auto aspRatio =
            (float)boundRect[index].width / boundRect[index].height;
        if ((aspRatio > 0.95) || (aspRatio < 1.05)) {
          objectType = "Square";
          break;
        }
        objectType = "Rect";
        break;
      }
      default:
        objectType = "Cir";
        break;
      }
      auto mid_x = (boundRect[index].br().x + boundRect[index].tl().x) / 2;
      auto mid_y = (boundRect[index].br().y + boundRect[index].tl().y) / 2;
      rectangle(img, boundRect[index].tl(), boundRect[index].br(),
                Scalar(255, 0, 100), 10);
      putText(img, objectType, Point(mid_x, mid_y), FONT_HERSHEY_DUPLEX, 1,
              Scalar(0, 255, 0), 2);
      // drawContours(img, contours, index, Scalar(255, 0, 255),20);
      drawContours(img, conpoly, index, Scalar(255, 200, 0), 1);
    }
  }

  imshow("img", img);
  waitKey(0);
  // for (auto index = 0; index < 5; ++index) {
  //   imshow("img", (*imgs[index]));
  //   waitKey(2000);
  // }
}

int main() {
  // singlePic();
  // pics2Vid();
  // singlePicButcolor();
  // singlePicButGasBlur();
  // singlePicButCanny();
  // singlePicResize();
  // singleWrapImage();
  shapeDetect();
  // singlePic2HSVBytarckBar();
}