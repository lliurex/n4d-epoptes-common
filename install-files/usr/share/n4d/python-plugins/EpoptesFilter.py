import subprocess
import os
import n4d.responses

class EpoptesFilter:
	
	def __init__(self):
		
		self.allowed_groups=[0,1000,10001,10003]
		self.del_epoptes_from_iptables()
		self.set_drop_epoptes()
		self.set_accept_allowed_groups()
		
		
	#def init

	def del_epoptes_from_iptables(self):
		
		p=subprocess.Popen(["iptables-save"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output=p.communicate()[0]

		if type(output) is bytes:
			output=output.decode()
			
		output=output.split("\n")
		
		ret=[]
		
		for item in output:
			if "--dport 10000" in item and "OUTPUT" in item:
				ret.append("iptables " + item.replace("-A","-D"))
		
		
		for item in ret:
			#print(item)
			os.system(item)
		
		
	#def del_epoptes_from_iptables

	def set_drop_epoptes(self):
	
		cmd="iptables -A OUTPUT -p tcp --dport 10000 -j DROP"
		os.system(cmd)
		
	#def set_drop_epoptes
	
	def set_accept_allowed_groups(self):
		
		for item in self.allowed_groups:
			
			cmd="iptables -I OUTPUT -m owner --gid-owner %s --suppl-groups -p tcp --dport 10000 -j ACCEPT"%item
			os.system(cmd)
	
		#Old n4d:return True
		return n4d.responses.build_successful_call_response()
		
	#def set_accept_allowed_groups
	
#class EpoptesFilter



