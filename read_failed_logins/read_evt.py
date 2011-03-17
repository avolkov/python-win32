#!c:\Python2.7\python.exe -u

import win32evtlog
import win32evtlogutil
import string, pickle, sys, os.path


def read_faild_login_events():
	event_log = win32evtlog.OpenEventLog(None, "Security")
	flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
	login_attempt_events = []
	while(True):
		records = win32evtlog.ReadEventLog(event_log, flags,0)
		for rec in records:
			if rec.EventID == 529:
				login_attempt_events.append(rec)
		if len(records) == 0:
			break
	return login_attempt_events

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
def filter_interesting(input):
		"""
		@input: list
		@output: returns list containing [username, login type, src ip, src port]
		"""
		return [input[0], int(input[2]), input[12], int(input[13])]
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >> sys.stderr, "Usage: "+sys.argv[0]+" <pickle_save_filename>"
		sys.exit(1)
	if os.path.isfile(sys.argv[1]):
		print >> sys.stderr, "File '"+sys.argv[1]+" exists! Not overwriting."
		print >> sys.stderr, "Usage: "+sys.argv[0]+" <pickle_save_filename>"
		sys.exit(2)
	
	login_attempts = read_faild_login_events()
	output = open(sys.argv[1], 'wb')
	interesting_data = []
	for login_attempt in login_attempts:
		interesting = filter_interesting(safe_format_to_list(get_event_string(login_attempt)))
		interesting.insert(0,login_attempt.TimeGenerated.Format("%Y-%m-%d %H:%M:%S"))
		interesting_data.append(interesting)
	#print interesting
	pickle.dump(interesting_data, output, -1)
	output.close()
	