cat ueye.py > camera_temp.py
sed -i '/^_is_StopLiveVideo/,$!d' camera_temp.py
sed -iE 's/\(def is_[a-zA-Z_]*(\)hCam/\1self/g' camera_temp.py 
sed -i 's/(hCam/(self.hCam/' camera_temp.py
sed -i 's/^/    /' camera_temp.py


cat camera_class_template.txt > camera.py
cat camera_temp.py >> camera.py
rm camera_temp.py
rm *.pyE