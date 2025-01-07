from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('in.html')

@app.route('/get_value')
def get_value():
    v = "py"
    return v

if __name__ == '__main__':
    app.run(debug=True)
