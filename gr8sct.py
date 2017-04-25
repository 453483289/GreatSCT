from display import *
from fileOps import *
from completer import *

import readline
import threading
import time

configDir = "./config/"

display = Display()
fileOps = FileOps(configDir)
completer = Completer()

class State():
	prevState = None
	currentState = None
	selection = None
	suppliedVal = None
	transMap = {}
	
	def transition(self, selection, suppliedVal = None):
	
		try:
			nextState = eval(self.transMap[selection])
		except KeyError:
			nextState = eval(self.currentState)

		nextState.selection = selection
		nextState.suppliedVal = suppliedVal
		nextState.prevState = self.__class__.__name__
		nextState.currentState = nextState().__class__.__name__

		return(nextState().run())

	def run(self):
		readline.set_completer(completer.check)
		readline.set_completer_delims("")
		readline.parse_and_bind("tab: complete")


class Intro(State):
	transMap = {"help": "Help", "exit": "Exit"}

	def firstRun(self):
		self.currentState = "Intro" #seed currentState to return here if invalid selection is set, this is auto preformed in transistion() for future states 
		display.clear()
		display.init()
		display.prompt("{0}Enter any key to begin, \"help\", or \"exit\" at any time: {1}".format(display.GREEN, display.ENDC), '')
		input()
		self.run()

	def run(self):
		super().run()

		display.clear()
		display.prompt("Loaded modules from: {0}\n".format(fileOps.getConfigDir()))

		configs = fileOps.getConfigs()
		for i, f in enumerate(configs):
			display.prompt("{0}\t[{1}]{2}  ".format(display.GREEN, i, display.ENDC), '')
			display.prompt(f)
			self.transMap[f] = "ConfigEdit"

		completer.setCommands(list(self.transMap.keys()))

		display.prompt("\nPlease select a module to use: ", '')

		selection = input()
		if selection.isdigit():
			selection = configs[int(selection)]

		fileOps.loadConfig(selection)
		self.transition(selection)


class ConfigEdit(State):
	transMap = {"exit": "Exit", "menu": "Intro", "help": "Help", "generate": "GenerationPrompt"}	
	optionsMap = {}	#will become a dict of {"0": "optionA" "1": "optionB"}
			#allows number input since the 0th actual content of config
			#will likely be DEFAULT, help or type data	
	
	def run(self):
		super().run()

		display.clear()
		display.prompt("Payload Editor\n")
		
		config = fileOps.getCurrentConfig()

		completer.setCommands(list(self.transMap.keys()))
		self.parse(config)
		display.prompt("Select an option to edit, {0}generate{1}, or {2}exit{3}: ".format(display.GREEN, display.ENDC, display.GREEN, display.ENDC), '')

		selection = input()
	
		#Not sure if these checks are needed	
		if selection.startswith("set "):
			option = selection.split(" ")[1]
			self.suppliedVal = selection.split(option+" ", 1)[-1]
	
			if self.suppliedVal == "":
				selection = "invalid"

			selection = option
		
		if selection.isdigit():
			try:
				selection = self.optionsMap[selection]
			except KeyError:
				selection = "invalid"

		self.transition(selection, self.suppliedVal)
			

	def parse(self, config):

		optionNum = 0
		for section_name in config:

			if section_name == "DEFAULT":
				continue

			section = config[section_name]
			if section_name == "Type":
				display.prompt("Selected Payload: {0}\n".format(section["name"]))

			else:
				numTabs = 1
				if len(section_name) < 12: numTabs = 2

				display.prompt("{0}\t[{1}] {2}:{3}{4}{5}".format(display.GREEN, optionNum, section_name, display.ENDC, '\t'*numTabs, section["var"]))
				
				self.transMap[section_name] = "OptionEdit"
				self.optionsMap[chr(optionNum+48)] = section_name
				completer.addCommand(section_name)
				completer.addCommand("set " + section_name)
				completer.addCommand("set " + chr(optionNum+48))
				optionNum += 1
			
			section = config[section_name]
		display.prompt("")


class OptionEdit(State):
	transMap = {"exit": "Exit", "ConfigEdit": "ConfigEdit"}

	validParams = []
	
	def run(self):
		config = fileOps.getCurrentConfig()
		option = config[self.selection]
		self.validParams = self.parseOptions(option)

		if self.suppliedVal == None:
			display.prompt("Enter a value for [{0}]: (Valid options are: [".format(self.selection), '')
			for param in self.validParams:
				display.prompt("\'{0}{1}{2}\'".format(display.GREEN, param, display.ENDC), '')
				
				if param != self.validParams[-1]:
					display.prompt(', ', '')
			display.prompt("]): ", '')			

			self.suppliedVal = input()

		if self.suppliedVal in self.validParams or "allowWilds" in self.validParams:
			fileOps.updateCurrentConfig(self.selection, self.suppliedVal)

		self.transition(self.prevState)

		
		#TODO: Move valid param checking to fileops	
	def parseOptions(self, option):
		validParams = []
	
		optionString = 	""
		for validParam in option:

			if validParam == "var":
				continue

			validParams.append(validParam)

		return validParams				



class GenerationPrompt(State):

	def run(self):
		config = fileOps.getCurrentConfig()
		t1 = threading.Thread(target = fileOps.generate, args = [config])

		t1.start()

		i = 1
		end = ['/', '-', '\\', '|']
		while t1.is_alive():
			display.prompt("Generating: "+"="*i+end[i%4], '\r')
			time.sleep(0.3)
			i = i+1

		t1.join()
		display.prompt("{0}Generating: 8{1}D{2}\n".format(display.GREEN, '='*i, display.ENDC))

		info = config["Type"]["runInfo"]
		display.prompt("{0}Execute with: {1}".format(display.GREEN, display.ENDC), '')
		display.prompt(info, '\n\n')
		

class Help(State):
	transMap = {"Help": "Help", "Intro": "Intro", "ConfigEdit": "ConfigEdit", "GenerationPrompt": "GenerationPrompt"}
	
	def run(self):
		display.clear()
			
		if self.prevState == "Intro":
			display.prompt("Select a payload module by index ['#'] or name\n\tValid options are:\n")
		
			#TODO this is used in multiple states, move it to super	
			configs = fileOps.getConfigs()
			for i, f in enumerate(configs):
				conf = fileOps.loadConfig(f)
				helpStr = ''
				numTabs = 1
				if len(f) < 19: numTabs = 2

				try:
					helpStr = conf.get("Type", "name")	
				except Exception:
					helpStr = ''

				display.prompt("{0}\t[{1}]  {2}{3}{4}{5}".format(display.GREEN, i, f, display.ENDC, '\t'*numTabs, helpStr))

			display.prompt("\nEnter any key to return to module selection")

		elif self.prevState == "ConfigEdit":
			display.prompt("Help from Config Editor")

		elif self.prevState == "GenerationPrompt":
			display.prompt("Help from Generation")

		elif self.prevState == "Help":
			display.prompt("Help from Help")

		input()
		self.transition(self.prevState)



class Exit(State):

	def run(self):
		exit(0)
	

def main():
	intro = Intro()
	intro.firstRun()
	


if __name__ == '__main__':
	try:
		main()

	except KeyboardInterrupt:
		print('')
		exit(0)
	
	except EOFError:
		print('')
		exit(0)
