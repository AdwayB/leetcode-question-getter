from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from helpers.filter_data import filter_data
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)


def is_valid_percentage(value):
    try:
        percentage = int(value)
        return 0 <= percentage <= 100
    except ValueError:
        return False


def is_valid_topics(topics):
    if not isinstance(topics, list):
        return False
    for topic in topics:
        if not re.match("^[A-Z][a-zA-Z \-\(\)]*$", topic):
            return False
    return True


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/fetch', methods=['POST', 'GET'])
def fetch_questions():
    try:
        num_questions = int(request.form['num_questions'])
        easy_proportion = int(request.form['easy_proportion'])
        medium_proportion = int(request.form['medium_proportion'])
        hard_proportion = int(request.form['hard_proportion'])
        topics = request.form.getlist('topics')

        print(f"Topics Requested: {topics}")  # Debugging

        if not is_valid_percentage(easy_proportion) or not is_valid_percentage(
                medium_proportion) or not is_valid_percentage(hard_proportion):
            flash("Each difficulty percentage must be between 0 and 100.")
            raise ValueError("Each difficulty percentage must be between 0 and 100.") 

        if easy_proportion + medium_proportion + hard_proportion != 100:
            flash("The sum of all difficulty percentages must be 100.")
            raise ValueError("The sum of all difficulty percentages must be 100.") 

        if not is_valid_topics(topics):
            flash("Topics must only contain alphabets, commas, spaces and parentheses.")
            raise ValueError("Topics must only contain alphabets, commas, spaces and parentheses.") 

        filtered_data, json_file, excel_file = filter_data(num_questions, easy_proportion, medium_proportion,
                                                           hard_proportion,
                                                           topics)

        return render_template('results.html', tables=filtered_data.to_html(classes='data', escape=False),
                               json_file=json_file,
                               excel_file=excel_file)
    except ValueError as e:
        flash("Please enter valid input values.")
        print(f"Exception: {e}")
        return redirect(url_for('home'))
    except Exception as e:
        flash("An error occurred while fetching data.")
        print(f"Exception: {e}")
        return redirect(url_for('home'))


@app.route('/download/<filetype>')
def download_file(filetype):
    if filetype == 'json':
        return send_file('lc-questions.json', as_attachment=True)
    elif filetype == 'excel':
        return send_file('lc-questions.xlsx', as_attachment=True)
    else:
        return "Invalid file type!", 400
