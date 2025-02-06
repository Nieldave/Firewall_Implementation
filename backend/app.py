from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Log, Rule

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firewall.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    return jsonify([log.to_dict() for log in logs])

@app.route('/api/rules', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_rules():
    if request.method == 'GET':
        rules = Rule.query.all()
        return jsonify([rule.to_dict() for rule in rules])
    elif request.method == 'POST':
        data = request.json
        rule = Rule(**data)
        db.session.add(rule)
        db.session.commit()
        return jsonify(rule.to_dict()), 201
    elif request.method == 'PUT':
        data = request.json
        rule = Rule.query.get(data['id'])
        if rule:
            rule.update(data)
            db.session.commit()
            return jsonify(rule.to_dict())
        return jsonify({'error': 'Rule not found'}), 404
    elif request.method == 'DELETE':
        data = request.json
        rule = Rule.query.get(data['id'])
        if rule:
            db.session.delete(rule)
            db.session.commit()
            return jsonify({'message': 'Rule deleted'})
        return jsonify({'error': 'Rule not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)