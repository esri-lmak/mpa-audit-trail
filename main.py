import requests
import pypyodbc
import db_connection as dbConnection
import flask
from flask import jsonify
from flask import flash, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>MPA - Geospace SEA Audit Trail</h1>
    	<p>A prototype API for inserting audit trail in Geoportal.</p>'''

@app.route('/create', methods=['POST'])
def createAuditTrail():
	# Get the sql connection
	connection = dbConnection.getConnection()
	cursor = connection.cursor()

	try:
		_json = request.json
		_auditTrailTypeId = _json['auditTrailTypeId']
		_actionToId = str(requests.get('https://www.wikipedia.org').headers['X-Client-IP'])
		_remark = _json['remark']
		_notes = _json['notes']
		_createdBy = _json['createdBy']
		_createdDate = 'GETDATE()'
		
		# validate the received values
		if _auditTrailTypeId and _actionToId and _remark and _notes and _createdBy and request.method == 'POST':
			# save edits
			sql = "INSERT INTO AuditTrail(AuditTrailTypeId, ActionToId, Remark, Notes, CreatedDate, CreatedBy) VALUES(%s, %s, %s, %s, %s, %s)"
			data = (_auditTrailTypeId, _actionToId, _remark, notes, _createdDate, _createdBy)
			cursor.execute(sql, data)
			connection.commit()
			response = jsonify('Record created successfully!')
			response.status_code = 200
			return response
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		connection.close()

@app.route('/all', methods=['GET'])
def getAllAuditTrail():
	# Get the sql connection
	connection = dbConnection.getConnection()
	cursor = connection.cursor()
	
	try:
		sql = "SELECT * FROM AuditTrail"
		all_records = cursor.execute(sql).fetchall()
		return jsonify(all_records)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		connection.close()

@app.route('/ip', methods=['GET'])
def ip():
	# GET IP address
	ip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
	return ip

if __name__ == "__main__":
	app.run(debug = True);
