
import sys
import getopt
import re
import simplejson

def print_usage_text():
	print """
Usage: python convert.py [args] [sqldumpfile] > [outputfile]

Options and arguments:
	--format [xml|json]	-f [xml|json]	: specify output format, can be either JSON or XML
	--pretty-print		-p 		: indents output for eye-candy
	--help			-h		: this text
"""

pretty_print = False

try:
	optlist, args = getopt.getopt(sys.argv[1:], 'hpf:', ['help', 'pretty-print', 'format='])

except getopt.GetoptError:
	print_usage_text()
	sys.exit(2)
		
for opt, arg in optlist:
	if opt in ('-h', '--help'):
		print_usage_text()
		sys.exit()
		
	elif opt in ('-f', '--format'):
		format = arg

		if format not in ['json', 'xml']:
			print_usage_text()
			sys.exit(2)

	elif opt in ('-p', '--pretty-print'):
		pretty_print = True
			
dumpfilename = sys.argv[-1]

try:
	dumpfile = open(dumpfilename, 'r')
except IOError:
	print "ERROR: File \"" + dumpfilename + "\" was not found."
	sys.exit(3)
	
regex = re.compile(r"INSERT INTO [`'\"](?P<table>\w+)[`'\"] \((?P<columns>.+)\) VALUES\((?P<values>.+)\)")
rows = []

for line in dumpfile:
	match = regex.match(line)
	
	# non-INSERTS will be ignored
	if match:
 		table = match.group('table')

		# split parameters and remove their leading and trailing `-tags and whitespaces
		keys = map(lambda w: w.strip(" `'\""), match.group('columns').split(','))
		values = map(lambda w: w.strip(" `'\""), match.group('values').split(','))
	
		rows.append(dict(map(lambda k,v: (k,v), keys, values)))

if format == 'json':
	print simplejson.dumps(rows, indent="\t" if pretty_print else None)
		
