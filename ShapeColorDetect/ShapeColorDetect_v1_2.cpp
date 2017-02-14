#include <ctime>
#include <cmath>
#include <fstream>
#include <iostream>
#include </usr/local/include/raspicam/raspicam_cv.h>
#include </usr/local/include/raspicam/raspicam.h>
#include </usr/local/include/raspicam/raspicam_still_cv.h>
#include </usr/local/include/raspicam/raspicamtypes.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include </usr/local/include/opencv2/opencv.hpp>

// Les fonctions à créer
//#include <writeArrayInText.cpp>
//#include <MatToUchar.cpp>
using namespace std; 
using namespace cv;



static double angle(cv::Point pt1, cv::Point pt2, cv::Point pt0)
{
	double dx1 = pt1.x - pt0.x;
	double dy1 = pt1.y - pt0.y;
	double dx2 = pt2.x - pt0.x;
	double dy2 = pt2.y - pt0.y;
	return (dx1*dx2 + dy1*dy2)/sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) + 1e-10);
}


void setLabel(cv::Mat& im, const std::string label, std::vector<cv::Point>& contour)
{
	int fontface = cv::FONT_HERSHEY_SIMPLEX;
	double scale = 0.4;
	int thickness = 1;
	int baseline = 0;

	cv::Size text = cv::getTextSize(label, fontface, scale, thickness, &baseline);
	cv::Rect r = cv::boundingRect(contour);

	cv::Point pt(r.x + ((r.width - text.width) / 2), r.y + ((r.height + text.height) / 2));
	cv::rectangle(im, pt + cv::Point(0, baseline), pt + cv::Point(text.width, -text.height), CV_RGB(255,255,255), CV_FILLED);
	cv::putText(im, label, pt, fontface, scale, CV_RGB(0,0,0), thickness, 8);
}

void shapeDetector(cv::Mat source, std::vector<std::vector<cv::Point> > contours) 
{
	// Find shape
	
	std::vector<cv::Point> approx;
	cv::Mat dst = source.clone();
	int thickness = 2;
	
	for (int i = 0; i < contours.size(); i++)
	{
		// Approximate contour with accuracy proportional
		// to the contour perimeter
		cv::approxPolyDP(cv::Mat(contours[i]), approx, cv::arcLength(cv::Mat(contours[i]), true)*0.02, true);

		// Skip small or non-convex objects 
		if (std::fabs(cv::contourArea(contours[i])) < 200 || !cv::isContourConvex(approx))
			continue;

		if (approx.size() == 3)
		{
			setLabel(dst, "TRI", contours[i]);    // Triangles
			cv::Rect r= cv::boundingRect(approx);
			cv::Point pt(r.x, r.y);
			cv::rectangle(dst,pt,pt + cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
			
		}
		else if (approx.size() >= 4 && approx.size() <= 6)
		{
			// Number of vertices of polygonal curve
			int vtc = approx.size();

			// Get the cosines of all corners
			std::vector<double> cos;
			for (int j = 2; j < vtc+1; j++)
				cos.push_back(angle(approx[j%vtc], approx[j-2], approx[j-1]));

			// Sort ascending the cosine values
			std::sort(cos.begin(), cos.end());

			// Get the lowest and the highest cosine
			double mincos = cos.front();
			double maxcos = cos.back();

			// Use the degrees obtained above and the number of vertices
			// to determine the shape of the contour
			if (vtc == 4 && mincos >= -0.1 && maxcos <= 0.3)
				{
				setLabel(dst, "RECT", contours[i]);
				cv::Rect r = cv::boundingRect(approx);
				cv::Point pt(r.x, r.y);
				cv::rectangle(dst,pt,pt+cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
				}
			else if (vtc == 5 && mincos >= -0.34 && maxcos <= -0.27)
				setLabel(dst, "PENTA", contours[i]);
			else if (vtc == 6 && mincos >= -0.55 && maxcos <= -0.45)
				setLabel(dst, "HEXA", contours[i]);
		}
		else
		{
			// Detect and label circles
			double area = cv::contourArea(contours[i]);
			cv::Rect r = cv::boundingRect(contours[i]);
			int radius = r.width / 2;

			if (std::abs(1 - ((double)r.width / r.height)) <= 0.2 &&
			    std::abs(1 - (area / (CV_PI * std::pow(radius, 2)))) <= 0.2)
				{
				setLabel(dst, "CIR", contours[i]);
				cv::Rect r = cv::boundingRect(approx);
				cv::Point pt(r.x, r.y);
				cv::rectangle(dst,pt,pt+cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
				}
		}
	}

	//cv::imshow("Image", source);
	cv::imshow("dst", dst);
	cv::waitKey(0);
}

 
int main ( int argc,char **argv ) {
   
    time_t timer_begin,timer_end;
    raspicam::RaspiCam_Cv Camera;
    cv::Mat image;
    int nCount=100;
    //set camera params
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC3 ); // CV_8UC3 = frame RGB; CV_8UC1 = frame gray;
   // Camera.set( CV_CAP_PROP_FRAME_WIDTH, 640 );
   // Camera.set( CV_CAP_PROP_FRAME_HEIGHT, 480 );
    //Open camera
    cout<<"Opening Camera..."<<endl;
    if (!Camera.open()) {cerr<<"Error opening the camera"<<endl;return -1;}
    //Start capture
    cout<<"Capturing "<<nCount<<" frames ...."<<endl;
    time ( &timer_begin ); /* Lance le chrono */
    for ( int i=0; i<nCount; i++ ) 
    {
        Camera.grab();
        
        Camera.retrieve (image);
        cv::imshow("frame", image);
        if ( i%5==0 )  cout<<"\r captured "<<i<<" images"<<std::flush;
    }
    cout<<"Stop camera..."<<endl;
    Camera.release();
    //show time statistics
    time ( &timer_end ); /* get current time; same as: timer = time(NULL)  */ /* Arrete le chrono */
    double secondsElapsed = difftime ( timer_end,timer_begin );
    cout<< secondsElapsed<<" seconds for "<< nCount<<"  frames : FPS = "<<  ( float ) ( ( float ) ( nCount ) /secondsElapsed ) <<endl;
    
    printf("Appuyez sur n'importe quelle touche pour fermer");
	getchar();
	
// Image preprocessing
	//Median blur
	cv::Mat blur;
	medianBlur(image,blur,5);	 
	//cv::imwrite("raspicam_cv_image_blur.jpg",blur);
    //cout<<"Image saved at raspicam_cv_image_blur.jpg"<<endl;
    
    // Convert into HSV
    cv::Mat hsv;
    cvtColor(blur, hsv, CV_RGB2HSV);
    //cv::imwrite("raspicam_cv_image_hsv.jpg",blur);
    //cout<<"Image saved at raspicam_cv_image_hsv.jpg"<<endl;
     //getchar();
    
    //Défine range of red and blue color in HSV
    cv::Mat blueMask, blueMask1, blueMask2, redMask;
   /* uchar blueLower_data[3]= {75,50,50};
    uchar blueUpper_data[3] = {130,255,255};
    uchar redLower1_data[3] = {0,50,50};
    uchar redUpper1_data[3] = {10,255,255};
    uchar redLower2_data[3] = {160,50,50};
    uchar redUpper2_data[3] = {180,255,255}; */
    uchar redLower_data[3]= {75,50,50};
    uchar redUpper_data[3] = {130,255,255};
    uchar blueLower1_data[3] = {0,50,50};
    uchar blueUpper1_data[3] = {10,255,255};
    uchar blueLower2_data[3] = {160,50,50};
    uchar blueUpper2_data[3] = {180,255,255};
    cv::Mat redLower = cv::Mat(1,3,CV_8UC1, redLower_data);
    cv::Mat redUpper = cv::Mat(1,3,CV_8UC1,redUpper_data);
    cv::Mat blueLower1 = cv::Mat(1,3,CV_8UC1, blueLower1_data);
    cv::Mat blueUpper1 = cv::Mat(1,3,CV_8UC1, blueUpper1_data);
    cv::Mat blueLower2 = cv::Mat(1,3,CV_8UC1, blueLower2_data);
    cv::Mat blueUpper2 = cv::Mat(1,3,CV_8UC1, blueUpper2_data);
    
    inRange(hsv, redLower, redUpper, redMask);
    inRange(hsv, blueLower1, blueUpper1, blueMask1);
    inRange(hsv, blueLower2, blueUpper2, blueMask2);
    blueMask = blueMask1+blueMask2;
    
   // cv::imshow("redmask", redMask);
   // cv::imshow("bluemask1", blueMask1);
   // cv::imshow("bluemask2", blueMask2);
   // cv::waitKey(0);
    
    // find contours in the thresholded image and initialize the shape detector
    
    std::vector<std::vector<cv::Point> > contours1;
    findContours(blueMask.clone(), contours1, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
    
    std::vector<std::vector<cv::Point> > contours2;
    findContours(redMask.clone(), contours2, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
    
	// find shape
	shapeDetector(image, contours1);
	shapeDetector(image, contours2);
	
	
    /*unsigned char *c1 = (unsigned char*)(cnts1.data);
    
    for (int i=0; i<cnts1.size(); i++)
    {
		c = cnts1(i);
		cout<< "conts1 : "<< c <<endl;
		}
    getchar(); */
    
	//cnts1 = cnts1[0] if imutils.is_cv2() else cnts1[1]
	
	//findContours(redMask,cnts2 ,CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
	//cnts2 = cnts2[0] if imutils.is_cv2() else cnts2[1]
    
    
	
  //Convert cv::Mat to uchar (0 à 255)
/*  int width = image.size().width;
    int height = image.size().height;
    unsigned char *data = (unsigned char*)(image.data) ; // data is the pointer of the elements of image's pixel data 
	unsigned char array[height * width]; // array équivalent à data 
	int g; // gray level 
*/ 	
/*	for (int i=0; i<height; i++)
	{	
		for (int j=0; j<width; j++)
		{ 	
			g = data[width * j + i];
			//array[width * j + i] = g; /* Calcul trés lourd! Le programme "break".
			
		}
	} 
*/ 
	
/*	
    //save array in text  
    ofstream fichier("array.txt", ios::out | ios::trunc);
    if (fichier)
    {
		//fichier << "[ ";
		for (int i=0; i<height; i++)
		{
			for (int j=0; j<width; j++)
			{ 
				g = data[width * j + i];
				fichier << g << " ";
			}
		} 
		//fichier << " ]";
	}
	fichier.close();
*/
/*    //save image  
    cv::imwrite("raspicam_cv_image.jpg",image);
    cout<<"Image saved at raspicam_cv_image.jpg"<<endl;
    
    //System pause
    printf("Appuyez sur n'importe quelle touche pour fermer");
	getchar(); */
	
	return 0;
}
