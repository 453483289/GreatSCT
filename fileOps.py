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
		FileOps.selectedConfig = ConfigParser()
		FileOps.selectedConfig.optionxform = str #disable configparser convert data to lowercase
		FileOps.selectedConfig.read("{0}{1}".format(FileOps.configDir, configName))
		
		return(FileOps.selectedConfig)

	def updateCurrentConfig(self, option, value):
		FileOps.selectedConfig[option]["var"] = value	

	def getCurrentConfig(self):
		return(FileOps.selectedConfig)

	def loadTemplate(self, config):
		template = ConfigParser(interpolation = ExtendedInterpolation())
		template.optionxform = str
		template.read("./template/SCT/regsvr32.template")
		self.genFromTemplate(template)
		
	def genFromTemplate(self, template):

		framework = ''
		domain = ''
		port = ''
		params = []

		for config_section in FileOps.selectedConfig:
			if config_section != "DEFAULT" and config_section != "Type":
				print(config_section)
				var = FileOps.selectedConfig[config_section]["var"]
				params.append([config_section, var])
			
			if config_section == "Framework":
				framework = FileOps.selectedConfig[config_section]["var"]
			elif config_section == "Redirector Domain":
				domain= FileOps.selectedConfig[config_section]["var"]
			elif config_section == "Redirector Port":
				port= FileOps.selectedConfig[config_section]["var"]


		generator = Generator()
		shellcode = generator.genShellcode(framework, domain, port)
	
		for template_section in template:
			section = template[template_section]

			if template_section == "ShellCode":
				section["value"] = shellcode
			else:
				for param in params:
					if template_section == param[0]:
						section["value"] = param[1]
		
		shellcode = template.get("ShellCode", "value")	
		payload = template.get("Template", "data")
		print(payload)
		
			
					
					
			
					
		#generator = Generator()
		#generator.genShellcode("metasploit", "test.com", "9999")

	"""	for section_name in template:
			print(section_name)
			section = template[section_name]
			for param in section:
				if param == "generator":
					print(section["generator"])
					section["value"] = eval(section["generator"])
					print(section["value"])"""
