from flask import Flask, jsonify, request

app = Flask(__name__)

# Define a simple endpoint with input parameter
@app.route('/hello', methods=['GET'])
def hello():
    # Get the 'name' parameter from the query string
    name = request.args.get('name', 'World')
    return jsonify({'message': f'Hello, {name}!'})

if __name__ == '__main__':
    app.run(debug=True)
