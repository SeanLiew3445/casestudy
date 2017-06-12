import subprocess_bridge, json
from flask import Flask, jsonify, request, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth

cs = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'sean':
		return 'liew'
	return None

@auth.error_handler
def unauthorised():
	return make_response(jsonify( { 'error': 'Unauthorised access' } ), 403)

@cs.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@cs.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

@cs.route('/read/bridge/<bridge>', methods=['GET'])
@auth.login_required
def get_bridge(bridge):
	#check if bridge exists on pc
	if len(str(subprocess_bridge.bridge_pc(bridge))) == 0:
		abort(404)

	return str(subprocess_bridge.get_bridge(bridge))	

@cs.route('/add/bridge/<bridge>', methods=['POST'])
@auth.login_required
def add_bridge(bridge):

	#check if bridge already exists
	if len(str(subprocess_bridge.bridge_pc(bridge))) == 0:
		abort(400)

	subprocess_bridge.add_bridge(bridge)
	return jsonify({'Bridge': bridge}), 201

@cs.route('/delete/bridge/<bridge>', methods=['DELETE'])
@auth.login_required
def del_bridge(bridge):
	
	#check if bridge exists
	if len(str(subprocess_bridge.bridge_pc(bridge))) == 0:
		abort(404)

	subprocess_bridge.del_bridge(bridge)
	return jsonify({'result': True})

@cs.route('/update/bridge/<bridge>', methods=['GET'])
@auth.login_required
def update_bridge(bridge):
        #check if bridge exists on pc
        if len(str(subprocess_bridge.bridge_pc(bridge))) == 0:
                abort(404)
	
	if not request.json or not 'options' in request.json:
		abort(400)

	options = request.json['options']
        return str(subprocess_bridge.update_bridge(bridge,options))

if __name__ == '__main__':
	cs.run(debug=True)
