import cv2
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model(r'alg\cnn.h5')

# Set up video capture device
cap = cv2.VideoCapture(0)

# Define labels
labels = ['Apple','Apple Black rot','Apple Cedar apple rust','Apple healthy','Blueberry healthy','Corn','Corn Gray leafspot',
'Corn healthy','Grape','Grape healthy','Grape Leaf blight','Orange Haunglongbing','Peach','Tomato']


def livestreaming():
    while True:
        # Read frame from video capture device
        ret, frame = cap.read()

        # Preprocess the image
        resized_frame = cv2.resize(frame, (256, 256))
        normalized_frame = resized_frame / 255.0
        input_frame = np.expand_dims(normalized_frame, axis=0)

        # Make prediction
        prediction = model.predict(input_frame)[0]

        # Get predicted label
        predicted_label = labels[np.argmax(prediction)]

        # Overlay label onto image
        cv2.putText(frame, predicted_label, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Show video frame
        cv2.imshow('frame', frame)

        # Wait for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture device and close window
    cap.release()
    cv2.destroyAllWindows()
