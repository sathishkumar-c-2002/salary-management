from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId
from salary_calculator import generate_salary_report
from datetime import datetime
import os

app = Flask(__name__)

# Configuring MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI" ,"mongodb+srv://csathishkumar:renuka02@cluster0.ktgvzmh.mongodb.net/salary_reports?retryWrites=true&w=majority&appName=Cluster0") #, "mongodb://localhost:27017/salary_reports")
mongo = PyMongo(app)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  
            "https://salary-manage.netlify.app",
            "https://salary-management-frontend.onrender.com"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/api/test-db-connection', methods=['GET'])
def test_db_connection():
    """Endpoint to test MongoDB connection and basic operations"""
    try:
        # Test connection by performing a simple operation
        test_data = {
            "test": "connection",
            "timestamp": datetime.utcnow(),
            "status": "testing"
        }
        
        # Test insert operation
        insert_result = mongo.db.reports.insert_one(test_data.copy())
        
        # Test read operation
        fetched_data = mongo.db.reports.find_one({"_id": insert_result.inserted_id})
        
        # Test delete operation (clean up)
        delete_result = mongo.db.reports.delete_one({"_id": insert_result.inserted_id})
        
        return _corsify_response(jsonify({
            "status": "success",
            "connection": True,
            "inserted_id": str(insert_result.inserted_id),
            "fetched_data": {
                "_id": str(fetched_data["_id"]),
                "timestamp": fetched_data["timestamp"].isoformat(),
                "status": fetched_data["status"]
            },
            "deleted_count": delete_result.deleted_count,
            "message": "All database operations completed successfully"
        }))
        
    except Exception as e:
        return _corsify_response(jsonify({
            "status": "error",
            "connection": False,
            "error": str(e),
            "message": "Failed to connect to database"
        })), 500

@app.route('/api/calculate', methods=['POST', 'OPTIONS'])
def calculate():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    elif request.method == 'POST':
        data = request.json
        report = generate_salary_report(data)

        report_with_metadata = {
            **report,
            "created_at": datetime.utcnow(),
            "input_data": data,
            "ip_address": request.remote_addr
        }

        result = mongo.db.reports.insert_one(report_with_metadata)
        report['_id'] = str(result.inserted_id)

        return _corsify_response(jsonify(report))

@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = list(mongo.db.reports.find().sort("created_at", -1).limit(50))

    for report in reports:
        report['_id'] = str(report['_id'])
        report['created_at'] = report['created_at'].isoformat()
    return _corsify_response(jsonify(reports))

@app.route('/api/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    try:
        report = mongo.db.reports.find_one({'_id': ObjectId(report_id)})
        if report:
            report['_id'] = str(report['_id'])
            report['created_at'] = report['created_at'].isoformat()
            return _corsify_response(jsonify(report))
        return _corsify_response(jsonify({"error": "Report not found"}), 404)
    except Exception as e:
        return _corsify_response(jsonify({"error": "Invalid report ID format"}), 400)

def _build_cors_preflight_response():
    response = jsonify({'message': 'Preflight Request Accepted'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_pymongo import PyMongo
# from bson import ObjectId
# from salary_calculator import generate_salary_report
# from datetime import datetime
# import os

# app = Flask(__name__)

# #Configuring MongoDB
# app.config["MONGO_URI"] = os.getenv("MONGO_URI","mongodb://localhost:27017/salary_reports")
# mongo = PyMongo(app)

# CORS(app, resources={
#     r"/api/*": {
#         "origins": [
#             "http://localhost:3000",  
#             "https://salary-manage.netlify.app",
#             "https://salary-management-frontend.onrender.com"
#         ],
#         "methods": ["GET", "POST", "OPTIONS"],
#         "allow_headers": ["Content-Type"]
#     }
# })

# @app.route('/api/calculate', methods=['POST', 'OPTIONS'])
# def calculate():
#     if request.method == 'OPTIONS':
#         return _build_cors_preflight_response()
#     elif request.method == 'POST':
#         data = request.json
#         report = generate_salary_report(data)

#         report_with_metadata = {
#             **report,
#             "created_at": datetime.utcnow(),
#             "input_data":data,
#             "ip_address": request.remote_addr
#         }

#         result = mongo.db.reports.insert_one(report_with_metadata)

#         report['_id'] = str(result.inserted_id)

#         return _corsify_response(jsonify(report))


# @app.route('/api/reports',methods = ['GET'])
# def get_reports():
#     reports = list(mongo.db.reports.find().sort("created_at", -1).limit(50))

#     for report in reports:
#         report['_id'] = str(report['_id'])
#         report['created_at'] = report['created_at'].isoformat()
#     return _corsify_response(jsonify(reports))

# @app.route('/api/reports/<report_id>', methods=['GET'])
# def get_report(report_id):
#     report = mongo.db.reports.find_one({'_id': ObjectId(report_id)})
#     if report:
#         report['_id'] = str(report['_id'])
#         report['created_at'] = report['created_at'].isoformat()
#         return _corsify_response(jsonify(report))
#     return _corsify_response(jsonify({"error":"Report not found"}),404)




# def _build_cors_preflight_response():
#     response = jsonify({'message': 'Preflight Request Accepted'})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Headers", "*")
#     response.headers.add("Access-Control-Allow-Methods", "*")
#     return response

# def _corsify_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     return response

# if __name__ == '__main__':
#     app.run(debug=True)