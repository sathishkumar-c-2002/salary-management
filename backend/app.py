from flask import Flask,request,jsonify
from flask_cors import CORS
from salary_calculator import generate_salary_report

app= Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # For development
            "https://salary-management-frontend.onrender.com/"  # Your Render frontend URL
        ]
    }
})

@app.route('/api/calculate',methods=['POST'])
def calculate():
    data = request.json
    report = generate_salary_report(data)
    return jsonify(report)

if __name__=='__main__':
    # app.run(debug=True)
     app.run(host='0.0.0.0', port=10000)