import json
import sys

def print_usage():
        print 'ERR'
        print '\nUSAGE: python input output\n'
        sys.exit()


if __name__=='__main__':
        if len(sys.argv) >= 2:
                filename = sys.argv[1]
		if len(sys.argv) == 3:
			out_file = sys.argv[2]
		else:
			out_file = 'mod_'+sys.argv[1]

                with open(filename) as f:
                        try:
                                data = json.load(f)
                        except:
                                print "Enter valid json file."
                                sys.exit()

        else:
                print_usage()



	name = raw_input("Name*: ")

	if not name:
		print "Fields marked with (*) are compulsory"
		sys.exit()

	label = raw_input("Label: ")
	desc = raw_input("Description: ")
	info = raw_input("Info: ")

	# TODO: add input options for levels, hierarchies, etc. . .

	dim_data = {}

	dim_data["name"] = name
	if label:
		dim_data["label"] = label

	if desc:
		dim_data["description"] = desc

	if info:
		dim_data["info"] = info

	data["dimensions"].append(dim_data)

	with open(out_file, 'w') as f:
		json.dump(data, f)
