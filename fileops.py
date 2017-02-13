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

def export(template):
	#takes a tokenized list
	#concats together and writes to file
	
	fi = open('./test', 'w');

	for tag in template:
		fi.write(tag);

	fi.close();			

def loadModule(module):
	#takes a dict {'name':moduleName,'filepath':moduleFilePath}	
	#returns a dict {'name':mName,
	#		 'filepath':mFilePath,
	#		 'options:[moduleOption:defaultVal],
	#		 'allowedValues':{moduleOption:[(allowedVal, valAlias]}]
	#		}
	

	options = [];
	optAllowedVals = [];
	addVar = False;
	addName = False;
	addValue = False;
	addAllowed = False;
	addAlias = False;
	addTemplate = False
	moduleOption = '';
	defaultVal = '';
	allowedVals = [];
	template = [];

	path = module['filepath'];
	fi = open(path, "r");
	data = fi.read();
	data = re.split('([<]/*\w*[>])', data); 
	
	for tag in data:

		if addVar and addName and tag != '</name>':	
			moduleOption = tag;

		if addVar and addValue and tag != '</val>':
			defaultVal = tag;	
		
		if addVar and addAllowed and not addAlias and tag != '</opt>':
			allowedVal = tag;	
	
		if addVar and addAlias and tag != '</alias>':
			allowedVals.append((allowedVal, tag));

		if not addVar and moduleOption != '':	
			options.append({moduleOption:defaultVal});
			optAllowedVals.append({moduleOption:allowedVals});
			moduleOption = '';
			defaultVal = ''
			allowedVals = [];

		if addTemplate and tag != '</template>':
			template.append(tag);
		
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

		elif tag == "<alias>":
			addAlias = True;
		elif tag == "</alias>":
			addAlias = False;
		
		elif tag == "<template>":
			addTemplate = True;
			addVar = False;	
			addName = False;
			addValue = False;
			addAllowed = False;
		elif tag == "</template>":
			addTemplate = False;

	fi.close();
	return({'name':module['name'], 'filepath':module['filepath'], 'options':options, 'allowedValues':optAllowedVals, 'template':template});	
