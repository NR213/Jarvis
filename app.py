import codecs
import io
from pyexpat.errors import codes
from urllib import request
from flask import Flask, jsonify, render_template,request, redirect
#from utils import predict
import csv
import pandas as pd
import json

app = Flask(__name__)
  

@app.route('/Jarvis', methods=['GET'])
def upload_file():
    """ Simple html file to pass data """
    return render_template('upload_file.html')

@app.route('/Jarvis', methods=['POST'])
def validate_file():
    """ Validates the data and the query and populates the result """
    try:
        if 'file' not in request.files:
            raise Exception('File not uploaded properly')
        
        file = json.load(request.files.get('file'))

        print(file['data'])
        
        print(file['questions'])

        excel_data = file['data'] # needs to be further processed!
        query = list(file['questions'])
        if  not query:
            raise Exception('No proper data or query found!')

        # #result = predict(excel_data,query)
        # result = 1
        # if not result:
        #     raise Exception ('Something is wrong with prediction function, please have a look!')
        
        validated_result = {
                            'status': 200,
                            'data': 'success',
                            'Error': None
                            }
        
        return render_template('show_data.html', validated_result=validated_result)
    except Exception as e:
        
        validated_result = {'status': 404,
                                    'data': None,
                                    'Error': 'Error with data!'
                            }
        
        # message = e.args[0] 
        # if message:
        #     validated_result = jsonify({'status': 404,
        #                                 'data': None,
        #                                 'Error': message
        #                                 })
        
        print(validated_result)
            
        return render_template('show_data.html', validated_result=validated_result)
        

if __name__ == "__main__":
    app.run(debug=True)