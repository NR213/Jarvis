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

        excel_data = file['dataQueries'] 
        questions = file['questions']
        if not excel_data:
            raise Exception('No proper data or query found!')

        queryString = ''
        queryString += '|'.join([data['name'].split('.')[1] for data in excel_data])
        data_headers = [data['name'].split('.')[1] for data in excel_data]

        row_values = []
        rows = []
        count = 0
        while count < len(excel_data[0]["data"]):
            for each in excel_data:
                for index,value in enumerate(each['data']):
                    if index == count:
                        row_values.append(value)
            row_list = {f"row_{count}":row_values}
            row_values = []
            rows.append(row_list)
            count = count + 1
        
        for index, data in enumerate(rows):
            queryString += '\n'
            queryString += '|'.join([str(element) for element in data[f'row_{index}']])

        print(queryString)
        print(questions)

        #result = predict(queryString,questions)


        
        
        validated_result = {
                            'status': 200,
                            'data': 'success',
                            'Error': None
                            }
        
        return render_template('show_data.html', validated_result=validated_result)
    except Exception as e:
        print(e)
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