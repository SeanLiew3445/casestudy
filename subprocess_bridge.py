import subprocess, sys
from flask import Flask, jsonify

def bridge_pc(bridge):
	show = subprocess.Popen(('sudo ovs-vsctl show | grep ' + bridge), shell=True, stdout=subprocess.PIPE).communicate()[0]
	return show

def get_bridge(bridge):
	read = subprocess.call(['sudo', 'ovs-vsctl', 'list', 'Bridge', bridge])
	return read

def add_bridge(bridge):
	add = subprocess.call(['sudo', 'ovs-vsctl', 'add-br', bridge])

def del_bridge(bridge):
	delete = subprocess.call(['sudo', 'ovs-vsctl', '--if-exists', 'del-br', bridge])

def update_bridge(bridge, options):
        update = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'Bridge', bridge, options])

