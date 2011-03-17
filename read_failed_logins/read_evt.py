#!c:\Python2.7\python.exe -u

import win32evtlog
import win32evtlogutil
import string, pickle, sys, os.path

def read_login_events(eventid, log_source):
	event_log = win32evtlog.OpenEventLog(None, log_source)
	flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
	login_attempt_events = []
	while(True):
		records = win32evtlog.ReadEventLog(event_log, flags,0)
		for rec in records:
			if rec.EventID == eventid:
				login_attempt_events.append(rec)
		if len(records) == 0:
			break
	return login_attempt_events

def read_faild_login_events():
	def filter_interesting(input):
		"""
		@input: list
		@output: returns list containing [username, login type, src ip, src port]
		"""
		return [input[0], int(input[2]), input[12], int(input[13])]

	interesting_data = []
	for item in read_login_events(529,"Security"):
		interesting_data.append(format_data(item, filter_interesting))
	return interesting_data
def read_successful_login_events():
	def filter_interesting(input):
		return input
	interesting_data = []
	for item in read_login_events(528,"Security"):
		interesting_data.append(format_data(item, filter_interesting))
	return interesting_data
def read_logoff_events():
	def filter_interesting(input):
		return input
	interesting_data = []
	for item in read_login_events(551,"Security"):
		interesting_data.append(format_data(item, filter_interesting))
	return interesting_data

def read_explicit_logon_events():
	def filter_interesting(input):
		"""
		@output ['username', 'target username',  'target server', 'source ip', 'source port']
		"""
		return [input[0], input[5], input[9], input[11], input[12]]
	interesting_data = []
	for item in read_login_events(552,"Security"):
		interesting_data.append(format_data(item, filter_interesting))
	return interesting_data	

def format_data(event_log_item, outer_filter):
	interesting = outer_filter(safe_format_to_list(get_event_string(event_log_item)))
	interesting.insert(0,event_log_item.TimeGenerated.Format("%Y-%m-%d %H:%M:%S"))
	return interesting

def get_event_string(event):
		"""
		@event: PyEventLogRecord
		"""
		return str(win32evtlogutil.SafeFormatMessage(event))
def safe_format_to_list(msg):
		"""
		@msg: str
		"""
		try:
			return [string.strip(x, "\"'()<> .,") for x in (msg.split(":")[1]).split(",")]
		except IndexError:
			return []
def usage(arg):
	if len(arg) > 0:
		print >> sys.stderr, arg
	print >> sys.stderr, "Usage: "+sys.argv[0]+" <pickle_save_filename> [failed_login, ok_login, exp_login, logoff] "
if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage()
		sys.exit(1)
	if os.path.isfile(sys.argv[1]):
		usage("File '"+sys.argv[1]+" exists! Not overwriting.")
		sys.exit(2)
	
	
	if sys.argv[2] == "failed_login":
		interesting_data =  read_faild_login_events()
	elif sys.argv[2] == "ok_login":
		interesting_data = read_successful_login_events()
	elif sys.argv[2] == "exp_login":
		interesting_data = read_explicit_logon_events()
	elif sys.argv[2] == "logoff":
		interesting_data = read_logoff_events()
	else:
		usage("Unknown option '"+sys.argv[2]+"'")
		sys.exit(3)
	output = open(sys.argv[1], 'wb')
	#print interesting
	pickle.dump(interesting_data, output, -1)
	output.close()
	