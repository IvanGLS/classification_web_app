import base64

from flask import Flask, request, render_template
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import io

app = Flask(__name__)

# Load the pre-trained model
model = load_model('weather_model.h5')


@app.route('/', methods=['GET'])
def index():
    # Show the upload form
    return render_template('upload.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        # Convert the file stream to an io.BytesIO object
        img_bytes = io.BytesIO(file.read())
        img = image.load_img(img_bytes, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        predictions = model.predict(img_array)
        predicted_class_indices = np.argmax(predictions, axis=1)
        labels = {0: 'Winter', 1: 'Summer', 2: 'Autumn', 3: 'Spring'}
        predicted_label = labels[predicted_class_indices[0]]

        # Encode the image to display in the result page
        img_bytes.seek(0)
        base64_img = base64.b64encode(img_bytes.read()).decode('utf-8')
        image_src = f"data:image/jpeg;base64,{base64_img}"

        return render_template('result.html', season=predicted_label, image_src=image_src)

    return 'Invalid file', 400



if __name__ == '__main__':
    app.run(debug=True)
