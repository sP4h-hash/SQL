#!/usr/bin/python

import sys,  re,  urllib,  urllib2,  string
from urllib2 import Request,  urlopen,  URLError,  HTTPError
from urlparse import urlparse

    
# We test if the url is reachable
def URL_TESTING(Site_URL):
    # Define User-Agent variable
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)"
    
    # Adding the User-Agent to the HTTP request
    Get_URL = urllib2.Request(Site_URL)
    Get_URL.add_header("User-Agent",  user_agent)
    
    # Now let's do the HTTP request
    print "[i] Checking if a connection can be established..."
    try:
        http_URL_test = urllib2.urlopen(Get_URL)
    except HTTPError,  e:
        print "[!] The connection couldn't be established."
        print "[!] Error code: ",  e.code
        print "[!] Exiting now!"
        print ""
        print ""
        sys.exit(1)
    except URLError,  e:
        print "[!] The connection couldn't be established."
        print "[!] Reason: ",  e.reason
        print "[!] Exiting now!"
        print ""
        print ""
        sys.exit(1)
    else:
        print "[i] HaHaa XD, Connected to target! URL seems to be valid."
    return

# Scan the provided URL for a SQL injection vulnerability
def URL_SCANNING(Site_URL):
    # I defined some variables needed for detecting MySQL errors in the source code
    SQL_ERR_1 = "You have an error in your SQL syntax"
    SQL_ERR_2 = "supplied argument is not a valid MySQL result resource"
    SQL_ERR_3 = "check the manual that corresponds to your MySQL"
    PARM_EQ = "="
    PARM_SGN_1 = "?"
    PARM_SGN_2 = "&"
    TRIGGER_ERR_1 = "'"
    TRIGGER_ERR_2 = "-1"
    
    # I defined dict which will list all vulnerable parameters
    VULN_PARAM = {}
    
    # I defined the variables needed to craft URLs for exploitation (if there is at least one vulnerability)
    exploit_urls = list()
    
    # I defined User-Agent variable
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)"
    
    # Adding the User-Agent to the HTTP request (via GET) 
    Get_URL = urllib2.Request(Site_URL)
    Get_URL.add_header("User-Agent",  user_agent)
    
    # Starting the request
    try:
        CALL_HTTP = urllib2.urlopen(Get_URL)
    except HTTPError,  e:
        print "[!] The connection could not be established."
        print "[!] Error code: ",  e.code
        print "[!] Exiting now!"
        print ""
        print ""
        sys.exit(1)
    except URLError,  e:
        print "[!] The connection could not be established."
        print "[!] Reason: ",  e.reason
        print "[!] Exiting now!"
        print ""
        print ""
        sys.exit(1)  
    
    # Storing the response (source code of called website)
    FULL_HTML_CODE = CALL_HTTP.read()
    
    # Paring the URL so I can work with it
    PARSED_URL = urlparse(Site_URL)
    print ""
    print "[i] Moving on now."
    print "[i] Server/Domain is:",  PARSED_URL.netloc
    if len(PARSED_URL.path) == 0:
        print "[!] The URL doesn't contain a script :("
    else:
        print "[i] Detected the path to the script :) :",  PARSED_URL.path
    if len(PARSED_URL.query) == 0:
        print "[!] The URL doesn't contain a query string :("
    else:
        print "[i] Detected the URL query string :) :",  PARSED_URL.query
        print ""
    
    # Searching it for MySQL errors
    SRCH_SQL_ERR_1 = re.findall(SQL_ERR_1, FULL_HTML_CODE)
    if len(SRCH_SQL_ERR_1) != 0:
        print "[!] SQL error in the original URL/website found."
        print "[!] There might be problems exploiting this website (if it is vulnerable)."
    
    SRCH_SQL_ERR_2 = re.findall(SQL_ERR_2,  FULL_HTML_CODE)
    if len(SRCH_SQL_ERR_2) != 0:
        print "[!] SQL error in the original URL/website found."
        print "[!] There might be problems exploiting this website (if it is vulnerable)."
    
    SRCH_SQL_ERR_3 = re.findall(SQL_ERR_3,  FULL_HTML_CODE)
    if len(SRCH_SQL_ERR_3) != 0:
        print "[!] SQL error in the original URL/website found."
        print "[!] There might be problems exploiting this website (if it is vulnerable)."
    
    if PARM_SGN_1 in Site_URL and PARM_EQ in Site_URL:
        print "[i] It seems that the URL contains at least one parameter."
        print "[i] Trying to find also another parameters..."
        
        if PARM_SGN_2 in PARSED_URL.query and PARM_EQ in PARSED_URL.query:
            print "[i] Also found at least one other parameter in the URL."
        else:
            print "[i] No other parameters were found."
        
    else:
        print ""
        print "[!] It seems that there is no parameter in the URL."
        print "[!] How the hell am I supposed to find a vulnerability?"
        print "[!] Please provide an URL with a script and query string."
        print "[!] Example: target/index.php?cat=1&article_id=2"
        print "[!] Hint: I can't handle SEO links, so try to find an URL with a query string."
        print "[!] Exiting now!"
        print ""
        print ""
        sys.exit(1)
    
   
    PARAMS = dict([part.split('=') for part in PARSED_URL[4].split('&')])

  
    PARAM_CNTR = len(PARAMS)
    

    print "[i] The following", PARAM_CNTR, "parameter(s) was/were found:"
    print "[i]",  PARAMS
    print "[i] Starting to scan the provided URL(s) for SQL injection vulnerabilities."
    print ""


    for index, item in enumerate(PARAMS):

        print "[i] Probing parameter \"",  item, "\"..."
  

        QUERY_FOR_REPLACE = "".join(PARSED_URL[4:5])
        MODIFIED_QUERY = QUERY_FOR_REPLACE.replace(PARAMS[item],  TRIGGER_ERR_1)

        TRIGGER_URL_1_P1 = "".join(PARSED_URL[0:1]) + "://" #http
        TRIGGER_URL_1_P2 = "".join(PARSED_URL[1:2])         #www.site.com/test.php
        TRIGGER_URL_1_P3 = "".join(PARSED_URL[2:3])  + "?"  
        TRIGGER_URL_1_P4 = "".join(MODIFIED_QUERY)  
        TRIG_URL_1 = TRIGGER_URL_1_P1 + TRIGGER_URL_1_P2 + TRIGGER_URL_1_P3 + TRIGGER_URL_1_P4

        # Calling the modified URL
        try:
            HTTP_CALL_TRIGGER_1 = urllib2.urlopen(TRIG_URL_1)
        except HTTPError,  e:
            print "[!] The connection could not be established."
            print "[!] Error code: ",  e.code
        except URLError,  e:
            print "[!] The connection could not be established."
            print "[!] Reason: ",  e.reason
    
        # Storing the response (by .read we get all the source code of called website)
        HTML_CALL_TRIGGER_1 = HTTP_CALL_TRIGGER_1.read()

        # Searching the response for MySQL errors
        SRCH_SQL_ERR_TRIGG_1 = re.findall(SQL_ERR_1, HTML_CALL_TRIGGER_1)
        SRCH_SQL_ERR_TRIGG_2 = re.findall(SQL_ERR_2, HTML_CALL_TRIGGER_1)
        SRCH_SQL_ERR_TRIGG_3 = re.findall(SQL_ERR_3, HTML_CALL_TRIGGER_1)
        
        # If the first method was not successfull we simply try the next one
        if len(SRCH_SQL_ERR_TRIGG_1) == 0 and len(SRCH_SQL_ERR_TRIGG_2) == 0 and len(SRCH_SQL_ERR_TRIGG_3) == 0:

            MODIFIED_QUERY = QUERY_FOR_REPLACE.replace(PARAMS[item],  TRIGGER_ERR_2)
            TRIGGER_URL_2_P1 = "".join(PARSED_URL[0:1]) + "://"
            TRIGGER_URL_2_P2 = "".join(PARSED_URL[1:2]) 
            TRIGGER_URL_2_P3 = "".join(PARSED_URL[2:3])  + "?"
            TRIGGER_URL_2_P4 = "".join(MODIFIED_QUERY)  
            TRIG_URL_2 = TRIGGER_URL_2_P1 + TRIGGER_URL_2_P2 + TRIGGER_URL_2_P3 + TRIGGER_URL_2_P4
            try:
                http_request_trigger_2 = urllib2.urlopen(TRIG_URL_2)
            except HTTPError,  e:
                print "[!] The connection could not be established."
                print "[!] Error code: ",  e.code
            except URLError,  e:
                print "[!] The connection could not be established."
                print "[!] Reason: ",  e.reason
            
            # Call the modified URL and look for MySQL errors
            HTML_CALL_TRIGGER_2 = http_request_trigger_2.read()
            SRCH_SQL_ERR_TRIGG_1 = re.findall(SQL_ERR_1, HTML_CALL_TRIGGER_2)
            SRCH_SQL_ERR_TRIGG_2 = re.findall(SQL_ERR_2, HTML_CALL_TRIGGER_2)
            SRCH_SQL_ERR_TRIGG_3 = re.findall(SQL_ERR_3, HTML_CALL_TRIGGER_2)
            
            # When nothing was found show this message
            if len(SRCH_SQL_ERR_TRIGG_1) == 0 and len(SRCH_SQL_ERR_TRIGG_2) == 0 and len(SRCH_SQL_ERR_TRIGG_3) == 0:
                print "[i] The parameter \"",  item,  "\" doesn't seem to be vulnerable."
        
        else:
            # Add the vulnerable parameter to the report variable
            print "[+] Found possible SQL injection vulnerability! Parameter:", item
            VULN_PARAM[index+1] = item
                   
    # Generate a short report
    if len(VULN_PARAM) != 0:
        print ""
        print "[#] Displaying a short report for the provided URL:"
        print "[#] At least one parameter seems to be vulnerable. "
        print VULN_PARAM
        print "[#] (Pattern: param number, param name)"
        
    else:
        print ""
        print "[#] Displaying a short report for the provided URL:"
        print "[#] No SQL injection vulnerabilities found"
        print "Your Website is secure from SQL Injection."

    # And exit
    print ""
    print "[i] That's it. Bye!"
    print ""
    print ""
    sys.exit(1)
    return
    # End of scan_url function
    # Function for finding the amount of columns (column fuzzer)
# Checking if argument was provided
if len(sys.argv) <=1:
    USAGE_PRNT()
    sys.exit(1)
    
for arg in sys.argv:
    # Checking if help was called
    if arg == "--help":
        HELP_PRNT()
        sys.exit(1)
    # Cheking if about was called
    if arg == "--about":
        ABOUT_PRNT()
        sys.exit(1)
    
    # Checking if scanning mode was called
    if arg == "-u":
        Site_URL = sys.argv[2]
        BANNER_PRNT()
        
        # At first we test if we can actually reach the provided URL
        URL_TESTING(Site_URL)
        
        # Now start the main scanning function
        URL_SCANNING(Site_URL)
    
