# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
import flask
from flask import jsonify
from flask import Flask, render_template, request, url_for, json
import pandas as pd
import flask_json
from flask_json import FlaskJSON, JsonError, json_response, as_json

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

def display_top(filename, v, n):
    DD=pd.DataFrame()
    for chunk in pd.read_table(filename, sep="^", chunksize=10000):
        chunk.columns=map(str.strip, chunk.columns)
        DD=DD.append(chunk[['arr_port','pax']], ignore_index =True)
    D1= DD.groupby("arr_port")["pax"].sum().order(ascending=False)[:n]
    D1.index=map(str.strip, D1.index)
    D1.air_port=D1.index
    return D1.to_dict()

@app.route('/result/', methods=['POST'])
def result():
    n=request.form['top']
    if n=='':
	return "Please submit a value of top's"
    if not n.isdigit() or int(n)>10:
	return 'The submitted value is not integer! Please return and run again'
    filename='/media/sf_VM_share/bookings.csv'
    v=dict(fields= ['pax', 'arr_port'])
    n=int(n)
    #print n
    json_string = display_top(filename,v,n)
    #print 'Json: %s' % json_string
    return render_template('index.html', json = json_string)
    #return jsonify(json=json_string)

# Run the app :)
if __name__ == '__main__':
  app.run(debug=True)

