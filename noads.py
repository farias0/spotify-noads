import colored
from colored import stylize
import argparse
import sys

HOSTS_PATH = '/etc/hosts'
STRING_BEGIN = "SPOTIFY - ADS - BEGIN"
STRING_END = "SPOTIFY - ADS - END"
STRING_UPDATES = "BLOCK UPDATES"

def checkConflits(args):
	if ((args.disable_ads and args.enable_ads) or 
	(args.enable_updates and args.disable_updates) or 
	((args.disable_updates or args.disable_ads) and args.off) or 
	((args.enable_updates or args.enable_ads) and args.on)):

		error('Conflicting arguments')

def disable(lines, function, line):
	if function == 'ads':
		stop_at = STRING_UPDATES
	elif function == 'updates':
		stop_at = STRING_END

	print(stylize('disabling %s from line %d:' % (function, line), colored.fg('blue')))

	while (stop_at in lines[line]) == False:
		if lines[line].startswith('#'):
			lines[line] = lines[line][1:]
		else:
			if lines[line] != '\n':
				print('line %d isn\'t commented, skipping...' % line)

		line = line+1

	print(stylize('%s disabled' % function, colored.fg('green')))

def enable(lines, function, line):
	if function == 'ads':
		stop_at = STRING_UPDATES
	elif function == 'updates':
		stop_at = STRING_END

	print(stylize('enabling %s from line %d:' % (function, line), colored.fg('blue')))

	while (stop_at in lines[line]) == False:
		if lines[line].startswith('#'):
			if lines[line] != '\n':
				print('line %d already commented, skipping...' % line)
		else:
			lines[line] = '#' + (lines[line])
			
		line = line+1

	print(stylize('%s enabled\n' % function, colored.fg('blue')))

def error(msg, exit_code=1):
    sys.stderr.write(stylize("Error: %s\n" % msg, colored.fg('red')))
    exit(exit_code)

def main():
	parser = argparse.ArgumentParser(description="Manages Spotify ads IPs on /etc/hosts")
	parser.add_argument('--disable_ads', action='store_true',
						help="disable ads IPs")
	parser.add_argument('--enable_ads', action='store_true',
						help="enables ads IPs")
	parser.add_argument('--disable_updates', action='store_true',
						help="disable updates IPs")
	parser.add_argument('--enable_updates', action='store_true',
						help="enable updates IPs")
	parser.add_argument('--on', action="store_true",
						help="disable both ads and updates")
	parser.add_argument('--off', action="store_true",
						help="enable both ads and updates")
	args = parser.parse_args()

	print(stylize('DISABLE ADS FOR SPOTIFY', (colored.fg('white'), colored.bg('green'))))
	print('')

	checkConflits(args)

	with open(HOSTS_PATH, 'r+') as file:

		#check ads block
		lines = file.readlines()
		for i in range (0, len(lines)):
			if STRING_BEGIN in lines[i]:
				break

		#if ads ips are disabled
		if (lines[i+1].startswith('#')):
			if len(sys.argv)==1:
				print(stylize('ads enabled', colored.fg('red')))
			elif args.disable_ads or args.on:
				disable(lines, 'ads', i+1)
			elif args.enable_ads or args.off:
				print(stylize('ads already enabled', colored.fg('blue')))
		else:
			if len(sys.argv)==1:
				print(stylize('ads disabled', colored.fg('green')))
			elif args.enable_ads or args.off:
				enable(lines, 'ads', i+1)
			elif args.disable_ads or args.on:
				print(stylize('ads already disabled', colored.fg('blue')))

		#check update block
		for j in range(i, len(lines)):
			if STRING_UPDATES in lines[j]:
				break

		#if updates ips are disabled
		if (lines[j+1].startswith('#')):
			if len(sys.argv)==1:
				print(stylize('updates enabled', colored.fg('red')))
			elif args.disable_updates or args.on:
				disable(lines, 'updates', j+1)
			elif args.enable_updates or args.off:
				print(stylize('updates already enabled', colored.fg('blue')))	
		else:
			if len(sys.argv)==1:
				print(stylize('updates disabled', colored.fg('green')))
			elif args.enable_updates or args.off:
				enable(lines, 'updates', j+1)
			elif args.disable_updates or args.on:
				print(stylize('updates already disabled', colored.fg('blue')))

		if len(sys.argv)>1:
			file.seek(0)
			file.truncate(0)
			file.writelines(lines)

if __name__ == "__main__":
	main()