from flask import Flask, jsonify

app = Flask("financial")

# Define a simple endpoint
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=False)
