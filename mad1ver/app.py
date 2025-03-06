from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        print(request.form['name'])
        return redirect(url_for('form'))
    return render_template('form.html')

@app.route('/print', methods=['GET', 'POST'])
def print_on_html():
    if request.method == 'POST':
        return render_template('print.html', name=request.form['name'])
    return render_template('print.html')

@app.route('/print/<name>')
def print_on_html2(name):
    return render_template('print.html', name=name)


if __name__ == '__main__':
    app.run()