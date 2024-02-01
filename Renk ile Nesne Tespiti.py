import cv2
import numpy as np
from collections import deque

#NESNE MERKEZİNE DEPOLAYACAK VERİ TİPİ
buffer_size = 16
pts = deque(maxlen= buffer_size)

# mavi renk aralığı  HSV H=TON(84,179) / S = DOYGUNLUK(98,255) / V = PARLAKLIK(0,255)
blueLower = (84 , 98 , 0)
blueUpper = (179 , 255 , 255)

#CAPTURE 
cap=cv2.VideoCapture(0)
cap.set(3, 940)
cap.set(4, 480)

while True:
    success, imgOriginal = cap.read()
    
    if success:
        
        #blur
        blurred = cv2.GaussianBlur(imgOriginal ,(11,11), 0)
        #hsv
        hsv = cv2.cvtColor(blurred , cv2.COLOR_BGR2HSV)  
        cv2.imshow("HSW IMG", hsv)
        
        #mavi için maske oluştur
        mask = cv2.inRange(hsv, blueLower , blueUpper)
        cv2.imshow("mask image", hsv  ) 
        
        #maskenin etrafında kalan gürültüleri sil
        mask = cv2.erode(mask, None, iterations=2) #erezyon
        mask = cv2.dilate(mask, None, iterations=2) #genişletme
        cv2.imshow("mask+ erezyon ve genisleme", mask)
        
        # kontur bulma => (_,contours,_) 
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center =None
        if len(contours) > 0:
            print("if")
            
            #en büyük konturu al
            c = max(contours, key=cv2.contourArea)
            
    
            # dikdörtgene çevir
            rect = cv2.minAreaRect(c)
                
            ((x,y), (width,height),rotation ) = rect
                
            s = "x: {}, y: {}, widht: {}, heiht: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            print(s)
            
                  
            # kutucuk 
            box = cv2.boxPoints(rect)
            box = np.int64(box)
            
            # moment
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                
            #konturu çizdir sarı
            cv2.drawContours(imgOriginal , [box], 0, (0,255,255),2)
        
            # merkese bir tane nokta çizdirelim pembe
            cv2.circle( imgOriginal , center, 5, (255,0,255), -1)
                
            #bilgileri ekrana yazdır
            cv2.putText(imgOriginal , s , (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL , 1 , (255,255,255), 2 )
        else:
            print("Kontur bulunamadı veya boş liste döndü.")

        # deque geçtiği noktalardan çizgi şeklinde gelmesini sağlar
        pts.appendleft(center)
        
        for i in range(1, len(pts)):
            
            if pts[i-1] is None or pts[i] is None: continue
        
            cv2.line(imgOriginal ,pts[i-1] ,pts[i] , (0,255,0),3 ) 
            
        cv2.imshow("orjinal tespit", imgOriginal)
                                                                                                         
     
    if cv2.waitKey(1) & 0xFF == ord('q'): break
cap.release()
cv2.destroyAllWindows()

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
