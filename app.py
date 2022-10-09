import codecs
import io
from pyexpat.errors import codes
from flask import Response
from urllib import request
from flask import Flask, jsonify, render_template,request, redirect
from flask_ngrok import run_with_ngrok
import csv
import pandas as pd
import json

def create_app():
  app = Flask(__name__, instance_relative_config=True)
  run_with_ngrok(app) 

  @app.route('/', methods=['GET','POST'])
  def validate_file():
      json_output = {}
      try:
          excel_data = request.json['dataQueries'] 
          questions = request.json['questions']
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
          queryString = '"""'+ queryString + '"""'
          
          result = predict(queryString,questions)

          result = result.rstrip(result[-1])
          ans = result.split("|")
          
          json_output['answer'] = ans
          
          return Response(json_output['answer'], status=200, mimetype='application/json')
      
      except Exception as e:
          json_output['answer'] = ''
          return Response(json_output['answer'], status=404, mimetype='application/json')
  return app
