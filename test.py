import face_recognition
import cv2

# Load an image file
image = face_recognition.load_image_file("path_to_your_image.jpg")

# Find all face locations and encodings in the image
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

# Print results
print("Found {} face(s) in the image.".format(len(face_locations)))
