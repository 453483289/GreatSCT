#!/usr/bin/env python
import os

'''
This module is used for displaying information and interactive cli.
'''

class Color:
	colorMap = {"GREEN": "\033[92m", "RED": "\033[31m", "ENDC": "\033[0m"}
	
	def setColor(self, text, color):
		try:
			text = "{0}{1}{2}".format(self.colorMap[color], text, self.colorMap["ENDC"])
		except KeyError:	#supplied nondefined color
			text = text

		return text


class Display:
	color = Color()
	clearCMD = ''	
	intro = """                     ______,------'--"-.
                    /                    \                 
                .--'      ,____,------.__/-._              
             ,-/         |                   \_            
          _/              \                    \           
        -'                 |                     \         
     _/                    |       __            |         
    /                    /       / ,------.   ,-----.      
   / /                  /      -' |        \-|       |     
    /                  |      '   |        | \       '     
     /                 |_____|    |        |  \      /     
    /           ,----./_______\_.  \       /   \    /      
    /          /      \           \_`-----/     \--'       
   / /        |                          / 0  0 / /        
    /\        |                                /  |        
     |         \                                  \        
      /          \                          ,---. |        
     / \_         \     \                  /    / /        
         \        |\____/                /     | |         
          \       |                     /     '  '         
            \     /                    /     /  /          
             \   /                    |      | |           
              /.-                     \______/ |           
         .__'    \                             |           
      /-`         \            \              /______      
  .--`             \            `------------/       `--.  
 /                  \                     /              \ 
___________________________________________________________
___________________________________________________________
                          ,-----.-----.                    
             ,------.----\ __   /__   /                    
            /  ,____//|  //_/  //,-----.------.            
           /  /   / /_/_/     / /  ____/_____/-----.       
--  --  --/  /___/_   \/__   /_/  /_/_ / /__   ___/-- -- --
         /  //_  _//\  \_/  //_\__   //    /  /            
_________\______/_/  \__|__/_,---/  //____/  /             
____________________________/______/______/_/              
___________________________________________________________
___________________________________________________________
Lopi                                               Dietrich
	A COM Scriptlet Payload Generation Tool"""


	def init(self):
		if (os.name == 'nt'):
			Display.clearCMD = 'cls'
		else:
			Display.clearCMD = 'clear'

		self.clear()
	
		print(self.intro)

	def clear(self):
		os.system(Display.clearCMD)

	def prompt(self, item, color="ENDC", term="\n"):
		item = self.color.setColor(item, color)
		print(item, end=term)

"""
	def do_EOF(self, line):
		'''
		Control + D aka EOF exits cleanly

		Args:
			self (object): the cmd.Cmd module object
			line (string): user input
		Returns:
			True (boolean)
		'''
		return True

	def do_exit(self, line):
		'''
		Type 'exit' to quit Great SCT

		Args:
			self (object): the cmd.Cmd module object
			line (string): user input
		Returns:
			True (boolean)
		'''
		return True

	def do_configs(self, line):
		'''
		Displays all the available configuration files from config directory


		Args:
			self (object): the cmd.Cmd module object
			line (string): user input
		'''

		configs = getAvailableConfigs()
		for i in configs:
			print(i)

	def do_generate(self, text):
		'''
		Generates a payload from a configuration file. i.e. generate default


		Args:
			self (object): the cmd.Cmd module object
			text (string): user input
		'''
		if text:
			config = ConfigParser()
			config.read('./config/{0}.cfg'.format(text))
			framework = getFramework(config)
			shellcode = getShellCode(config)
			stagingMethod = getStagingMethod(config)
			redirector = getRedirector(config)
			x86process = getX86Process(config)
			x64process = getX64Process(config)

			genSCT(framework, stagingMethod, redirector, x86process, x64process)
			print('Generated a Great SCT payload named payload.sct from {0} config.'.format(text))
		else:
			config = ConfigParser()
			config.read('./config/default.cfg')
			framework = getFramework(config)
			shellcode = getShellCode(config)
			stagingMethod = getStagingMethod(config)
			redirector = getRedirector(config)
			x86process = getX86Process(config)
			x64process = getX64Process(config)

			genSCT(framework, stagingMethod, redirector, x86process, x64process)
			print('Generated a Great SCT payload named payload.sct from default config.'.format(text))

	def complete_generate(self, text, line, begidx, endidx):
		'''
		Generates tab completion from available config files


		Args:
			self (object): the cmd.Cmd module object
			text (string): user input
			line (string): next line
			begidx (int): beginning of index
			endidx (int) end of index

		Returns:
			completions (list): list of string completions
		'''
		if not text:
			completions = getAvailableConfigs()
		else:
			completions = [
				f
				for f in getAvailableConfigs()
				if f.startswith(text)
			]

		return completions
"""	
