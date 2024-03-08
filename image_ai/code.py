##################################################import###########################################################
import pytesseract	 
from pytesseract import Output
import re
from PIL import Image
from googletrans import Translator
import cv2
##################################################Configurations###################################################
myconfig=r"--psm 11 --oem 3"
##################################################################################################################
text=pytesseract.image_to_string(Image.open('test.jpg'),config=myconfig,lang="eng")
img=cv2.imread("demo.png")
height,width,_=img.shape
data=pytesseract.image_to_data(img,config=myconfig,output_type=Output.DICT)
amount_boxes=len(data['text'])
for i in range(amount_boxes):
    if float(data['conf'][i])>20:
        (x,y,width,height)=(data['left'][i],data['top'][i],data['width'][i],data['height'][i])
        img=cv2.rectangle(img,(x,y),(x+width,y+height),(0,255,0),2)
        img=cv2.putText(img,data['text'][i],(x,y+height+20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2,cv2.LINE_AA)
'''def translate():
    translator = Translator()
    translated_text = translator.translate(text, dest='es').text
    print('Original text: ', text)
    print('Translated text: ', translated_text)'''
def detect_image_lang(img_path):
    try:
        osd = pytesseract.image_to_osd(img_path)
        script = re.search("Script: ([a-zA-Z]+)\n", osd).group(1)
        conf = re.search("Script confidence: (\d+\.?(\d+)?)", osd).group(1)
        return script, float(conf)
    except e:
        return None, 0.0
script_name, confidence = detect_image_lang("test.jpg")
'''translate()'''
print(script_name)
print(text)
cv2.imshow("img",img)
cv2.waitKey(0)