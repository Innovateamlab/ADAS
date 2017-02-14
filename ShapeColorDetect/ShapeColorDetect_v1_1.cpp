#include <ctime>
#include <fstream>
#include <iostream>
#include </usr/local/include/raspicam/raspicam_cv.h>
#include </usr/local/include/raspicam/raspicam.h>
#include </usr/local/include/raspicam/raspicam_still_cv.h>
#include </usr/local/include/raspicam/raspicamtypes.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

//#include <writeArrayInText.cpp>
using namespace std; 
 
int main ( int argc,char **argv ) {
   
    time_t timer_begin,timer_end;
    raspicam::RaspiCam_Cv Camera;
    cv::Mat image;
    int nCount=100;
    //set camera params
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC1 );
    //Open camera
    cout<<"Opening Camera..."<<endl;
    if (!Camera.open()) {cerr<<"Error opening the camera"<<endl;return -1;}
    //Start capture
    cout<<"Capturing "<<nCount<<" frames ...."<<endl;
    time ( &timer_begin );
    for ( int i=0; i<nCount; i++ ) {
        Camera.grab();
        Camera.retrieve ( image);
        if ( i%5==0 )  cout<<"\r captured "<<i<<" images"<<std::flush;
    }
    cout<<"Stop camera..."<<endl;
    Camera.release();
    //show time statistics
    time ( &timer_end ); /* get current time; same as: timer = time(NULL)  */
    double secondsElapsed = difftime ( timer_end,timer_begin );
    cout<< secondsElapsed<<" seconds for "<< nCount<<"  frames : FPS = "<<  ( float ) ( ( float ) ( nCount ) /secondsElapsed ) <<endl;
    
    printf("Appuyez sur n'importe quelle touche pour fermer");
	getchar();
	
    //Convert cv::Mat to char
    int width = image.size().width;
    int height = image.size().height;
    unsigned char *data = (unsigned char*)(image.data) ;/* data is the pointer of the elements of image's pixel data */
	unsigned char array[height * width]; /*array équivalent à data */
	int g; /* gray level */
	
	for (int i=0; i<height; i++)
	{	
		for (int j=0; j<width; j++)
		{ 	
			g = data[width * j + i];
			//array[width * j + i] = g; /* Calcul trés lourd! Le programme "break".
			
		}
	}
	
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
    //save image  
    cv::imwrite("raspicam_cv_image_2.jpg",image);
    cout<<"Image saved at raspicam_cv_image_2.jpg"<<endl;
    
    //System pause
    printf("Appuyez sur n'importe quelle touche pour fermer");
	getchar();
	
	return 0;
}
