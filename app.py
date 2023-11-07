from flask import Flask, request, render_template
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = load_model('weather_model.h5')

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        img = image.load_img(file.stream, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        predictions = model.predict(img_array)
        predicted_class_indices = np.argmax(predictions, axis=1)
        labels = {0: 'Winter', 1: 'Summer', 2: 'Autumn', 3: 'Spring'}
        predicted_label = labels[predicted_class_indices[0]]
        return predicted_label

if __name__ == '__main__':
    app.run(debug=True)
