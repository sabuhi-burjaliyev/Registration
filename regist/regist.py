import json
from random import randint

class System():
    def __init__(self):
        self.status = True
        self.data = self.getdata()

    def getdata(self):
        try:
            with open('regist.json','r') as document:
                data = json.load(document)
        except:
            with open('regist.json','w') as document:
                document.write('{}')

        with open('regist.json','r') as document:
            data = json.load(document)

        return data
    def showmenu(self):
        print("""
***** Welcome to BSecurity registration ****

1) Log in
2) Sign up
3) Forget password
4)Exit system        
        """)

    def menuchoice(self):
        while True:
            try:
                choice = int(input('Enter your operation :'))
                while choice < 1 or choice > 4:
                    choice = int(input('Choice must be between (1-4)'))
                break
            except:
                print('Enter a number please !')
        return choice
    def run(self):
        self.showmenu()
        choice = self.menuchoice()
        if choice == 1:
            self.login()
        if choice == 2:
            self.signup()
        if choice == 3:
            self.forgotpassword()
        if choice == 4:
            self.exit()

    def login(self):
        username = input('Enter your username :')
        password = input('Enter your password :')
        if self.check(username,password):
            print('You logged in successfully !')
            self.status = False
        else:
            print('Incorrect username or password !')


    def signup(self):
        username = input('Enter username :')
        password = input('Enter password :')
        mail = input('Enter mail :')
        activation = self.sendactivation()
        enteredactivation = input('Enter activation code :')
        if enteredactivation == str(activation):
            self.regist(username,password,mail)
        else:
            print('Wrong activation !')

    def regist(self,username,password,mail):
        self.data = self.getdata()
        try:
            for user in self.data['users']:
                if user['mail'] == mail:
                    print('There is already a user with that email !')
                    break
            self.data['users'].append({'username':username,'password':password,'mail':mail})
        except:
            self.data['users'] = []
            self.data['users'].append({'username':username,'password':password,'mail':mail})

        with open('regist.json','w') as document:
            json.dump(self.data,document)

    def sendactivation(self):
        with open('activation.txt','w') as document:
            activation = randint(1000,9999)
            document.write(str(activation))
        return activation

    def forgotpassword(self):
        self.data = self.getdata()
        try:
            mail = input('Enter your mail :')
            for user in self.data['users']:
                if user['mail'] == mail:
                    activation = self.sendactivation()
                    enteredactivation = input('Enter activation code :')
                    if str(activation) == enteredactivation:
                        while True:
                            password = input('Enter new password :')
                            newpassword = input('Enter password again :')
                            if password == newpassword:
                                user['password'] = password
                                with open('regist.json','w') as document:
                                    json.dump(self.data,document)
                                return None
                            else:
                                print('Passwords don\'t match. Enter again')
                    else:
                        print('Wrong activation code !')
                        return None

            print('There is no registered mail !')
        except:
            print('There is no registered mail !')
    def check(self,username,password):
        self.data =self.getdata()
        try:
            for user in self.data['users']:
                if user['username'] == username and user['password'] == password:
                    return True
        except:
            return False

        return False


    def exit(self):
        self.status = False

system = System()

while system.status:
    system.run()