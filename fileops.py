import os
import re

def getAvailModules(profileDir):
	#takes a directory string
	#returns a list of {'name':moduleName,'filepath':moduleFilePath}s	
	profiles = [];

	for fi in os.listdir(profileDir):
		if not fi[0] == '.':
			profiles.append({'name':fi,'filepath':profileDir+fi});

	return profiles;

def loadModule(module):
	#takes a dict {'name':moduleName,'filepath':moduleFilePath}	
	#returns a dict {'name':mName,
	#		 'filepath':mFilePath,
	#		 'options:[moduleOption:defaultVal],
	#		 'allowedValues':{moduleOption:[allowedVals]}]
	#		}
	

	options = [];
	optAllowedVals = [];
	addVar = False;
	addName = False;
	addValue = False;
	addAllowed = False;
	moduleOption = '';
	defaultVal = '';
	allowedVals = [];

	path = module['filepath'];
	fi = open(path, "r");
	data = fi.read();
	data = re.split('([<]/*\w*[>])', data); 
	
	for tag in data:
		if addVar and addName and tag != '</name>':	
			moduleOption = tag;

		if addVar and addValue and tag != '</val>':
			defaultVal = tag;	
		
		if addVar and addAllowed and tag != '</opt>':
			allowedVals.append(tag);

		if not addVar and moduleOption != '':	
			options.append({moduleOption:defaultVal});
			optAllowedVals.append({moduleOption:allowedVals});
			moduleOption = '';
			defaultVal = ''
			allowedVals = [];
	
		if tag == "<var>":
			addVar = True;	
		elif tag == "</var>":
			addVar = False;	
	
		elif tag == "<name>":
			addName = True;
		elif tag == "</name>":
			addName = False;

		elif tag == "<val>":
			addValue = True;
		elif tag == "</val>":
			addValue = False;
		
		elif tag == "<opt>":
			addAllowed = True;
		elif tag == "</opt>":
			addAllowed = False;

	return({'name':module['name'], 'filepath':module['filepath'], 'options':options, 'allowedValues':optAllowedVals});	
