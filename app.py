from flask import Flask, render_template, request, redirect, url_for, send_file
import pdfkit
import imgkit
import uuid
import os

app = Flask(__name__)
EXPORT_FOLDER = "exports"
if not os.path.exists(EXPORT_FOLDER):
    os.makedirs(EXPORT_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    username = request.form.get('username')
    return render_template('game.html', username=username)

@app.route('/result', methods=['POST'])
def result():
    username = request.form.get('username')
    choice1 = request.form.get('choice1')
    choice2 = request.form.get('choice2')
    choice3 = request.form.get('choice3')

    outcome = "Game Over"
    reason = ""

    if choice1 == "left":
        if choice2 == "wait":
            if choice3 == "yellow":
                outcome = "You Win"
                reason = "You found the treasure!"
            elif choice3 == "red":
                reason = "Room full of fire."
            elif choice3 == "blue":
                reason = "Room of beasts."
            else:
                reason = "Invalid door chosen."
        else:
            reason = "Attacked by an angry trout."
    else:
        reason = "Fell into a hole."

    file_id = uuid.uuid4().hex
    export_file = os.path.join(EXPORT_FOLDER, f'{file_id}.pdf')

    rendered = render_template('result.html', username=username, outcome=outcome, reason=reason)
    
    # Generate PDF
    pdfkit.from_string(rendered, export_file)

    # Optionally generate image
    img_file = os.path.join(EXPORT_FOLDER, f'{file_id}.jpg')
    imgkit.from_string(rendered, img_file)

    return render_template('result.html', username=username, outcome=outcome, reason=reason,
                           pdf_file=f'{file_id}.pdf', img_file=f'{file_id}.jpg')

@app.route('/download/<file_type>/<filename>')
def download(file_type, filename):
    file_path = os.path.join(EXPORT_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

