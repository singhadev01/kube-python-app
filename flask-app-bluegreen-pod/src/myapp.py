from flask import Flask, render_template
import os, sys

# get version from env variable
if 'APP_VERSION' in os.environ.keys():
    APP_VERSION = os.environ['APP_VERSION']   
else:
    APP_VERSION = 'UNDEFINED'
print(f"App Version {APP_VERSION}")

app=Flask(__name__)

@app.route('/')
def home():
    return  render_template("home.html")

@app.route('/about')
def about():
    return  render_template("about.html")

@app.route('/info')
def  info():
    return "App Version " + APP_VERSION

@app.route('/version')
def  version():
    if APP_VERSION is None:
        color = '#ffffff' #  white = '#ffffff'
        return render_template("version.html", version = APP_VERSION, color = color )
    
    if APP_VERSION.upper() == 'V1':
        color = '#4dfff0' ##  blue
    elif APP_VERSION.upper() == 'V2':
        color ='#81F781' ## Green
    else:
        color = '#FA5858' #redbrown
    return render_template("version.html", version = APP_VERSION, color = color )

@app.route('/<my_name>')
def greeting(my_name):
    uc = my_name.upper()
    return f"<h1> Welcome Mr/Mrs {uc} to our world </h1>"


@app.route('/square/<int:num>')
def square(num):
    result = num ** num
    return f'square of # {str(num)} = {str(result)}' 


if __name__ == "__main__":
    #app.run(debug=True)
    #app.run(host='127.0.0.1', port=9999, debug=True)
    app.run(host='0.0.0.0', port=9999, debug=True)