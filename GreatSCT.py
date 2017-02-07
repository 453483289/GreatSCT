from display import *
import fileops

def main():

	profiles = fileops.getAvailModules("./Profiles/");
	activeModule = '';

	display = Display();
	input();
	entry = '';
	while entry != 'quit':
		if entry == 'profile' or activeModule == '':
			display.showOptions(profiles);

			entry = input();
			if entry.isdigit():
				if int(entry) < len(profiles):
					activeModule = fileops.loadModule(profiles[int(entry)]);
					entry = 'module';
				else:
					display.error("Not a valid profile");
			else:
				display.error("Please enter an integer");
		
		elif entry == 'help':
			display.help();
			entry = input();


		if activeModule != '' and entry == 'module': #shortcricuts so module entry won't work without active module	
			while entry != 'back' and entry != 'profile' and entry != 'help' and entry != 'quit': #TODO: Make an struct of menu options
				entry = '';
				display.showOptions(activeModule['options']);
				display.show('Active Module: {}'.format(activeModule['name']));
				entry = input();
				if entry.isdigit():
					if int(entry) < len(activeModule['options']):
						display.show("\nEdit Option {0}:  {1}, Allowed Values: {2}".format(entry, 
														    activeModule['options'][int(entry)], 
														    activeModule['allowedValues'][int(entry)]));

						activeModule['options'][int(entry)][list((activeModule['options'][int(entry)]).keys())[0]] = input() #FUCK YOU SLEEP, FUCK YOU EFFICIENCY, IT WORKS SO I WIN
				


if __name__ == "__main__":
	main();
