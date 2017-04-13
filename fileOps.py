import os
from configparser import ConfigParser, ExtendedInterpolation
from generator import Generator

class FileOps():
	configDir = ''
	selectedConfig = None

	def __init__(self, configDir):
		FileOps.configDir = configDir

	def getConfigs(self):
		fileList = []

		#http://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python
		for base, dirs, files in os.walk(FileOps.configDir):
			path = base.split(FileOps.configDir)[-1]
			for f in files:
				filePath = "{0}/{1}".format(path, f)
				fileList.append(filePath)
		return(fileList)

	def getConfigDir(self):
		return(FileOps.configDir)

	def loadConfig(self, configName):
		FileOps.selectedConfig = ConfigParser(interpolation = ExtendedInterpolation())
		FileOps.selectedConfig.optionxform = str #disable configparser convert data to lowercase
		FileOps.selectedConfig.read("{0}{1}".format(FileOps.configDir, configName))
		
		return(FileOps.selectedConfig)

	def updateCurrentConfig(self, option, value):
		FileOps.selectedConfig[option]["var"] = value	

	def getCurrentConfig(self):
		return(FileOps.selectedConfig)

	def generate(self, config):
		template = ConfigParser(interpolation = ExtendedInterpolation())
		template.optionxform = str
		template.read(FileOps.selectedConfig["Type"]["template"])

		return (self.genFromTemplate(template))
		
	def genFromTemplate(self, template):

		framework = ''
		domain = ''
		port = ''
		params = []
		outfile = "output.gr8sct"
		runInfo = ''

		for config_section in FileOps.selectedConfig:
			if config_section != "DEFAULT" and config_section != "Type":
				var = FileOps.selectedConfig[config_section]["var"]
				params.append([config_section, var])

			if config_section == "Type":
				runInfo = FileOps.selectedConfig[config_section]["runInfo"]

			if config_section == "Output":
				outfile = FileOps.selectedConfig[config_section]["var"]		
	
			if config_section == "Framework":
				framework = FileOps.selectedConfig[config_section]["var"]
			elif config_section == "Redirector Domain":
				domain = FileOps.selectedConfig[config_section]["var"]
			elif config_section == "Redirector Port":
				port = FileOps.selectedConfig[config_section]["var"]


		generator = Generator()
		shellcodex64 = generator.genShellcode(domain, port, "x64")
		shellcodex86 = generator.genShellcode(domain, port, "x86")
		
		for template_section in template:
			section = template[template_section]
		
			if template_section == "ShellCodex64":
				section["value"] = shellcodex64
			
			elif template_section == "ShellCodex86" or template_section == "ShellCode":
				section["value"] = shellcodex86

			else:
				for param in params:
					if template_section == param[0]:
						section["value"] = param[1]
		
		payload = template.get("Template", "data")

		f = open(outfile, "w+")
		f.write(payload)

		return runInfo
		
			
					
					
			
					

