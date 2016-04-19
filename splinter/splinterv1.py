"""
You will need to get splinter using pip.
Download: https://pip.pypa.io/en/latest/installing.html
Run:      python get-pip.py

Then (after setting the path) you must run pip install splinter.

Here resides the headless driver of choice:
http://phantomjs.org/download.html
"""

from splinter import Browser
import time
import urllib2
import os, sys, getopt
import subprocess
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
force = 0

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hf",["help", "force"])
    except getopt.GetoptError:
        print 'One of those options were invalid.'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == "--help":
            print 'Usage: python splinterv1.py [-f] [-h --help]'
            sys.exit()
        elif opt == "-f" or opt == "--force":
            global force
            force = 1

if __name__ == "__main__":
   main(sys.argv[1:])


def file_open(filename):
    try:
        f = open(filename, "r")
        print("Opened %s successfully" % filename)
        return (f, 100) #file exists
    except IOError:
        f = open(filename, "w")
        print("Created %s" % filename)
        return (f, 101) #file does not exist
    except:
        print "Something went wrong...\n"
        sys.exit()

date = time.strftime("%Y-%m-%d | %H:%M:%S")

site1 = "https://my.freenom.com/clientarea.php"
email = "debdanmeg@live.com.au"
password = "1995sikatarts"
password2 = "6991sikatartS"
enter = '\n'
site2 = "https://my.freenom.com/clientarea.php?action=domains"
subdomain = "minecraft"

new_ip = urllib2.urlopen("http://myip.dnsdynamic.org/").read()

output = file_open("oldip.txt")
f = output[0]

# When the oldip.txt file did exists.
# Then acts differently if IP has changed or not.
if(output[-1] == 100):
    old_ip = f.read()
    f.close()
    if(old_ip == new_ip):
        if(force == 0):
            f = file_open("log.txt")[0]
            f.close()
            """
            This may seem redundant, but this tries to open it if it 
            is there, makes it if it's not or termiantes program 
            execution when something goes wrong. If the program doesn't
            stop after this point, we know we're safe to append...        
            """
            f = open("log.txt", "a")
            f.write("[%s] IP still  %s\n" % (date, old_ip))
            f.close()
            print("IP has not changed. Exiting...")
            sys.exit()
        else:
            print("-f flag set, forcing rest of program execution...")

# When the old_ip.txt file did not exist.
else:
    old_ip = new_ip
    f.write(new_ip)
    f.close()

file_open("log.txt")
f.close()
f = open("log.txt", "a")
f.write("[%s] IP set to %s\n" % (date, new_ip))
f.close()

print("Old IP: %s\nNew IP: %s\n" % (old_ip, new_ip))


f = file_open("ip.txt")[0]
f.close()
f = open("ip.txt", "w")
f.write(new_ip)
f.close()

"""
Using the namecheap subdomain
"""

site1 = "https://www.namecheap.com/myaccount/login.aspx"
uname = "banool"
site2 = "https://manage.www.namecheap.com/myaccount/modsingle.asp?domain=ibdefinitions.me&type=hosts&rkey=NC"

browser = Browser('chrome')
browser.visit(site1)

unamefield = (browser.find_by_name('LoginUserName'))[-1]
unamefield.fill(uname)
pwordfield = (browser.find_by_name('LoginPassword'))[-1]
pwordfield.fill(password2[::-1] + enter)

browser.visit(site2)
browser.fill("Address4", new_ip)
"""
Works with the chrome driver but not phantomjs
ipfield = (browser.find_by_name("Address4"))[0]
ipfield.fill("123.3.130.55")
"""

submit = browser.find_by_name("HOSTSUBMIT")[-1]
submit.click()

print("Done!")
browser.quit()








"""
Using the freenom site.

browser = Browser('chrome')
browser.visit(site1)

browser.fill('username', email)
browser.fill('password', password[::-1] + enter)

browser.visit(site2)
browser.click_link_by_partial_text("Manage")
browser.click_link_by_partial_text("Management")
browser.click_link_by_partial_href("domainregister")


http://splinter.cobrateam.info/docs/api/driver-and-element-api.html#elementapi
What this does it it finds the element by the id, then uses that element
object to fill it. Since ids should be unique, using this method you should
always be able to do stuff with each element.

ns2box = browser.find_by_id("ns2") 
ns2box.fill(subdomain)

browser.fill('currentipaddress', old_ip)
browser.fill('newipaddress', new_ip)

submit = browser.find_by_value('Save Changes')[1]
submit.click()

#browser.find_by_id("ns2")
#browser.is_element_present_by_id("ns2") <-- goodun

old_ip = new_ip
f = open("oldip.txt", "w")
f.write(old_ip)
f.close()

time.sleep(2)
"""







"""
Using the Facebook thing

site1 = "http://www.facebook.com"
site2 = "https://www.facebook.com/editdoc.php?note_id=1509053409344925"

browser = Browser('firefox')

browser.visit(site1)
browser.fill('email', email)
browser.fill('pass', password2[::-1] + enter)

browser.visit(site2)

#with browser.get_iframe('editor') as iframe:
  #  iframe.do_stuff()

swag = browser.find_by_id("editor").first
swag.click()
time.sleep(3)
swag.click()
swag.fill('a')

old_ip = new_ip
f = open("oldip.txt", "w")
f.write(old_ip)
f.close()

swag.click()
"""


#browser.quit()