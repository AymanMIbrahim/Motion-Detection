import cv2
import time
from playsound import playsound
import threading
from multiprocessing import freeze_support

Error = False
Play = True

def ErrorCheck():
	global Error,Play
	while Play:
		if Error:
			playsound("beep-03.mp3")



def Process():
	global Error,Play
	cap = cv2.VideoCapture(0)
	_,BG = cap.read()
	BG = cv2.resize(BG , (1920,1080))
	grayBG = cv2.cvtColor(BG , cv2.COLOR_BGR2GRAY)
	grayBG = cv2.GaussianBlur(grayBG , (21 , 21) , 0)
	ChangeBG = False
	while True:
		Error = False
		ret,frame = cap.read()
		frame = cv2.resize(frame , (1920,1080))
		if ChangeBG:
			_,BG = cap.read()
			BG = cv2.resize(BG , (1920,1080))
			grayBG = cv2.cvtColor(BG , cv2.COLOR_BGR2GRAY)
			grayBG = cv2.GaussianBlur(grayBG , (21 , 21) , 0)
			ChangeBG = False
		if ret:
			W , H , _ = frame.shape
			grayFrame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
			grayFrame = cv2.GaussianBlur(grayFrame , (21 , 21) , 0)


			deltaframe = cv2.absdiff(grayBG , grayFrame)

			thresh = cv2.threshold(deltaframe , 50 , 255 , cv2.THRESH_BINARY)[1]
			thresh = cv2.dilate(thresh , None , iterations=2)

			(cntr , _) = cv2.findContours(thresh.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

			for c in cntr:
				if cv2.contourArea(c) < 20000:
					continue

				else:
					Error = True
					ChangeBG = True
					cv2.putText(frame, "ALERT! MOTION HAS DETECTED", (20, 50),
		                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, [0,0,255], 1)


			cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
			cv2.imshow("Camera" , frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				Play = False
				break
		else:
			break


	# Releasing camera
	cap.release()
	# Destroying all opened OpenCV windows
	cv2.destroyAllWindows()

if __name__ == "__main__":
	freeze_support()
	t1 = threading.Thread(target=ErrorCheck)
	t2 = threading.Thread(target=Process)

	t1.start()
	t2.start()

	t1.join()
	t2.join()
	