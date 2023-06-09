# --------   \/  BEN'S CODE  \/    --------#
# -------- IMPORTING KIVY WIDGETS -------- #

from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window

from datetime import datetime
from datetime import date

import random

import ast

from covid import Covid

Config.set('graphics', 'fullscreen', 0)
Config.write()

# -------- EXTRACTING USER INFORMATION -------- #
# NOTE:
# userFile = users.txt,
# userFileContent = content of users.txt in str form,
# userDictionary = content of users.txt in dict form,
# userList = content of users.txt in list form.

userFile = open("users.txt", "r")
userFileContent = userFile.read()
userDictionary = ast.literal_eval(userFileContent)
userFile.close()
activityFile = open("activity.txt", "r")
activityFileContent = activityFile.read()
activityDictionary = ast.literal_eval(activityFileContent)
activityFile.close()

# -------- POP-UP BOXES --------#


# Invalid Username and/or Passowrd Pop-up
class invalidUsernamePopup(FloatLayout):
    pass


# Account Not In Database Pop-up
class accountNotValidPopup(FloatLayout):
    pass


# Wrong Passowrd Pop-up
class wrongPasswordPopup(FloatLayout):
    pass


# Entry Text Boxes Empty Pop-up
class noEntryPopup(FloatLayout):
    pass


# Invalid Time Pop-up
class invalidTimePopup(FloatLayout):
    pass


# Invalid Date Pop-up
class invalidDatePopup(FloatLayout):
    pass


# Invalid Look Up Pop-up
class invalidLookupPopup(FloatLayout):
    pass


# -------- LANDING SCREEN PYTHON CODE -------- #

infoFile = open("info.txt", "r")
enteredUser = int(infoFile.read())
infoFile.close()


class LandingScreen(Screen, Widget):
    email = ObjectProperty(None)
    emailDefault = StringProperty()
    password = ObjectProperty(None)
    passwordDefault = StringProperty()
    hidePasswordButton = ObjectProperty(None)
    apiInfo = StringProperty()

    def __init__(self, **kwargs):
        super(LandingScreen, self).__init__(**kwargs)
        covid = Covid()
        covid.get_data()
        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        self.apiInfo = str("\n\n\nGlobal active cases: " + str(active) +
                           "\nGlobal confirmed cases: " + str(confirmed) +
                           "\nGlobal recoveries: " + str(recovered))
        tipVariable = random.randint(0, 9)
        if tipVariable == 0:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nClean your hands often. Use soap and water, or "\
                           "an alcohol-based hand rub."
        elif tipVariable == 1:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nStay home if you are sick."
        elif tipVariable == 2:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nWear a mask on public transport, if possable."
        elif tipVariable == 3:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nMaintain a safe distance from anyone who is "\
                           "coughing or sneezing."
        elif tipVariable == 4:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nWear a mask when physical distancing is not "\
                           "possible."
        elif tipVariable == 5:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nAvoid touching your eyes, nose or mouth."
        elif tipVariable == 6:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nCover your nose and mouth with your bent elbow "\
                           "or a tissue when you cough or sneeze."
        elif tipVariable == 7:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nSeek medical attention if you "\
                           "have a fever, cough "\
                           "or difficulty breathing."
        else:
            self.apiInfo = self.apiInfo + "\n\nRemember to:"\
                           "\nFace the coloured side away when wearing a mask."
        global enteredUser
        if enteredUser == -1:
            self.emailDefault = ""
            self.passwordDefault = ""
        else:
            global userDictionary
            self.emailDefault = userDictionary[enteredUser][0]
            self.passwordDefault = userDictionary[enteredUser][1]
            enteredUser = -1

    def login_submit(self, widget):
        # Animating the button
        button_animate = Animation(
            pos_hint={"x": 0.05, "top": 0.39},
            duration=0.05)
        button_animate += Animation(
            pos_hint={"x": 0.05, "top": 0.40},
            duration=0.1)
        button_animate.start(widget)

        # Password and Username Validation
        # accessState = Current state of user's entry attempt;
        # 4 = Not yet determined
        # 0 = No issues, user access granted
        # 1 = One or both textboxes are empty
        # 2 = Username does not match any profile in the database
        # 3 = Password is incorrect (does not match the selected profile)
        # 5 = User has logged in as admin

        accessState = 4
        if str(self.email.text) == "" or str(self.password.text) == "":
            accessState = 1
        if accessState == 4 and\
           str(self.email.text) == "ADMIN" and\
           accessState == 4 and\
           str(self.password.text) == "ADMIN":
            accessState = 5
        elif (accessState == 4 and
              str(self.email.text) != "ADMIN" or
              accessState == 4 and
              str(self.password.text) != "ADMIN"):
            for i in range(0, len(userDictionary)):
                if userDictionary[i][0] == str(self.email.text):
                    accessState = 4
                    observedAccount = i
                    break
                else:
                    accessState = 2
            if accessState == 4 and userDictionary[observedAccount][1]\
               == str(self.password.text):
                accessState = 0
                global enteredUser
                enteredUser = i
                infoFile = open("info.txt", "w")
                infoFile.write(str(enteredUser))
                infoFile.close()
            elif (accessState == 4 and
                  userDictionary[observedAccount][1] !=
                  str(self.password.text)):
                accessState = 3
        if accessState == 0:
            self.email.text = ""
            self.password.text = ""
            self.manager.current = "UserDashboard"
        elif accessState == 1:
            show = invalidUsernamePopup()
            popupWindow = Popup(title="Invalid Email or Password",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif accessState == 2:
            show = accountNotValidPopup()
            popupWindow = Popup(title="Account Does Not Exist",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif accessState == 3:
            show = wrongPasswordPopup()
            popupWindow = Popup(title="Password Incorrect!",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        if accessState == 5:
            self.email.text = ""
            self.password.text = ""
            self.manager.current = "LookupScreen"

    # Hiding And Revealing Password On Button Press
    def unhidePassword(self, widget):
        if self.password.password is True:
            self.password.password = False
            self.hidePasswordButton\
                .background_normal = 'images/hide_password.png'
            self.hidePasswordButton\
                .background_down = 'images/hide_password.png'
        elif self.password.password is False:
            self.password.password = True
            self.hidePasswordButton\
                .background_normal = 'images/unhide_password.png'
            self.hidePasswordButton\
                .background_down = 'images/unhide_password.png'
        # Animating the button
        button_animate = Animation(
            pos_hint={"x": 0.285, "top": 0.550},
            duration=0.05)
        button_animate += Animation(
            pos_hint={"x": 0.285, "top": 0.555},
            duration=0.1)
        button_animate.start(widget)


# --------       \/  ETHAN'S CODE  \/        -------#
# -------- REGISTRATION SCREEN PYTHON CODE -------- #


# Setting up classes for the poppups.
class invalidRegNamePopup(FloatLayout):
        pass


class invalidPhoneNumberPopup(FloatLayout):
        pass


class invalidPasswordPopup(FloatLayout):
        pass


class invalidAddressPopup(FloatLayout):
        pass


class UnmatchedEmailPopup(FloatLayout):
        pass


class NoRecordedActivityPopup(FloatLayout):
        pass


# Setting variables for the dictionary implementation.
class RegistrationScreen(Screen, Widget):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    phoneNumber = ObjectProperty(None)
    fullName = ObjectProperty(None)
    address = ObjectProperty(None)
    registrationButton = ObjectProperty(None)

    def on_pre_enter(self):
        global enteredUser
        global userDictionary
        if enteredUser != -1:
            global userDictionary
            self.email.text = userDictionary[enteredUser][0]
            self.password.text = userDictionary[enteredUser][1]
            self.phoneNumber.text = userDictionary[enteredUser][2]
            self.fullName.text = userDictionary[enteredUser][3]
            self.address.text = userDictionary[enteredUser][4]
            self.registrationButton.text = "UPDATE ACCOUNT"
        else:
            self.email.text = ""
            self.password.text = ""
            self.phoneNumber.text = ""
            self.fullName.text = ""
            self.address.text = ""
            self.registrationButton.text = "REGISTER"


# Error handling, searching for unfilled content boxes.
    def register(self, widget):
        global enteredUser
        global userDictionary
        if " " in self.email.text or self\
                      .email.text == "" or " " not in self.fullName.text:
            show = invalidRegNamePopup()
            popupWindow = Popup(title="Invalid Fullname or Email",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif False == ((self.phoneNumber.text).
                       isdigit()) or self.phoneNumber.text == "":
            show = invalidPhoneNumberPopup()
            popupWindow = Popup(title="Invalid Phone Number",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif "@" not in self.email.text or self.email.text == "":
            show = invalidRegNamePopup()
            popupWindow = Popup(title="Invalid Fullname or Email",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif "." not in self.email.text:
            show = invalidRegNamePopup()
            popupWindow = Popup(title="Invalid Fullname or Email",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif True == ((self.fullName.text).
                      isdigit()) or self.fullName.text == "":
            show = invalidRegNamePopup()
            popupWindow = Popup(title="Invalid Fullname or Email",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif True == " " or "\'" in self.password\
                                        .text or self.password.text == "":
            show = invalidPasswordPopup()
            popupWindow = Popup(title="Invalid Password",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif (self.address.text == "" or
              self.address.text == "" or
              "|" in self.address.text or
              ">" in self.address.text or
              "<" in self.address.text or
              "_" in self.address.text or
              "=" in self.address.text or
              "*" in self.address.text or
              "^" in self.address.text or
              "%" in self.address.text or
              "@" in self.address.text):
            show = invalidAddressPopup()
            popupWindow = Popup(title="Invalid Address",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        else:
            currentUsers = [self.email.text,
                            self.password.text,
                            self.phoneNumber.text,
                            self.fullName.text,
                            self.address.text]
            if enteredUser == -1:
                userDictionary[len(userDictionary)] = currentUsers
                enteredUser = len(userDictionary) - 1
                infoFile = open("info.txt", "w")
                infoFile.write(str(enteredUser))
                infoFile.close()
            else:
                userDictionary[enteredUser] = currentUsers
            userFile = open("users.txt", "w")
            userFile.write(str(userDictionary))
            userFile.close
            global activityDictionary
            activityDictionary[len(userDictionary) - 1] = []
            activityFile = open("activity.txt", "w")
            activityFile.write(str(activityDictionary))
            activityFile.close()
            self.email.text = ""
            self.password.text = ""
            self.phoneNumber.text = ""
            self.address.text = ""
            self.fullName.text = ""
            self.manager.current = "UserDashboard"
        # Animating the button
        button_animate = Animation(
            pos_hint={"x": 0.25, "top": 0.19},
            duration=0.05)
        button_animate += Animation(
            pos_hint={"x": 0.25, "top": 0.20},
            duration=0.1)
        button_animate.start(widget)

    def back(self, widget):
        # Animating the button
        button_animate = Animation(
            pos_hint={"x": 0.025, "top": 0.19},
            duration=0.05)
        button_animate += Animation(
            pos_hint={"x": 0.025, "top": 0.20},
            duration=0.1)
        button_animate.start(widget)
        global enteredUser
        if enteredUser == -1:
            self.manager.current = 'LandingScreen'
        else:
            self.manager.current = 'UserDashboard'


# --------     \/  BEN'S CODE  \/      --------#
# -------- USER DASHBOARD PYTHON CODE -------- #


class UserDashboard(Screen):
    userWelcomeA = ObjectProperty(None)
    userWelcomeB = ObjectProperty(None)
    userActivity = ObjectProperty(None)
    location = ObjectProperty(None)
    time = ObjectProperty(None)
    date = ObjectProperty(None)

    # Function called when user logs in
    # Updates Kivy UI with appropriate welcome message
    # Adds or overwrites recent activity in UI

    def on_pre_enter(self):
        global enteredUser
        global userDictionary
        global activityDictionary
        global datetime
        self.userWelcomeA.text = "HELLO"
        self.userWelcomeA.font_size = 60
        self.userWelcomeB.text = str("\n" +
                                     userDictionary[enteredUser]
                                     [3].split(" ")[0].upper())
        if int(datetime.now().strftime("%H%M")) >= 600\
           and int(datetime.now().strftime("%H%M")) < 900:
            self.userWelcomeA.text = self.userWelcomeA.text\
                .replace("HELLO", "\nGOOD MORNING")
            self.userWelcomeA.font_size = 34
        elif (int(datetime.now().strftime("%H%M")) >= 1300 and
              int(datetime.now().strftime("%H%M")) < 1700):
            self.userWelcomeA.text = self.userWelcomeA.text\
                .replace("HELLO", "\nGOOD AFTERNOON")
            self.userWelcomeA.font_size = 34
        elif (int(datetime.now().strftime("%H%M")) >= 1700 and
              int(datetime.now().strftime("%H%M")) < 2100):
            self.userWelcomeA.text = self.userWelcomeA.text\
                .replace("HELLO", "\nGOOD EVENING")
            self.userWelcomeA.font_size = 34
        elif (int(datetime.now().strftime("%H%M")) >= 2100 and
              int(datetime.now().strftime("%H%M")) < 2400 or
              int(datetime.now().strftime("%H%M")) >= 0 and
              int(datetime.now().strftime("%H%M")) < 600):
            self.userWelcomeA.text =\
                 self.userWelcomeA.text.replace("HELLO", "\nGOOD NIGHT")
            self.userWelcomeA.font_size = 34
        if activityDictionary[enteredUser] != []:
            self.userActivity.text = ""
            for i in reversed(range(0, len(activityDictionary[enteredUser]))):
                self.userActivity.text =\
                     self.userActivity.text +\
                     activityDictionary[enteredUser][i].replace("!", " / ") +\
                     "\n\n"
        else:
            self.userActivity.text = "NO RECENT ACTIVITY"
        systemTime = datetime.now()
        self.time.text = systemTime.strftime("%H%M")
        systemDate = date.today()
        self.date.text = systemDate.strftime("%d/%m/%Y")

    # Function called when user logs out
    def logOut(self, widget):
        global enteredUser
        enteredUser = -1
        infoFile = open("info.txt", "w")
        infoFile.write(str(enteredUser))
        infoFile.close()
        self.manager.current = 'LandingScreen'
        # Animating the button
        button_animate = Animation(
            pos_hint={"x": 0.34, "top": 0.244},
            duration=0.05)
        button_animate += Animation(
            pos_hint={"x": 0.34, "top": 0.254},
            duration=0.1)
        button_animate.start(widget)

    # Function called when user submits an activity entry
    # Entry data is validated
    # Python activity dictionary is updated
    # New dictionary is saved to activity.txt
    # Kivy UI is updated to show recent activity

    def submit(self, widget):
        allowedDateCharacters = {'1',
                                 '2',
                                 '3',
                                 '4',
                                 '5',
                                 '6',
                                 '7',
                                 '8',
                                 '9',
                                 '0',
                                 '/'}
        if (self.location.text != "" and
            self.location.text.isspace() is False and
            self.date.text != "" and
            allowedDateCharacters.issuperset(self.date.text) is True and
            self.time.text != "" and
            self.time.text.isnumeric() is True and
            "@" not in self.location.text and
            "%" not in self.location.text and
            ">" not in self.location.text and
            "<" not in self.location.text and
            "^" not in self.location.text and
            "*" not in self.location.text and
            "=" not in self.location.text and
            "]" not in self.location.text and
            "[" not in self.location.text and
            "}" not in self.location.text and
            "{" not in self.location.text and "|"
                not in self.location.text):
            timeEntryLength = 0
            for i in range(0, len(self.time.text)):
                timeEntryLength = timeEntryLength + 1
            dateEntryLength = 0
            invalidDateEntry = 0
            if str(self.date.text)[0] == "/":
                invalidDateEntry = 1
            else:
                for i in range(0, len(self.date.text.split("/"))):
                    dateEntryLength = dateEntryLength + 1
            if dateEntryLength != 3:
                invalidDateEntry = 1
            if len(self.date.text.split("/")) == 3:
                for i in range(0, 3):
                    if self.date.text.split("/")[i] == "":
                        invalidDateEntry = 1
                if invalidDateEntry == 0:
                    if int(self.date.text.split("/")[0]) < 0 or\
                       int(self.date.text.split("/")[0]) > 32:
                        invalidDateEntry = 1
                    elif (int(self.date.text.split("/")[1]) < 0 or
                          int(self.date.text.split("/")[1]) > 12):
                        invalidDateEntry = 1
                    elif (int(self.date.text.split("/")[2]) < 2019 or
                          int(self.date.text.split("/")[2]) > 3019):
                        invalidDateEntry = 1
            else:
                invalidDateEntry = 1
            if (int(self.time.text) >= 0 and
                int(self.time.text) <= 2400 and
                timeEntryLength == 4 and
               invalidDateEntry == 0):
                global activityDictionary
                activityDictionary[enteredUser] = (
                                 activityDictionary[enteredUser] +
                                 [str(self.location.text +
                                      "!" +
                                      self.time.text +
                                      "!" +
                                      self.date.text)])
                activityFile = open("activity.txt", "w")
                activityFile.write(str(activityDictionary))
                activityFile.close()
                if self.userActivity.text == "NO RECENT ACTIVITY":
                    self.userActivity.text = (
                                              self.location.text +
                                              " / " +
                                              self.time.text +
                                              " / " +
                                              self.date.text)
                else:
                    self.userActivity.text = (self.location.text +
                                              " / " + self.time.text +
                                              " / " + self.date.text +
                                              "\n\n" +
                                              self.userActivity.text)
                self.location.text = ""
                self.time.text = ""
                self.date.text = ""
            elif invalidDateEntry == 1:
                show = invalidDatePopup()
                popupWindow = Popup(title="Invalid Entry!",
                                    content=show,
                                    size_hint=(None, None),
                                    size=(600, 400))
                popupWindow.open()
            else:
                show = invalidTimePopup()
                popupWindow = Popup(title="Invalid Entry!",
                                    content=show,
                                    size_hint=(None, None),
                                    size=(600, 400))
                popupWindow.open()
        elif (self.location.text == "" or
              self.time.text == "" or
              self.location.text.isspace() is True):
            show = noEntryPopup()
            popupWindow = Popup(title="Invalid Entry!",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif self.time.text.isnumeric() is False:
            show = invalidTimePopup()
            popupWindow = Popup(title="Invalid Entry!",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        elif(allowedDateCharacters.issuperset(self.date.text) is False or
             self.date.text == ""):
            show = invalidDatePopup()
            popupWindow = Popup(title="Invalid Entry!",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        # Animating the button
        button_animate = Animation(
            pos_hint={"x": 0.34, "top": 0.458},
            duration=0.05)
        button_animate += Animation(
            pos_hint={"x": 0.34, "top": 0.468},
            duration=0.1)
        button_animate.start(widget)

    def accountSettings(self, widget):
        # Animating the button
        button_animate = Animation(
            pos_hint={"x": 0.66, "top": 0.244},
            duration=0.05)
        button_animate += Animation(
            pos_hint={"x": 0.66, "top": 0.254},
            duration=0.1)
        button_animate.start(widget)
        self.manager.current = 'RegistrationScreen'


# -------- \/  BEN / ETHAN'S CODE  \/ --------#
# --------       LOOK UP SCREEN      -------- #


class LookupScreen(Screen):
    email = ObjectProperty(None)
    inquiryActivity = ObjectProperty(None)

    def searchSubmit(self, widget):
        if self.email.text != "" and\
           " " not in self.email.text and\
           "@" in self.email.text and\
           "." in self.email.text:
                userSearchValue = -1
                for i in range(0, len(userDictionary)):
                    if userDictionary[i][0] == self.email.text:
                        userSearchValue = i
                        break
                if userSearchValue == -1:
                    show = UnmatchedEmailPopup()
                    popupWindow = Popup(title="Invalid Inquiry",
                                        content=show,
                                        size_hint=(None, None),
                                        size=(600, 400))
                    popupWindow.open()
                elif activityDictionary[userSearchValue] == []:
                    show = NoRecordedActivityPopup()
                    popupWindow = Popup(title="Invalid Inquiry",
                                        content=show,
                                        size_hint=(None, None),
                                        size=(600, 400))
                    popupWindow.open()
                else:
                    userSearchActivity = str("INQUIRY ACTIVITY:\n" +
                                             (userDictionary
                                              [userSearchValue][3]) +
                                             "\n\n")
                    for i in range(0,
                                   len(activityDictionary[userSearchValue])):
                        userSearchActivity\
                            = str(userSearchActivity +
                                  "DATE: " +
                                  (activityDictionary[userSearchValue][i]
                                   .split("!")[2]) +
                                  " TIME: " +
                                  (activityDictionary[userSearchValue][i]
                                   .split("!")[1]) +
                                  " LOCATION: " +
                                  (activityDictionary[userSearchValue][i]
                                   .split("!")[0]) +
                                  "\n")
                    self.inquiryActivity.text = userSearchActivity
        else:
            show = invalidLookupPopup()
            popupWindow = Popup(title="Invalid Inquiry",
                                content=show,
                                size_hint=(None, None),
                                size=(600, 400))
            popupWindow.open()
        # Animating the button
        button_animate = Animation(
            pos_hint={"x": 0.02, "top": 0.79},
            duration=0.05)
        button_animate += Animation(
            pos_hint={"x": 0.02, "top": 0.80},
            duration=0.1)
        button_animate.start(widget)


# -------- \/ BEN'S CODE \/ --------#
# -------- SCREEN MANAGER  -------- #


class WindowManager(ScreenManager):
    if int(datetime.now().strftime("%H%M")) >=\
       600 and int(datetime.now().strftime("%H%M")) < 900:
        timeFileVar = "morning_theme"
        timeThemeColour = [0, 0, 0, 1]
        timeThemeAltColour = [1, 1, 1, 1]
    elif (int(datetime.now().strftime("%H%M")) >= 900 and
          int(datetime.now().strftime("%H%M")) < 1300):
        timeFileVar = "mid_day_theme"
        timeThemeColour = [0, 0, 0, 1]
        timeThemeAltColour = [1, 1, 1, 1]
    elif (int(datetime.now().strftime("%H%M")) >= 1300 and
          int(datetime.now().strftime("%H%M")) < 1700):
        timeFileVar = "afternoon_theme"
        timeThemeColour = [0, 0, 0, 1]
        timeThemeAltColour = [1, 1, 1, 1]
    elif (int(datetime.now().strftime("%H%M")) >= 1700 and
          int(datetime.now().strftime("%H%M")) < 2100):
        timeFileVar = "evening_theme"
        timeThemeColour = [0, 0, 0, 1]
        timeThemeAltColour = [1, 1, 1, 1]
    elif (int(datetime.now().strftime("%H%M")) >= 2100 and
          int(datetime.now().strftime("%H%M")) < 2400 or
          int(datetime.now().strftime("%H%M")) >= 0 and
          int(datetime.now().strftime("%H%M")) < 600):
        timeFileVar = "night_theme"
        timeThemeColour = [0.8, 0.8, 0.8, 1]
        timeThemeAltColour = [0.8, 0.8, 0.8, 1]


# -------- BUILDING THE APP -------- #

kv = Builder.load_file("Contact Tracker.kv")


class RightTrackApp(App):
    def build(self):
        return kv


class RightTrackApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    RightTrackApp().run()
