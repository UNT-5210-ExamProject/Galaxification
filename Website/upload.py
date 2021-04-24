import os
from flask import Flask, flash, request, redirect, render_template, url_for
import keras
import tensorflow as tf
import numpy as np 
from PIL import Image as PImage

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploaded_file/'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
processed_image = os.path.join(app.config['UPLOAD_FOLDER'], 'processedImage.png')
trained_model_path = './trained_model'
model = keras.models.load_model(trained_model_path)

def allowed_file_formats(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_prediction(uploaded_file):
    upoaded_image = PImage.open(uploaded_file)
    img_array = keras.preprocessing.image.img_to_array(upoaded_image)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    predicted_output = model.predict(img_array)
    classification_id = np.argmax(predicted_output, axis=1)[0]
    classification_type = classificationId_to_classificationName(classification_id)
    return classification_type

def classificationId_to_classificationName(argument): 
    dictionary = { 
        0: "Disk, Face-on, No Spiral", 
        1: "Smooth, Completely round", 
        2: "Smooth, in-between round",
        3: "Smooth, Cigar shaped", 
        4: "Disk, Edge-on, Rounded Bulge", 
        5: "Disk, Edge-on, Boxy Bulge",
        6: "Disk, Edge-on, No Bulge", 
        7: "Disk, Face-on, Tight Spiral", 
        8: "Disk, Face-on, Medium Spiral",
        9: "Disk, Face-on, Loose Spiral", 
    } 
    return dictionary.get(argument, "nothing")

def get_file_resolution_69_count(uploaded_file):
    submitted_file = PImage.open(uploaded_file)
    file_size_tuple = submitted_file.size
    return file_size_tuple.count(69)

@app.route("/")
def fileFrontPage():
    return render_template('fileform.html')

@app.route('/handleUpload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file_formats(file.filename):
            file.save(processed_image)
            if(get_file_resolution_69_count(processed_image) == 2):
                output = perform_prediction(processed_image)
                return render_template('fileform.html', output = "Predicted Value: {}".format(output))
            else:
                return render_template('fileform.html', output = "Invalid file resolution submitted. It should be of type 69*69 pixels.")
            ##Invoke classification model to classify processed image
            #return redirect(url_for('fileFrontPage'))
            ## can add a tempalte flash('Upload Complete..')
        else:
            return 'Invalid file format'
    return

if __name__ == '__main__':
    app.run()
