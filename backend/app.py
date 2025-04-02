from flask import Flask,request,jsonify
from flask_cors import CORS
from calculator import generate_salary_report

app= Flask(__name__)
CORS(app)

@app.route('/api/calculate',methods=['POST'])
def calculate():
    data = request.json
    report = generate_salary_report(data)
    return jsonify(report)

if __name__=='__main__':
    app.run(debug=True)