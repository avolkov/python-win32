**REQUIRES Active State Python
read_env.py
PURPOSE:
	Read all failed login attempts from Windows Event Log (Event ID 529) and save them to a pickle file.
USAGE:
	./read_env.py <save_target.pkl>
FORMAT:
	Pickle saves an array containing these array records, timestamp is a string and has to be converted to proper time object.
	[str(timestamp) str(u'attempted_username') int(login_type), str(src_ip), int(src_port)]
	Note login type, windows login type (value '10' - remote desktop")

read_pickle.py
PURPOSE:
	Read saved pickle and print out every item
USAGE:
	./read_pickle.py <saved_target.pkl>