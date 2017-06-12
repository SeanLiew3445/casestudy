import subprocess, sys
from flask import Flask, jsonify

def get_ovsctlshow(bridge):
	show = subprocess.Popen(('sudo ovs-vsctl show | grep ' + bridge), shell=True, stdout=subprocess.PIPE).communicate()[0]
	return show

def int_pc(port):
	show = subprocess.Popen(('sudo ifconfig | grep ' + port),shell=True, stdout=subprocess.PIPE).communicate()[0]
        return show

def int_bridge(port):
	show = subprocess.Popen(('sudo ovs-vsctl show | grep ' + port), shell=True, stdout=subprocess.PIPE).communicate()[0]
        return show

def get_ports(bridge):
	read = subprocess.call(['sudo', 'ovs-ofctl', 'dump-ports-desc', bridge])
	return read

def add_ports(bridge, interface):
	add = subprocess.call(['sudo', 'ovs-vsctl', 'add-port', bridge, interface])

def del_ports(bridge, port):
	delete = subprocess.call(['sudo', 'ovs-vsctl', '--if-exists', 'del-port', bridge, port])

def update_ports(bridge, port, action):
	update = subprocess.call(['sudo', 'ovs-ofctl', 'mod-port', bridge, port, action])
