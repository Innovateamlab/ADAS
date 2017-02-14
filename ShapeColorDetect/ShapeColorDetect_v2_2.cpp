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



void MatToTxtFile(cv::Mat image)
{
	
	
	int width = image.size().width;
    int height = image.size().height;
    int g;
    unsigned char array[height * width];
	//save array in text  
    ofstream fichier("array.txt", ios::out | ios::trunc);
    if (fichier)
    {
		//fichier << "[ ";
		for (int i=0; i<height; i++)
		{
			for (int j=0; j<width; j++)
			{ 
				g = array[width * j + i];
				fichier << g << " ";
			}
		} 
		//fichier << " ]";
	}
	fichier.close();
}



unsigned char MatToUChar(cv::Mat image)
{
	//Convert cv::Mat to uchar (0 à 255)
    int width = image.size().width;
    int height = image.size().height;
    unsigned char *data = (unsigned char*)(image.data) ; // data is the pointer of the elements of image's pixel data 
	unsigned char array[height * width]; // array équivalent à data 
	int g; // gray level 
 	
	for (int i=0; i<height; i++)
	{	
		for (int j=0; j<width; j++)
		{ 	
			g = data[width * j + i];
			//array[width * j + i] = g; /* Calcul trés lourd! Le programme "break".
			
		}
	} 
 
	
	return *data;
}


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

cv::Mat shapeDetectorBlue(cv::Mat source, std::vector<std::vector<cv::Point> > contours) 
{
	// Find shape
	cv::Mat img_cropped;
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

	/*	if (approx.size() == 3)
		{
			setLabel(dst, "TRIANGLE", contours[i]);    // Triangles
			cv::Rect r= cv::boundingRect(approx);
			cv::Point pt(r.x, r.y);
			cv::rectangle(dst,pt,pt + cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
			
		} */
		/*else*/ if (approx.size() == 4) //&& approx.size() <= 6)
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
				setLabel(dst, "BLUE RECT", contours[i]);
				cv::Rect r = cv::boundingRect(approx);
				cv::Point pt(r.x, r.y);
				cv::rectangle(dst,pt,pt+cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
				cv::Mat img_cropped = source(r);
				//cv::imshow("red cir", img_cropped);
				//cv::waitKey(30);
				}
			//else if (vtc == 5 && mincos >= -0.34 && maxcos <= -0.27)
				//setLabel(dst, "PENTA", contours[i]);
			//else if (vtc == 6 && mincos >= -0.55 && maxcos <= -0.45)
				//setLabel(dst, "HEXA", contours[i]);
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
				setLabel(dst, "BLUE CIR", contours[i]);
				cv::Rect r = cv::boundingRect(approx);
				cv::Point pt(r.x, r.y);
				cv::rectangle(dst,pt,pt+cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
				cv::Mat img_cropped = source(r);
				//cv::imshow("red cir", img_cropped);
				//cv::waitKey(30);
				
				}
		}
	}
	
	 
	//cv::imshow("Image", source);
	cv::imshow("dst_blue", dst);
	cv::waitKey(30);
	
	return img_cropped;
}

cv::Mat shapeDetectorRed(cv::Mat source, std::vector<std::vector<cv::Point> > contours) 
{
	// Find shape
	cv::Mat img_cropped;
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
			setLabel(dst, "RED TRI", contours[i]);    // Triangles
			cv::Rect r= cv::boundingRect(approx);
			cv::Point pt(r.x, r.y);
			cv::rectangle(dst,pt,pt + cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
			cv::Mat img_cropped = source(r);
			//cv::imshow("red cir", img_cropped);
			//cv::waitKey(30);
			
		}
		/*else if (approx.size() == 4) //&& approx.size() <= 6)
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
				setLabel(dst, "RECTANGLE", contours[i]);
				cv::Rect r = cv::boundingRect(approx);
				cv::Point pt(r.x, r.y);
				cv::rectangle(dst,pt,pt+cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
				}
			//else if (vtc == 5 && mincos >= -0.34 && maxcos <= -0.27)
				//setLabel(dst, "PENTA", contours[i]);
			//else if (vtc == 6 && mincos >= -0.55 && maxcos <= -0.45)
				//setLabel(dst, "HEXA", contours[i]);
		} */
		else
		{
			// Detect and label circles
			double area = cv::contourArea(contours[i]);
			cv::Rect r = cv::boundingRect(contours[i]);
			int radius = r.width / 2;

			if (std::abs(1 - ((double)r.width / r.height)) <= 0.2 &&
			    std::abs(1 - (area / (CV_PI * std::pow(radius, 2)))) <= 0.2)
				{
				setLabel(dst, "RED CIR", contours[i]);
				cv::Rect r = cv::boundingRect(approx);
				cv::Point pt(r.x, r.y);
				cv::rectangle(dst,pt,pt+cv::Point(r.width,r.height),CV_RGB(255,0,255),thickness);
				cv::Mat img_cropped = source(r);
				//cv::imshow("red cir", img_cropped);
				//cv::waitKey(30);
				}
		}
	}
	//cv::imshow("Image", source);
	cv::imshow("dst_red", dst);
	cv::waitKey(30);
	
	return img_cropped;
}

cv::Mat preprocessing(cv::Mat image_RGB)
{
	// Image preprocessing
	//Median blur
	cv::Mat blur;
	medianBlur(image_RGB,blur,5);	 
	//cv::imwrite("raspicam_cv_image_blur.jpg",blur);
    //cout<<"Image saved at raspicam_cv_image_blur.jpg"<<endl;
    
    // Convert into HSV
    cv::Mat hsv;
    cvtColor(blur, hsv, CV_RGB2HSV);
    //cv::imwrite("raspicam_cv_image_hsv.jpg",blur);
    //cout<<"Image saved at raspicam_cv_image_hsv.jpg"<<endl;
     //getchar();
     
     return hsv;
}

cv::Mat SetBlueMask(cv::Mat hsv)
{
cv::Mat blueMask, blueMask1, blueMask2;
uchar blueLower1_data[3] = {0,50,50};
uchar blueUpper1_data[3] = {10,255,255};
uchar blueLower2_data[3] = {160,50,50};
uchar blueUpper2_data[3] = {180,255,255};
cv::Mat blueLower1 = cv::Mat(1,3,CV_8UC1, blueLower1_data);
cv::Mat blueUpper1 = cv::Mat(1,3,CV_8UC1, blueUpper1_data);
cv::Mat blueLower2 = cv::Mat(1,3,CV_8UC1, blueLower2_data);
cv::Mat blueUpper2 = cv::Mat(1,3,CV_8UC1, blueUpper2_data);	

inRange(hsv, blueLower1, blueUpper1, blueMask1);
inRange(hsv, blueLower2, blueUpper2, blueMask2);
blueMask = blueMask1+blueMask2;

return blueMask;
	
}

cv::Mat SetRedMask(cv::Mat hsv)
{
cv::Mat redMask;
uchar redLower_data[3]= {75,50,50};
uchar redUpper_data[3] = {130,255,255};	
cv::Mat redLower = cv::Mat(1,3,CV_8UC1, redLower_data);
cv::Mat redUpper = cv::Mat(1,3,CV_8UC1,redUpper_data);	
	
inRange(hsv, redLower, redUpper, redMask);

return redMask;
}

 
int main ( int argc,char **argv ) {
   
    time_t timer_begin,timer_end;
    raspicam::RaspiCam_Cv Camera;
    cv::Mat image;
    int nCount=100;
    
    //set camera params
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC3 ); // CV_8UC3 = frame RGB; CV_8UC1 = frame gray;
    Camera.set( CV_CAP_PROP_FRAME_WIDTH, 640 );
    Camera.set( CV_CAP_PROP_FRAME_HEIGHT, 480 );
    //Camera.set(CV_CAP_PROP_FPS, 90);
    
    //Open camera
    if (!Camera.open()) {cerr<<"Error opening the camera"<<endl;return -1;} // Open the PiCam device
    cout<<"Opening Camera..."<<endl;
    
    time ( &timer_begin ); // Lance le chrono
    
    cout<<"Capturing "<<nCount<<" frames ...."<<endl;
    
    for ( int i=0; i<nCount; i++ ) 
    {	
		//Start capture
        Camera.grab();
        //cout<< "\n Grab " << i << " done" << endl;
        
        Camera.retrieve (image);
        //cout<< "\n frame to image " << i << " done" << endl;
        //cv::imshow("frame", image);
        //cv::waitKey(30);
        if ( i%5==0 )  cout<<"\r captured "<<i<<" images"<<std::flush;
    
	
// Image preprocessing : get the preprocessed image (in hsv)
	cv::Mat hsv = preprocessing(image);
    
//Défine range of red and blue color in HSV
    cv::Mat blueMask = SetBlueMask(hsv);
    cv::Mat redMask = SetRedMask(hsv);
    
   // cv::imshow("redmask", redMask);
   // cv::imshow("bluemask", blueMask);
   // cv::waitKey(0);
    
// find contours in the thresholded image and initialize the shape detector
    
    std::vector<std::vector<cv::Point> > contoursB;
    findContours(blueMask.clone(), contoursB, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
    
    std::vector<std::vector<cv::Point> > contoursR;
    findContours(redMask.clone(), contoursR, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
    
// find shape
	cv::Mat imgCropB = shapeDetectorBlue(image, contoursB);
	cv::Mat imgCropR = shapeDetectorRed(image, contoursR);
	
	
/*    //save image  
    cv::imwrite("raspicam_cv_image.jpg",image);
    cout<<"Image saved at raspicam_cv_image.jpg"<<endl;
*/ 

	
}
//show time statistics
	time ( &timer_end ); // Arrete le chrono
	double secondsElapsed = difftime ( timer_end,timer_begin );
    cout<< "\n" << secondsElapsed  <<" seconds for "<< nCount<<"  frames : FPS = "<<  ( float ) (nCount/secondsElapsed) << endl;
    cout<< "\n Appuyez sur 'Entrée' pour terminer" <<endl;
    getchar();

	Camera.release(); // Close the PiCam device
	cout<< "\n Release done" << endl;

	return 0;
}
