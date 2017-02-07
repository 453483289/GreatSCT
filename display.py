import os

class Display:
	clearSc = '';

	def __init__(self):
		if(os.name == 'nt'):
			self.clearSc = 'cls';
		else:
			self.clearSc = 'clear';
	

	def showOptions(self, profileDict):
		self.clear();	
		print('Please select an option');

		i = 0;
		for opt in profileDict:
			print('{0}: {1} '.format(i, opt));
			i = i+1;

	def help(self):
		self.clear();
		print("Help Menu");

	def show(self, info):
		print(info);
	
	def error(self, error):
		print(error);

	def clear(self):
		os.system(self.clearSc);
			
