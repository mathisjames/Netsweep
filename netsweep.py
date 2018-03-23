#!/usr/bin/python -W all

#-----------------------------------------------------------------------------#
# A P P  I N F O R M A T I O N #
#-----------------------------------------------------------------------------#
#
# NAME: NETSWEEP 
# DATE: 3/13/2018
# CREATOR: James Mathis
#
# DESCRIPTION:
#	Scan your default network (eth0) for devices.
# Display open ports, system information, and versions.
#
# (Note: This is a simple use case, with little error handling)
#
# VERSION: 1.0
#
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# M O D U L E S #
#-----------------------------------------------------------------------------#
import sys
import os
import commands
import re

#-----------------------------------------------------------------------------#
# C U S T O M  M O D U L E S #
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# C O N S T A N T  V A R I A B L E S #
#-----------------------------------------------------------------------------#
IP_LINE = 1
IP_ADDRESS = 11
UBUNTU_INFO = "addr"
FALSE = -1
NODE_ADDRESS = 4
NMAP = "nmap -sP "
IFCON = "/sbin/ifconfig eth0"

#-----------------------------------------------------------------------------#
# G L O B A L  V A R I A B L E S #
#-----------------------------------------------------------------------------#
network_nodes = {}	# node dict


#-----------------------------------------------------------------------------#
# F U N C T I O N S #
#-----------------------------------------------------------------------------#

#----------------------#
# Get node information #
#------------------------------------------#
def node_port_info(nodes):

	# loop through node list #
	for k, v in nodes.items():

                # Display screen information #
                print "\nScanning Node: ", v['ip_address']

		# get node information (Ports, MAC, Version)
        	status, output = commands.getstatusoutput( "nmap -sS " + v['ip_address']  )

		# split each line into array #
		tmp_ports = output.split('\n')

                # create new tmp list #
                tmp_list = []

		# loop through array, and cut out node information we need #
		for port in tmp_ports:

			# check if this is a line with port information #
			if re.search("open", port):

				# drop everything after first space and keep port num #
				port = re.sub(" .*$", "", port)

				# split line up for single ports #
				tmp_port = port.split('\n')

				# check if there are ports #
				if tmp_port:
					tmp_list.append( tmp_port )

		if not tmp_list:
			# add flag of no ports #
			v['ports'] = "NOP"
			
			# update dict with changes #
			nodes[k].update(v)

		else:
			# add ports to dict #
			v['ports'] = tmp_list

			# update dict with changes #
			nodes[k].update(v)

		# display information for user #
		print( "Recording node information" ) 


#-------------------------#
# gather all online nodes #
#------------------------------------------#
def online_nodes(raw_nodes):

	# split nodes up into an array #
	tmp_nodes = raw_nodes.split('\n')

	# get the length of our node array #
	node_size = len( tmp_nodes )

	node_index = 0

	# loop through nmap output #
	for node in tmp_nodes:
		
		# create node dict #
		d = {}

		# check if we have a node IP line #
		if re.search("report", node):

			# remove everything up to last space #
			node = re.sub(".* ", "", node)

			# remove ( from node IP address #
			node = re.sub("\(", "", node)

			# remove ) from node IP address #
			node = re.sub("\)", "", node)

			# store IP address in node dict #
			d['ip_address'] = node

			# update node list #
			network_nodes[ node ] = d	 
			



#--------------------------#
# Get IP address from ETH0 #
#------------------------------------------#
def get_ip_network():

	# get ip information from the system #
        status, output = commands.getstatusoutput( IFCON )

	# split lines on linefeeds #
	lines = output.split('\n')

	# check if there is addr in line. ubuntu format #
	if lines[IP_LINE].find(UBUNTU_INFO) != FALSE:

		# split out ip address from other info using space # 
		ip_info = lines[IP_LINE].split(' ')

		# split ip information out using the : #
		ip_address = ip_info[IP_ADDRESS].split(':')

		# copy ip address line #
		ip = ip_address[1]

		# drop last octet and add .0 #
		ip = ip[:ip.rfind(".")] + ".0"

	# return network information #
	return ip


#-----------------------------------------------------------------------------#
# M A I N  R O U T I N E #
#-----------------------------------------------------------------------------#
def main():

	# get current IP and convert to class c network by default #
	ip_network = get_ip_network() + "/24" 

	# display network being scanned #
	print( "Scanning network: " +  ip_network )

	# scan network for devices #
	status, output = commands.getstatusoutput( NMAP + ip_network )

	# collect nodes that are on the network #
	online_nodes(output)

	# get node port information #
	node_port_info( network_nodes )

	# display nodes information # 
	print ( network_nodes )



if __name__ == '__main__':
	main()

