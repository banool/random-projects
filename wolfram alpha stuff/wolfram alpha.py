from requests import get 

key = "XLPAPH-EGVKKAAT37"
input_want = str(raw_input("Whaddya wanna kno chunt? "))

call = "http://api.wolframalpha.com/v2/query?input=" + input_want + "&appid=" + key

data = get(call)
status_code = int(data.status_code)
if status_code == 200:
    print "Good call, code 200"
    print data.text
else:
    print "Something went wrong, got code " + str(status_code)


