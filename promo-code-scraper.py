########################################################################
########################################################################
###   THIS PROGRAM WAS MADE BY DEATHHACKZ                            ###
###   YOU ARE FREE TO MODIFY THIS IN ANY WAY WHATSOEVER, AS LONG     ###
###   AS YOU CLEARLY STATE THAT IT IS IN NO WAY AFFILIATED TO        ###
###   DEATHHACKZ.                                                    ###
###   THIS IS BUILT ON PYTHON 3.7.1                                  ###
###   MADE ENTIRELY ON WINDOWS 10, BUT SHOULD WORK ON MACOS, OTHER   ###
###   OPERATING SYSTEMS ARE NOT OFFICIALLY SUPPORTED, BUT MAY WORK.  ###
########################################################################
########################################################################

### Importing Libraries
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from pathlib import Path
import re, os, time, sys, subprocess

scriptVersion = "v1.0.0"

input("""Welcome to Promo Code Scraper """ + scriptVersion + """!

This program will scrape multiple websites for promo
codes for whatever site you select.

There are no guarantees if all the codes will work,
but some should work, if not try again on a later day
to see if any new codes have been added.

This program will create a folder with a text file inside
with all of the scraped promo codes.

You can manually input each code one by one in their
respective websites or you can use the companion script
which automates this tedious process.

Press ENTER to continue.
""")

input("""
   _____             _   _     _    _            _
  |  __ \           | | | |   | |  | |          | |
  | |  | | ___  __ _| |_| |__ | |__| | __ _  ___| | __ ____
  | |  | |/ _ \/ _` | __| '_ \|  __  |/ _` |/ __| |/ /|_  /
  | |__| |  __/ (_| | |_| | | | |  | | (_| | (__|   <  / /
  |_____/ \___|\__,_|\__|_| |_|_|  |_|\__,_|\___|_|\_\/___|

By using this program you are solely responsible for your
actions, and cannot blame the creator of this program.

This is for Educational Purposes ONLY!

Proceed at your own caution

If you agree to the above terms press ENTER, if not bye ;)
""")

userSavePath = input("=======================================================\nType in your desired save path, press ENTER for default\n=======================================================\n")
if len(userSavePath) > 0:
  if not os.path.exists(userSavePath):
    userSavePath = input("Your selected directory does not exits, try again or press ENTER for default\n")
else:
  userSavePath = os.getcwd().replace('\\', '/')
  print(userSavePath + '/Promo-Codes')

userSavePath = Path(userSavePath.replace('\\', '/') + '/Promo-Codes')

target = input("""
Supported Websites:

Ride Sharing:
[1]Uber
[2]Lyft

eCommerce:
[3]Amazon
[4]Ebay
[5]Best Buy
[6]Macys
[7]Walmart

Food:
[8]Dominos
[9]Papa Johns
[10]Pizza Hut

Type in the number of the site you want promo codes for
""")

### Allow Only Numbers Within Defined Range
try:
  int(target)
  if not 1 <= int(target) <= 10:
    raise OverflowError("Value is outside of defined range")
except OverflowError:
    target = input("ERROR! Only numbers 1-10 allowed! Try again!\n")
except ValueError:
  try:
    float(target)
  except ValueError:
    target = input("ERROR! Only numbers 1-10 allowed! Try again!\n")

### All Of The Supported Stores/Companies
allStores = ['uber', 'lyft', 'amazon', 'ebay', 'best buy', 'macys', 'walmart', 'dominos', 'papa johns', 'pizza hut']
target = allStores[int(target)-1]
fileSaveName = target.title().replace(" ", "-") + '-Promo-Codes.txt'
### Characters/Words That Are Mistaken For Codes
excludes = ['Discount Auto-Applied', 'Discount Auto Applied', 'Discount Applied', 'See site for details!', 'See Codes']

### Only Allow Sources That Have The Selected Target
def sift(target):
  sourceSifter = ''
  sourceOneHas = ['uber', 'lyft', 'amazon', 'ebay', 'best buy', 'macys', 'walmart', 'dominos', 'papa johns', 'pizza hut']
  sourceTwoHas = ['uber', 'lyft', 'amazon', 'ebay', 'best buy', 'macys', 'walmart', 'dominos', 'papa johns', 'pizza hut']
  sourceThreeHas = ['uber', 'lyft', 'amazon', 'ebay', 'best buy', 'macys', 'walmart', 'dominos', 'papa johns', 'pizza hut']
  if target in sourceOneHas:
    sourceSifter += 'sourceOne(target)'
  if target in sourceTwoHas:
    sourceSifter += 'sourceTwo(target)'
  if target in sourceThreeHas:
    sourceSifter += 'sourceThree(target)'
  sourceSifter = sourceSifter.replace(')s', ') + s')
  return sourceSifter

### Function To Remove All Instances Of Excluded Characters/Words From Codes
def removeExcludes(a):
  return [x for x in a if x not in excludes]

print("""
      __                    ___
     / /   ____  ____ _____/ (_)___  ____ _
    / /   / __ \/ __ `/ __  / / __ \/ __ `/
   / /___/ /_/ / /_/ / /_/ / / / / / /_/ / _ _
  /_____/\____/\__,_/\__,_/_/_/ /_/\__, (_|_|_)
                                  /____/
""")

### Starts Stopwatch To Measure Speed Of Script
timeStart = time.time()

######################################### SOURCE ONE #########################################
def sourceOne(target):
  ### Source One URLs
  rawSourceOneURL = 'https://zoutons.com'
  sourceOneURL = 'https://zoutons.com/us/' + target.replace(" ", "-") + '-coupons'
  ### Loading Main Page
  getSourceOneURL = uReq(sourceOneURL)
  sourceOne_html = getSourceOneURL.read()
  getSourceOneURL.close()
  sourceOneParsed = soup(sourceOne_html, 'html.parser')
  ### Getting Unlocked Code URL
  sourceOneNewURL = sourceOneParsed.findAll("a", {"class":"code_b_link"})
  sourceOneNewURL = rawSourceOneURL + sourceOneNewURL[0]["href"].split("#")[0] + "#close"
  ### Loading New Unlocked Code URL
  getNewSourceOne = uReq(sourceOneNewURL)
  newSourceOne_html = getNewSourceOne.read()
  getNewSourceOne.close()
  newSourceOneParsed = soup(newSourceOne_html, 'html.parser')
  ### Unformatted Codes
  sourceOneRawCodes = []
  ### Get All Unformatted Promo Codes And Push To List
  getAllSourceOneRawCodes = newSourceOneParsed.findAll("a", {"class":"code_b_link"})
  for rawCodes in getAllSourceOneRawCodes:
    getCodes = rawCodes.find("span")
    sourceOneRawCodes.append(str(getCodes))
  ### Formatting All Codes
  sourceOneEditedCodes = [x.replace('<span>', '').replace('</span>', '').replace('None', '').replace('+', '') for x in sourceOneRawCodes]
  sourceOneEditedCodes = removeExcludes(sourceOneEditedCodes)
  ### All Codes From Source One
  sourceOneCodes = list(filter(None, sourceOneEditedCodes))
  return sourceOneCodes
######################################### SOURCE TWO #########################################
def sourceTwo(target):
  ### Source Two URLs
  rawSourceTwoURL = 'https://www.groupon.com'
  sourceTwoURL = 'https://www.groupon.com/coupons/stores/' + target.replace(" ", "") + '.com'
  ### Loading Main Page
  getSourceTwoURL = uReq(sourceTwoURL)
  sourceTwo_html = getSourceTwoURL.read()
  getSourceTwoURL.close()
  sourceTwoParsed = soup(sourceTwo_html, 'html.parser')
  ### Getting Unlocked Code URL
  sourceTwoNewURL = sourceTwoParsed.findAll("a", {"data-bhw": "GetOnlinePromoCodeButton"})
  sourceTwoNewURL = 'https://www.groupon.com/coupons/stores/' + target.replace(" ", "") + '.com?c=' + sourceTwoNewURL[0]["href"].split('/')[3]
  ### Loading New Unlocked Code URL
  getNewSourceTwo = uReq(sourceTwoNewURL)
  newSourceTwo_html = getNewSourceTwo.read()
  getNewSourceTwo.close()
  newSourceTwoParsed = soup(newSourceTwo_html, 'html.parser')
  ### Unformatted Codes
  sourceTwoRawCodes = []
  ### Get All Unformatted Promo Codes And Set It To List
  getAllSourceTwoRawCodes = newSourceTwoParsed.script.text
  getCodes = re.findall(r'\"code\":\"(.*?)\"', getAllSourceTwoRawCodes)
  sourceTwoRawCodes = list(set(getCodes))
  ### Formatting All Codes
  sourceTwoEditedCodes = [x.replace('Code:', '').replace('+', '') for x in sourceTwoRawCodes]
  sourceTwoEditedCodes = removeExcludes(sourceTwoEditedCodes)
  ### All Codes From Source Two
  sourceTwoCodes = list(filter(None, sourceTwoEditedCodes))
  return sourceTwoCodes
####################################### SOURCE Three #######################################
def sourceThree(target):
  ### Source Three URLs
  rawSourceThreeURL = 'https://www.joinhoney.com'
  sourceThreeURL = 'https://www.joinhoney.com/shop/' + target.replace(" ", "-") + '?hasOpened=1'
  ### Loading Main Page
  getSourceThreeURL = uReq(sourceThreeURL)
  sourceThree_html = getSourceThreeURL.read()
  getSourceThreeURL.close()
  sourceThreeParsed = soup(sourceThree_html, 'html.parser')
  ### Unformatted Codes
  sourceThreeRawCodes = []
  ### Get All Unformatted Promo Codes And Set It To List
  getAllSourceThreeRawCodes = sourceThreeParsed.script.text
  getCodes = re.findall(r'\"rank\":\d+\.\d{1,}?,\"code\":\"(.*?)\"', getAllSourceThreeRawCodes)
  sourceThreeRawCodes = list(set(getCodes))
  ### Formatting All Codes
  sourceThreeEditedCodes = removeExcludes(sourceThreeRawCodes)
  ### All Codes From Source Three
  sourceThreeCodes = list(filter(None, sourceThreeEditedCodes))
  return sourceThreeCodes
######################################## COMPILING CODES ########################################

### Gather All Codes From Sources, Remove Codes With Spaces, Then Sort Them In Ascending Order
allPromoCodes = list(set(eval(sift(target))))
allPromoCodes = [x for x in allPromoCodes if " " not in x]
allPromoCodes.sort(key=str.lower)

### Check If Promo-Codes Folder Exits, If Not Create It
if not os.path.exists(userSavePath):
  os.mkdir(userSavePath)

change = 'no'

### Check If Promo Code File Exists, If Not Create One, Else Edit Existing, Then Add All Found Codes
if not os.path.exists(userSavePath / fileSaveName):
  with open(userSavePath / fileSaveName, 'w') as f:
    f.write(">====[Created @" + time.strftime("%X %x") + "]====<\n")
    f.write("\n".join(allPromoCodes))
    f.write("\n>====[Promo Code Scraper " + scriptVersion + "]====<")
else:
  change = 'yes'
  with open(userSavePath / fileSaveName, 'r+') as f:
    old = f.read()
    f.seek(0)
    f.write(">====[Created @" + time.strftime("%X %x") + "]====<\n")
    f.write("\n".join(allPromoCodes))
    f.write("\n>====[Promo Code Scraper " + scriptVersion + "]====<")
    f.write("\n" + old)

### Stop Stopwatch And Measure Script Speed
timeEnd = time.time()
timeElapsed = timeEnd - timeStart

print("""
      ____                   __
     / __ \____  ____  ___  / /
    / / / / __ \/ __ \/ _ \/ /
   / /_/ / /_/ / / / /  __/_/
  /_____/\____/_/ /_/\___(_)

""")

### Display Information To User
print('It took ' + str(timeElapsed)[:-13] + ' seconds to scrape ' + str(len(allPromoCodes)) + ' links')

if change == 'no':
  print("\nA text file has been made at " + userSavePath.as_posix() + "/" + fileSaveName + "\n\nAll of the parsed codes are in that file")
else:
  print("\nA text file has been edited at " + userSavePath.as_posix() + "/" + fileSaveName + "\n\nAll of the new parsed codes are in that file")

### Open Created/Edited Text File And Close Script, Added Support For Mac, And Linux Using Subprocess
input("\nPress Enter to Close & Open Promo Code File")
if sys.platform.startswith("win32"):
  os.startfile(userSavePath / fileSaveName)
elif sys.platform.startswith("darwin"):
  subprocess.call(('open', userSavePath / fileSaveName))
else:
  subprocess.call(('xdg-open', userSavePath / fileSaveName))
sys.exit()

# ########################################## TEMPLATE ##########################################

# def source"XXXX"(target):
#   ### Source XXXX URLs
#   rawSource"XXXX"URL = 'XXXX'
#   source"XXXX"URL = 'XXXX'
#   ### Loading Main Page
#   getSource"XXXX"URL = uReq(source"XXXX"URL)
#   source"XXXX"_html = getSource"XXXX"URL.read()
#   getSource"XXXX"URL.close()
#   source"XXXX"Parsed = soup(source"XXXX"_html, 'html.parser')
#   ### Getting Unlocked Code URL
#   source"XXXX"NewURL = findAll("a", {"class": "button-show-code"})
#   source"XXXX"NewURL = rawSource"XXXX"URL + source"XXXX"NewURL[0][href]...
#   ### Loading New Unlocked Code URL
#   getNewSource"XXXX" = uReq(source"XXXX"NewURL)
#   newSource"XXXX"_html = getNewSource"XXXX".read()
#   getNewSource"XXXX".close()
#   newSource"XXXX"Parsed = soup(newSource"XXXX"_html, 'html.parser')
#   ### Unformatted Codes
#   source"XXXX"RawCodes = []
#   ### Conditional Code ###
#   ### Conditional Code ###
#   ### Formatting All Codes
#   source"XXXX"EditedCodes = []
#   source"XXXX"EditedCodes = removeExcludes(source"XXXX"EditedCodes)
#   ### All Codes From Source XXXX
#   source"XXXX"Codes = list(filter(None, source"XXXX"EditedCodes))
#   return source"XXXX"Codes

# source"XXXX"(target)

# ########################################## TEMPLATE ##########################################
