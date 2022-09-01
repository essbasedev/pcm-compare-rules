#!/usr/bin/env python
import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
import os
from telegram import send_message
from main import compare_files, final_output
import uuid
from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
uploads = os.path.join(BASE_DIR, 'uploads')
app = Flask(__name__)
app.secret_key = "some secret string"
bootstrap = Bootstrap(app)
file1_name = None
file2_name = None
file1_status = False
file2_status = False


class UploadForm(FlaskForm):
    file_select = FileField('Select the XML file', validators=[DataRequired()])
    # submit = SubmitField(label="Upload")


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    log = ["🟡 Waiting for first file to upload"]
    global file1_name, file2_name
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file_select.data
        file_new_name = os.path.join(uploads, uuid.uuid4().hex + ".xml")
        file.save(file_new_name)
        if file1_name is None:
            try:
                file1_name = file_new_name
                log[0] = "🟢 File1 Uploaded successfully"
                log.append("🟡 Waiting for 2nd file to upload")
                return render_template('upload.html', form=form, step='Step 2', btn_val="Process Files >>", log=log)
            except:
                log[0] = "🔴 Error in uploading 1st file. Please try again."
        elif file2_name is None:
            try:
                file2_name = file_new_name
                compare_files(file1_name, file2_name)
                return redirect(url_for('result'))
            except:
                log[0] = "🟢 File1 Uploaded successfully"
                log.append("🔴 Error in uploading 2nd file. Please try again.")
    file1_name = None
    file2_name = None
    return render_template('upload.html', form=form, step='Step 1', btn_val="Next >>", log=log)


@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html', output=final_output)


@app.route('/about', methods=['GET', 'POST'])
def about():
    kanye_api = requests.get('https://api.kanye.rest/')
    api_data = kanye_api.json()['quote']
    return render_template('about.html', quote=api_data)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    print(request.method)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        telegram = request.form['telegram_id']
        message = request.form['message']
        agree = request.form['agree']
        message_text = f"Message from https://essbase.dev/pcm-tools/contact\n" \
                       f"Name: {name}\n" \
                       f"Email: {email}\n" \
                       f"Phone: {phone}\n" \
                       f"Telegram: @{telegram}\n" \
                       f"Message: {message}\n" \
                       f"Agree: {agree}"
        send_message(message_text)
        return render_template(
            'contact.html',
            h1_message='Thank you!',
            card_title='Your message has been sent!',
            card_text='I will respond to you as soon as it is possible.'
        )
    else:
        return render_template(
            'contact.html',
            h1_message='Contact Me!',
            card_title='Have doubts or want to share your inputs?',
            card_text='Feel free to post your message, I will respond to you as soon as possible.'
        )


if __name__ == '__main__':
    app.run(debug=True)
