from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        irradiation = float(request.form['irradiation'])
        temperature = float(request.form['temperature'])
        max_power = irradiation * (temperature + 25)  # A simple calculation for demonstration purposes

        return render_template('index.html',
                               irradiation=irradiation,
                               temperature=temperature,
                               max_power=max_power)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)