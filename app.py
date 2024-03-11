#importing the libraries
from flask import Flask, render_template, request, jsonify
import re
import html

#intializing the flask object
app = Flask(__name__)

#creating a route and bind it with functionality
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    test_string = html.escape(request.form['test_string'])
    regex_pattern = html.escape(request.form['regex_pattern'])
    
    # Use a try-except block to handle invalid regex patterns safely.
    try:
        matches = re.findall(regex_pattern, test_string)
    except re.error:
        matches = []
        regex_pattern = "Invalid regex pattern"

    num_matches = len(matches)
    digit_or_string_count = sum(1 for char in test_string if char.isdigit() or char.isalpha())

    # Generate an explanation dynamically based on user input (sanitized).
    explanation = "The regex pattern searches for sequences of characters that match the specified pattern. " \
                  "In this case, it looks for sequences that match the pattern '{}' in the test string. " \
                  "The pattern matches {} times in the test string. " \
                  "Additionally, the test string contains {} digits or alphabetic characters.".format(regex_pattern, num_matches, digit_or_string_count)

    # Render the results along with the original input and the explanation.
    return render_template('index.html', test_string=test_string, regex_pattern=regex_pattern, matches=matches, num_matches=num_matches, digit_or_string_count=digit_or_string_count, explanation=explanation)

@app.route('/validate-email', methods=['POST'])
def validate_email():
    # Extract and sanitize the email input
    email = html.escape(request.form['email'])
    regex_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    
    is_valid = re.match(regex_pattern, email) is not None
    result_message = "Valid email address." if is_valid else "Invalid email address."
    
    # Use jsonify to send the response back as JSON
    return jsonify({'email': email, 'is_valid': is_valid, 'result_message': result_message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)