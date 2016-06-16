import json
import sys

def print_usage():
	print 'ERR'
	print '\nUSAGE: python filename.json\n'
	sys.exit()


if __name__=='__main__':
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		with open(filename) as f:
			try:
				data = json.load(f)
			except:
				print "Enter valid json file."
				sys.exit()

	else:
		print_usage()

	for dim in data["dimensions"]:
		print dim["name"]

	key = raw_input("Enter dimension name from the list to be discarded: ")

	if not key:
		print "Please enter a key."
		sys.exit()

	for i in range(len(data["dimensions"])):
		if data["dimensions"][i]["name"] == key:
			del data["dimensions"][i]
			print "Successfully deleted"

			with open(filename,'w') as f:
				json.dump(data, f)			

			sys.exit()

	print "Dimension not found. Please try again with a valid dimension name."

	
