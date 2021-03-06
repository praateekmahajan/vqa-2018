import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from flask import Flask, render_template, send_from_directory, flash
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys
from werkzeug import SharedDataMiddleware
from test_new_forward_pass import *

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule('/static/images/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': app.config['UPLOAD_FOLDER']
})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/process_vqa', methods=['GET', 'POST'])
def process_vqa():
    if request.method == "POST":
        return "LMAO"
    image = request.args['filename']
    question = request.args['question']

    # PROCESS IMAGE ETC HERE
    answers = run_forward(image, question)
    # answers = [("yes", '90'), ('no', '5'), ('bhat bc', '5')]
    print(answers)
    return render_template('answer.html', image=image, question=question, answers=answers)


@app.route('/', methods=['GET', 'POST'])
def index_function():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if 'question' not in request.form:
            flash("No question")
            return redirect(request.url)
        question = request.form['question']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename) and question:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return "Uploaded"
            return redirect(url_for('process_vqa',
                                    filename=filename,
                                    question=question))
    return render_template('index.html')


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run(debug=True)
