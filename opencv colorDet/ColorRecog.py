
import numpy as np
import cv2
# web cam'den görüntü alır
webcam = cv2.VideoCapture(0)

while(1):
	
    #videoyu webcam'den görüntü şeklinde okuma
    
		ret, imageFrame = webcam.read()
		imageFrame = cv2.flip(imageFrame,1)
		
		# görüntüyü BGR'dan HSV'ye dönüştürme
		
		hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
	
		# kırmızı renk için aralık belirleme ve maskeleme işlemi
		red_lower = np.array([136, 87, 111], np.uint8)
		red_upper = np.array([180, 255, 255], np.uint8)
		red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)


		# yeşil renk için aralık belirleme ve maskeleme işlemi
		green_lower = np.array([25, 52, 72], np.uint8)
		green_upper = np.array([102, 255, 255], np.uint8)
		green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)


		# mavi renk için aralık belirleme ve maskeleme işlemi
		blue_lower = np.array([94, 80, 2], np.uint8)
		blue_upper = np.array([120, 255, 255], np.uint8)
		blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
		
		# Morfolojik işlem
		kernal = np.ones((5, 5), "uint8")
		
		# Kırmızı renk için
		red_mask = cv2.dilate(red_mask, kernal)
		res_red = cv2.bitwise_and(imageFrame, imageFrame,
								mask = red_mask)
		
		# yeşil renk için
		green_mask = cv2.dilate(green_mask, kernal)
		res_green = cv2.bitwise_and(imageFrame, imageFrame,
									mask = green_mask)
		
		# mavi renk için
		blue_mask = cv2.dilate(blue_mask, kernal)
		res_blue = cv2.bitwise_and(imageFrame, imageFrame,
								mask = blue_mask)

		# Kırmızı renki takip etmek ve kontur oluşturma
		contours, hierarchy = cv2.findContours(red_mask,
											cv2.RETR_TREE,
											cv2.CHAIN_APPROX_SIMPLE)
		
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if(area > 300):
				x, y, w, h = cv2.boundingRect(contour)
				imageFrame = cv2.rectangle(imageFrame, (x, y),
										(x + w, y + h),
										(0, 0, 255), 2)
				
				cv2.putText(imageFrame, "Red Colour", (x, y),
							cv2.FONT_HERSHEY_SIMPLEX, 1.0,
							(0, 0, 255))	

		# Yeşil renki takip etmek ve kontur oluşturma
		contours, hierarchy = cv2.findContours(green_mask,
											cv2.RETR_TREE,
											cv2.CHAIN_APPROX_SIMPLE)
		
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if(area > 300):
				x, y, w, h = cv2.boundingRect(contour)
				imageFrame = cv2.rectangle(imageFrame, (x, y),
										(x + w, y + h),
										(0, 255, 0), 2)
				
				cv2.putText(imageFrame, "Green Colour", (x, y),
							cv2.FONT_HERSHEY_SIMPLEX,
							1.0, (0, 255, 0))

		# Mavi renki takip etmek ve kontur oluşturma
		contours, hierarchy = cv2.findContours(blue_mask,
											cv2.RETR_TREE,
											cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if(area > 300):
				x, y, w, h = cv2.boundingRect(contour)
				imageFrame = cv2.rectangle(imageFrame, (x, y),
										(x + w, y + h),
										(255, 0, 0), 2)
				
				cv2.putText(imageFrame, "Blue Colour", (x, y),
							cv2.FONT_HERSHEY_SIMPLEX,
							1.0, (255, 0, 0))
				
		# Program Termination
		cv2.imshow("Renk algilama ", imageFrame)
		if cv2.waitKey(10) & 0xFF == ord('q'):
			cap.release()
			cv2.destroyAllWindows()
			break

