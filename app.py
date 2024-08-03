from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = 'data.csv'

def ensure_csv_file():
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'subtitle', 'content', 'timestamp']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

def read_data():
    ensure_csv_file()  
    data_list = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(row)
    return data_list

def write_data(data_list):
    ensure_csv_file()  
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['title', 'subtitle', 'content', 'timestamp']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)

@app.route('/')
def index():
    data_list = read_data()
    return render_template('index.html', data_list=data_list)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    subtitle = request.form['subtitle']
    content = request.form['content']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data_list = read_data()
    data_list.append({'title': title, 'subtitle': subtitle, 'content': content, 'timestamp': timestamp})
    
    write_data(data_list)
    
    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    data_list = read_data()
    if 0 <= index < len(data_list):
        data_list.pop(index)
        write_data(data_list)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
  
