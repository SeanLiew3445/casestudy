import subprocess
from flask import Flask, jsonify

def get_ovsctlshow(bridge):
	show = subprocess.check_output(['sudo', 'ovs-vsctl', 'show', '|', 'grep', bridge])
	return show

def check(port):
	show = subprocess.check_output(['sudo', 'ovs-vsctl', 'show', '|', 'grep', port])
        return show

def get_ports(bridge):
	read = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-ports-desc', bridge])
	return read

def add_ports(bridge, interface):
	add = subprocess.call(['sudo', 'ovs-vsctl', 'add-port', bridge, interface])

def del_ports(bridge, port):
	delete = subprocess.call(['sudo', 'ovs-vsctl', '--if-exists', 'del-port', bridge, port])

def update_ports(bridge, port, action):
	update = subprocess.call(['sudo', 'ovs-ofctl', 'mod-port', bridge, port, action])
