# -*- coding: utf-8 -*-
 
import os.path
import sys
import getopt
import time
from requests import session
import webbrowser
 
loginFormLink      = "https://knowledgepit.fedcsis.org/login/index.php"
submissionFormLink = "https://knowledgepit.fedcsis.org/mod/challenge/view.php?id=1014"
 
def parse_arguments():
    userName = ''
    password = ''
    fileName = ''
 
    try:
        myopts, args = getopt.getopt(sys.argv[1:],"u:p:f:", ['username=', 'password=', 'file='])
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage: %s -u username -p password -f fileName" % sys.argv[0])
        sys.exit(2)
 
    for o, a in myopts:
        if o in ('-u', '--username'):
            userName = a
        elif o in ('-p', '--password'):
            password = a
        elif o in ('-f', '--file'):
            fileName = a
 
    if not userName or not password or not fileName:
        print("Usage: %s -u username -p password -f fileName" % sys.argv[0])
        exit(2)
 
    print 'USER_NAME :', userName
    print 'PASSWORD  :', '*' * len(password)
    print 'FILE_NAME :', fileName
 
    return [userName, password, fileName]
 
########################################
#              POCZĄTEK                #
########################################
 
# Parse input arguments
userName, password, submissionFileName = parse_arguments()
 
loginData = {
        'username': userName,    # user name text input
        'password': password,    # password input
        'submit'  : 'Login',     # submit form button
        'rememberusername' : 0   # remember logging checkbox
}
 
submissionData = {
        'submissionname' : 'random_forest ' + str(time.time()),       # submission name text input
        'notes'          : 'max_iterations= 15,max_depth=51',       # submission description textarea
        'chooseFinal'    : 1,        # choosing the best score select input
        'submit1'        : 'Submit', # submit form button
}
 
# Open session
c = session()
print 'Created session'
 
# Login to the knowledgepit.fedcsis.org
print 'Logging in as an user: %s ...' % (loginData['username'])
 
start = time.time()
loginResponse = c.post(
        url  = loginFormLink,
        data = loginData,
        allow_redirects = True)
print 'Operation took %s seconds' % (time.time() - start)
 
# Check the login response
if loginResponse.status_code == 200:
        print 'Successfully logged in'
else:
        print '### Error ### with logging in'
        exit(1)
 
# Send submission with submission file
print 'Sending submission file: %s ...' % (submissionFileName)
 
start = time.time()
with open(submissionFileName, 'rb') as submissionFile:
        submissionResponse = c.post(
                url   = submissionFormLink,
                data  = submissionData,
                files = {'challengefile' : (os.path.basename(submissionFileName), submissionFile)})
print 'Operation took %s seconds' % (time.time() - start)
 
# Check the send submission response
if submissionResponse.status_code == 200:
        print 'Successfully sent submission file'
else:
        print '### Error ### with sending submission file'
        exit(1)
 
# Save response (HTML page) for checking for errors
with open('submissionTempOutput.html', 'w') as logFile:
        logFile.write(submissionResponse.text)
 
# Open browser with the submission send confirmation
#webbrowser.open_new_tab(logFile.name)
 
# Close session
c.close()
print 'Closed session'