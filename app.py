from flask import Flask, request, send_file, render_template_string
import io
from PIL import Image
import rembg
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

UPLOAD_FORM = '''
<!doctype html>
<title>Background Remover</title>
<h1>Upload an image to remove background</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=image accept="image/*">
  <input type=submit value=Upload>
</form>
'''

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No image uploaded', 400
        file = request.files['image']
        try:
            input_image = Image.open(file.stream)
        except Exception as e:
            return f"Invalid image file: {e}", 400
        output_image = rembg.remove(input_image)
        output_image.save("output.png")
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
