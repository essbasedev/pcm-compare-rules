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
from log import write_log, read_log

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


@app.route('/compare-rules', methods=['GET', 'POST'])
def upload():
    write_log("I", "Initiated upload process..")
    log = ["🟡 Waiting for first file to upload"]
    global file1_name, file2_name
    form = UploadForm()
    write_log("I", "Upload form class has been called")
    if form.validate_on_submit():
        write_log("I", "Validating the upload form")
        file = form.file_select.data
        file_new_name = os.path.join(uploads, uuid.uuid4().hex + ".xml")
        file.save(file_new_name)
        write_log("I", "file saved with new name")
        if file1_name is None:
            write_log("I", "If file1_name is none")
            try:
                write_log("I", "Try renaming file1_name = file new name")
                file1_name = file_new_name
                log[0] = "🟢 File1 Uploaded successfully"
                log.append("🟡 Waiting for 2nd file to upload")
                write_log("I", "Initiate 2nd file upload process")
                return render_template('upload.html', form=form, step='Step 2', btn_val="Process Files >>", log=log)
            except:
                write_log("E", "Error renaming file1_name = file new name ")
                log[0] = "🔴 Error in uploading 1st file. Please try again."
        elif file2_name is None:
            write_log("I", "If file2_name is none")
            try:
                write_log("I", "try file2_name = file_new_name")
                file2_name = file_new_name
            except:
                log[0] = "🟢 File1 Uploaded successfully"
                log.append("🔴 Error in uploading 2nd file. Please try again.")
                write_log("E", "Error renaming file2_name = file new name ")
            try:
                write_log("I", "Try comparing files")
                compare_files(file1_name, file2_name)
                write_log("I", "Success, the result is displayed.")
                return redirect(url_for('result'))

            except:
                write_log("E", "Error in comparing files")
                return redirect(url_for('error'))

    file1_name = None
    write_log("I", "file1_name=None")
    file2_name = None
    write_log("I", "file2_name=None")
    return render_template('upload.html', form=form, step='Step 1', btn_val="Next >>", log=log)


@app.route('/compare-rules/error', methods=['GET'])
def error():
    return render_template('error.html')


@app.route('/compare-rules/log', methods=['GET'])
def app_log():
    log_data = read_log()
    return render_template('log.html', log_data=log_data)


@app.route('/compare-rules/results', methods=['GET'])
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
