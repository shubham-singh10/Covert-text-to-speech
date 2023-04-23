import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)


# Load Known Face

Shubham_image = face_recognition.load_image_file("Face/Shubham.png")
Shubham_encoding = face_recognition.face_encodings(Shubham_image)[0]
Pranjal_image = face_recognition.load_image_file("Face/Pranjal.jpg")
Pranjal_Encoding = face_recognition.face_encodings(Pranjal_image)[0]

Known_face_encoding = [Shubham_encoding, Pranjal_Encoding]
Known_face_name = ["Shubham", "Pranjal"]

# list of expected students
students = Known_face_name.copy()

face_locations = []
face_encodings = []

# Get Current date and Time

now = datetime.now()
current_date = now.strftime("%y-%m-%d")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

#     Recognize faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(Known_face_encoding, face_encoding)
        face_distance = face_recognition.face_distance(Known_face_encoding, face_encoding)
        best_match_index = np.argmin(face_distance)

        if(matches[best_match_index]):
            name = Known_face_name[best_match_index]

    #    Add the text if a person is present
        if name in Known_face_name:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (255, 0, 0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + " Present", bottomLeftCornerOfText, font, fontScale,
                        fontColor, thickness, lineType)

            if name in students:
                students.remove(name)
                current_time = now.strftime("%H-%M-%S")
                lnwriter.writerow([name, current_time])

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
