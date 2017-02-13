from display import *
import fileops

display = Display();

def main():

	profiles = fileops.getAvailModules("./Profiles/");
	activeModule = None;
	selectedOption = None;
	
	entry = '';
	while entry != 'quit':
		#BUG:!: when editing an option if the value is another valid option it sets the value correctly then auto returns to edit the option with that value, it should return to showModule()
			#e.g. setting option #3 PortNum = 5 sets the port option to 5 then immediately takes you to edit option #5 Process_x64, it should return you to the menu
		entry = input();
		if entry == 'profile' or activeModule == None:
			activeModule = profileSelection(profiles, entry);
			if activeModule != None:
				entry = 'module';	
	
		if entry == 'help':
			showHelp();

		if activeModule != None and entry == 'generate':
			generate(activeModule);
		
		if activeModule != None and selectedOption != None:
			editOption(activeModule, selectedOption, entry);		
	
		if activeModule != None:
			selectedOption = showModule(activeModule, entry); 				

				

def profileSelection(profiles, entry):
	display.showOptions(profiles);

	selectedModule = None;
	if entry.isdigit():
		if int(entry) < len(profiles):
			selectedModule = fileops.loadModule(profiles[int(entry)]); #TODO: add try catch
		else:
			display.error("Not a valid profile");
	else:
		display.error("Please enter an integer");

	return(selectedModule);

def showHelp():
	display.help();

def showModule(activeModule, entry):
	display.showOptions(activeModule['options']);
	display.show('Active Module: {}'.format(activeModule['name']));
	
	optionSelected = None;
	if entry.isdigit():
		if int(entry) < len(activeModule['options']):
			display.show("\nEdit Option {0}:  {1}, Allowed Values: {2}".format(entry, 
											    activeModule['options'][int(entry)], 
											    activeModule['allowedValues'][int(entry)]));
			optionSelected = entry;

	return(optionSelected);			




def editOption(activeModule, selectedOption, entry):
	#behold the worlds most efficient, most easily parseable function
	#2/13/2016 it just keeps getting better

	options = list(activeModule['allowedValues'][int(selectedOption)].values())[0];
	option_list = [x[0] for x in options];
	if entry in option_list or '*' in option_list:	
		activeModule['options'][int(selectedOption)][list((activeModule['options'][int(selectedOption)]).keys())[0]] = entry #FUCK YOU SLEEP, FUCK YOU EFFICIENCY, IT WORKS SO I WIN
	else:
		display.error("Entry Invalid for this option");



def generate(activeModule):
	#Just when I thought it couldn't get better I bested myself
	#This one's now O(x^3) for those keeping score (profile storage format may need a slight rework)
	for pair in activeModule['options']:
		option = list(pair.keys())[0];
		value = list(pair.values())[0];
		alias = None;	
		for x in activeModule['allowedValues']:
			if option in x.keys():
				for val in x.values():
					for i in val:
						if '<_val_>' in i[1]:	
							alias = '<_val_>';
						elif value == i[0] and i[1] != '':
							alias = i[1];

		for i, variable in enumerate(activeModule['template']): #TODO: O(x^2) == :(
			if '<_'+option+'_>' == variable:
				if alias == '<_val_>':
					alias = value
				activeModule['template'][i] = alias;


	fileops.export(activeModule['template']);

if __name__ == "__main__":
	main();
