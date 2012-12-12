import os
from subprocess import Popen, PIPE 
from urlparse import urlparse

# Set Default Browser
browser = "WebKit"
# browser = "Safari"

# Get url address from safari / webkit
cmd = "/usr/bin/osascript -e 'tell application \"%s\"' -e 'get URL of current tab of window 1' -e 'end tell'" % browser
pipe = Popen(cmd, shell=True, stdout=PIPE).stdout
url = pipe.readlines()[0].rstrip('\n')

# Get index of current tab
cmd = "/usr/bin/osascript -e 'tell application \"%s\"' -e 'get index of current tab of window 1' -e 'end tell'" % browser
pipe = Popen(cmd, shell=True, stdout=PIPE).stdout
tindex = pipe.readlines()[0].rstrip('\n')

# Parse URL
o = urlparse(url)
string = ''
if 'twitter' in o.netloc:
	if o.path != '/':
		if 'status' in o.path:
			# Open specific tweet in tweetbot
			string = "tweetbot:/%s" % o.path
		else:
			# Open user profile in tweetbot
			string = "tweetbot:///user_profile/%s" % o.path
else:
	print "Not a Twitter URL..."

# Open Twitter URL in Tweetbot
if string != '':
	cmdList = []
	# Send to tweetbot, close blank safari window, switch back to original tab
	cmdList.append("""osascript -e 'tell application \"%s\" to open location \"%s\"'""" % (browser, string))
	cmdList.append("""osascript -e 'tell application \"%s\" to close current tab of window 1'""" % browser)
	cmdList.append("""osascript -e 'tell front window of application \"%s\" to set current tab to tab %s'""" % (browser, tindex))

	# Execute Commands
	for cmd in cmdList:
		os.system(cmd)

else:
	print "Exiting"