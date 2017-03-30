from display import *
from fileOps import *

configDir = "./config/"

display = Display()
fileOps = FileOps(configDir)



class State():
	prevState = None
	selection = None
	suppliedVal = None
	transMap = {}
	
	def transition(self, selection, suppliedVal = None):
		nextState = eval(self.transMap[selection])

		nextState.selection = selection
		nextState.suppliedVal = suppliedVal
		nextState.prevState = self.__class__.__name__
		nextState.currentState = nextState().__class__.__name__

		return(nextState().run())

	def run(self):
		print("not implemented")

class Intro(State):
	transMap = {"help": "Help", "exit": "Exit"}

	def firstRun(self):
		display.clear()
		display.init()
		display.prompt("Enter any key to begin:", ' ')
		input()
		self.run()

	def run(self):
		display.clear()
		display.prompt("Loaded modules from: {0}\n".format(fileOps.getConfigDir()))

		configs = fileOps.getConfigs()
		for i, f in enumerate(configs):
			display.prompt("\t[{0}]  {1}".format(i, f))
			self.transMap[f] = "ConfigEdit"

		display.prompt("\nPlease select a module to use, or \"help\" for more options:", ' ')

		selection = input()
		if selection.isdigit():
			selection = configs[int(selection)]

		fileOps.loadConfig(selection)
		self.transition(selection)	

class ConfigEdit(State):
	transMap = {"exit": "Menu", "menu": "Menu", "generate": "GenerationPrompt"}	
	optionsMap = {}	#will become a dict of {"0": "optionA" "1": "optionB"}
			#allows number input since the 0th actual content of config
			#will likely be DEFAULT, help or type data	
	
	def run(self):
		display.clear()
		display.prompt("Payload Editor\n")
		
		config = fileOps.getCurrentConfig()

		self.parse(config)	

		display.prompt("Select an option to edit, generate, or exit:", " ")

		selection = input()
		
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
				display.prompt("\t[{0}] {1}:\t{2}".format(optionNum, section_name, section["var"]))
				self.transMap[section_name] = "OptionEdit"
				self.optionsMap[chr(optionNum+48)] = section_name
				optionNum += 1
			
			section = config[section_name]
		display.prompt("")

class OptionEdit(State):
	transMap = {"ConfigEdit": "ConfigEdit"}

	validParams = []
	
	def run(self):
		config = fileOps.getCurrentConfig()
		option = config[self.selection]
		self.validParams = self.parseOptions(option)

		if self.suppliedVal == None:
			display.prompt("Enter a value for [{0}]: (Valid options are: {1}):".format(self.selection, self.validParams), " ")
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
		template =  fileOps.loadTemplate(config)
		

class Help(State):
	transMap = {"Help": "Help", "Intro": "Intro", "ConfigEdit": "ConfigEdit"}
	
	def run(self):
		display.clear()
			
		if self.prevState == "Intro":
			display.prompt("Help from Intro")

		input()
		self.transition(self.prevState)


	
		

def main():
	intro = Intro()
	intro.firstRun()
	


if __name__ == '__main__':
	#try:
		main()

	#except
