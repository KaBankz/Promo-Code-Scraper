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

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re, os, time, sys, subprocess

scriptVersion = "v1.0.0"

aboutTxt = """ABOUT\nWelcome to Promo Code Scraper  """ + scriptVersion + """
This program will scrape multiple websites for promo
codes for whatever site you select.

There are no guarantees if all the codes will work,
but some should work, if not try again on a later day
to see if any new codes have been added.

This program will create a folder with a text file inside
with all of the scraped promo codes.

You can manually input each code one by one in their
respective websites or you can use the companion script
which automates this tedious process."""

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

### About Section
def about():
  print('User Clicked About Button')
  toplevel = Toplevel()
  aboutOne = Label(toplevel, text=aboutTxt, justify=CENTER)
  aboutOne.pack(side="top", padx=30, pady=30)
  toplevel.focus_force()
  toplevel.resizable(False, False)

### Let User Select Save Location
def browsePath():
  print('User Clicked Browse Button')
  if not os.path.exists(savePath.get()):
    initFind = savePath.get()[:-12]
  else:
    initFind = savePath.get()
  print(initFind)
  dir = filedialog.askdirectory(initialdir=initFind, title='Please Select A Folder (Promo-Codes Folder Will Be Automatically Created)')
  if len(dir) > 0:
    savePath.delete(0,END)
    savePath.insert(0, Path(dir + '/Promo-Codes'))
  ### Change State Of Open Folder Button If Path Does Not Exist
  if not os.path.exists(savePath.get()):
    openFolderBTN.config(state="disabled")
  else:
    openFolderBTN.config(state="normal")
  return

### Open Save Location If It Exists, Added Support For Mac, And Linux Using Subprocess
def openFolder():
  print('User Clicked Open Folder Button')
  if os.path.exists(savePath.get()):
    if sys.platform.startswith("win32"):
      os.startfile(savePath.get())
    elif sys.platform.startswith("darwin"):
      subprocess.call(('open', savePath.get()))
    else:
      subprocess.call(('xdg-open', savePath.get()))
  else:
    messagebox.showinfo("ERROR!", "Your Selected Directory Does Not Have Promo-Codes Folder!")

def openFile(event):
  if sys.platform.startswith("win32"):
    os.startfile(Path(str(savePathLink["text"])))
  elif sys.platform.startswith("darwin"):
    subprocess.call(('open', Path(str(savePathLink["text"]))))
  else:
    subprocess.call(('xdg-open', Path(str(savePathLink["text"]))))

### Start Scraping
def getTarget():
  print('User Clicked Start Button')
  target = str(combo.get()).lower()
  fileSavePath = Path(savePath.get())
  fileName = target.title().replace(" ", "-") + '-Promo-Codes.txt'
  v.set('Loading Promo Codes For ' + target.title())
  root.update_idletasks()
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
  ### Gather All Codes From Sources, Remove Codes With Spaces, Then Sort Them In Ascending Order
  allPromoCodes = list(set(eval(sift(target))))
  allPromoCodes = [x for x in allPromoCodes if " " not in x]
  allPromoCodes.sort(key=str.lower)
  ### Check If Promo-Codes Folder Exits, If Not Create It
  if not os.path.exists(savePath.get()):
    os.mkdir(savePath.get())
  change = 'no'
  ### Check If Promo Code File Exists, If Not Create One, Else Edit Existing, Then Add All Found Codes
  if not os.path.exists(fileSavePath / fileName):
    with open(fileSavePath / fileName, 'w') as f:
      f.write(">====[Created @" + time.strftime("%X %x") + "]====<\n")
      f.write("\n".join(allPromoCodes))
      f.write("\n>====[Promo Code Scraper " + scriptVersion + "]====<")
  else:
    change = 'yes'
    with open(fileSavePath / fileName, 'r+') as f:
      old = f.read()
      f.seek(0)
      f.write(">====[Created @" + time.strftime("%X %x") + "]====<\n")
      f.write("\n".join(allPromoCodes))
      f.write("\n>====[Promo Code Scraper " + scriptVersion + "]====<")
      f.write("\n" + old)
  ### Change State Of Open Folder Button If Path Does Not Exist
  if not os.path.exists(savePath.get()):
    openFolderBTN.config(state="disabled")
  else:
    openFolderBTN.config(state="normal")
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
  ### Output To Console
  print('It took ' + str(timeElapsed)[:-13] + ' seconds to scrape ' + str(len(allPromoCodes)) + ' links')
  if change == 'no':
    print("\nA text file has been made at " + fileSavePath.as_posix() + "/" + fileName + "\n\nAll of the parsed codes are in that file")
  else:
    print("\nA text file has been edited at " + fileSavePath.as_posix() + "/" + fileName + "\n\nAll of the new parsed codes are in that file")
  ### Display Information To User
  v.set('Finished! Found ' + str(len(allPromoCodes)) + ' Codes')
  p.set(fileSavePath.as_posix() + "/" + fileName)
  root.update_idletasks()
  if change == 'no':
    messagebox.showinfo("Finished!", "A text file has been made at\n\n" + fileSavePath.as_posix() + "/" + fileName + '\n\nIt took ' + str(timeElapsed)[:-13] + ' seconds to scrape ' + str(len(allPromoCodes)) + ' links')
  else:
    messagebox.showinfo("Finished!", "A text file has been edited at\n\n" + fileSavePath.as_posix() + "/" + fileName + '\n\nIt took ' + str(timeElapsed)[:-13] + ' seconds to scrape ' + str(len(allPromoCodes)) + ' links')
############################################################################################
### Characters/Words That Are Mistaken For Codes
excludes = ['Discount Auto-Applied', 'Discount Auto Applied', 'Discount Applied', 'See site for details!', 'See Codes']
### Function To Remove All Instances Of Excluded Characters/Words From Codes
def removeExcludes(a):
  return [x for x in a if x not in excludes]
######################################## SOURCE ONE ########################################
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
######################################## SOURCE TWO ########################################
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
####################################### TKINTER CODE #######################################
### Create Root Frame
root = Tk()
style = Style()
root.title("Promo Code Scraper  " + scriptVersion)
style.configure("link.TLabel", foreground="blue")
### Dropdown For GUI
combo = Combobox(root)
combo['values']= ('Uber', 'Lyft', 'Amazon', 'Ebay', 'Best Buy', 'Macys', 'Walmart', 'Dominos', 'Papa Johns', 'Pizza Hut')
combo.current(0)
combo.grid(row=0, column=0, sticky='we', padx=5, pady=5)
### Create Start/Browse/OpenFolder/About Buttons
startSearchBTN = Button(root, text='Start', command=getTarget)
startSearchBTN.grid(row=0, column=1, padx=(0, 5), pady=5)
browsePathBTN = Button(root, text='Browse', command=browsePath)
browsePathBTN.grid(row=1, column=1, padx=(0, 5), pady=(0, 5))
aboutBTN = Button(root, text='About', command=about)
aboutBTN.grid(row=1, column=2, padx=(0, 5), pady=(0, 5))
openFolderBTN = Button(root, text='Open Folder', state='normal', command=openFolder)
openFolderBTN.grid(row=0, column=2, padx=(0, 5), pady=5)
### Current State Label
v = StringVar()
currentState = Label(root, textvariable=v, justify=LEFT)
currentState.grid(sticky=W, row=2, columnspan=3, padx=5)
v.set('Idle, Waiting User Input')
### Save Path Link
p = StringVar()
savePathLink = Label(root, textvariable=p, justify=LEFT, cursor="hand2", style="link.TLabel")
savePathLink.grid(sticky=W, row=3, columnspan=3, padx=5, pady=(0, 5))
savePathLink.bind('<Button-1>', openFile)
### Save Path Input For GUI
savePath = Entry(root)
savePath.grid(row=1, column=0, sticky='we', padx=5, pady=(0, 5))
savePath.insert(0, Path(os.getcwd().replace('\\', '/') + '/Promo-Codes'))
### Change State Of Open Folder Button If Path Does Not Exist
if not os.path.exists(savePath.get()):
  openFolderBTN.config(state="disabled")
### Resize Friendly
root.grid_columnconfigure(0, weight=1)
### Disable Y Resize
root.resizable(True, False)
### Position Window At Vertical Center
w = 500
h = 105
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight() - 200
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.update()
root.minsize(320, 0)
### Infinate Loop To Keep GUI Open Until User Quits
root.mainloop()
