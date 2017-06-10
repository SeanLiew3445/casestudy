import subprocess_sean, json
from flask import Flask, jsonify, request

cs = Flask(__name__)

@cs.route('/show', methods=['GET'])
def get_show():
	return subprocess_sean.get_ovsctlshow()

@cs.route('/read/<bridge>', methods=['GET'])
def get_read(bridge):
	return subprocess_sean.get_ports(bridge)	

@cs.route('/add', methods=['POST'])
def add_port():
	bridge = request.json['bridge']
	interface = request.json['interface']
	subprocess_sean.add_ports(bridge, interface)
	return jsonify({'Bridge': bridge,
			'Interface': interface}), 201

@cs.route('/delete/<bridge>', methods=['DELETE'])
def del_port(bridge):
	port = request.json['port']
	subprocess_sean.del_ports(bridge, port)
	return jsonify({'result': True})

@cs.route('/update/<bridge>/<port>', methods=['PUT'])
def update_port(bridge, port):
	action = request.json['action']
	subprocess_sean.update_ports(bridge, port, action)
	return subprocess_sean.get_ports(bridge)

if __name__ == '__main__':
	cs.run(debug=True)
