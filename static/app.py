import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

# แก้ไขบรรทัดนี้เพื่อระบุพาธของโฟลเดอร์ template และ static อย่างชัดเจน
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.urandom(24)

AUTHORIZED_EMAIL = "wiyadaprasomrak@gmail.com"
requests_data = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if email == AUTHORIZED_EMAIL:
            session['logged_in'] = True
            session['email'] = email
            return redirect(url_for('view_requests'))
        else:
            return "อีเมลไม่ถูกต้อง โปรดลองอีกครั้ง"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        sender_name = request.form.get('sender_name')
        study_room = request.form.get('study_room')
        pickup_location = request.form.get('pickup_location')
        receiver_name = request.form.get('receiver_name')
        delivery_location = request.form.get('delivery_location')
        item_to_deliver = request.form.get('item_to_deliver')
        desired_delivery_time = request.form.get('desired_delivery_time')

        if sender_name and study_room and pickup_location and receiver_name and delivery_location and item_to_deliver and desired_delivery_time:
            new_request = {
                'sender_name': sender_name,
                'study_room': study_room,
                'pickup_location': pickup_location,
                'receiver_name': receiver_name,
                'delivery_location': delivery_location,
                'item_to_deliver': item_to_deliver,
                'desired_delivery_time': desired_delivery_time,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            requests_data.append(new_request)
            return render_template('success.html')
        else:
            return "กรุณากรอกข้อมูลให้ครบถ้วน"
    return render_template('submit_form.html')

@app.route('/requests')
def view_requests():
    if 'logged_in' in session and session['email'] == AUTHORIZED_EMAIL:
        return render_template('requests.html', requests=requests_data)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5555)