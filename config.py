BOT_TOKEN = 'YOUR_TOKEN_BOT'  # string
api_id = 'YOUR API ID'  # int
api_hash = 'YOUR API HASH'  # string
Group_ID = 'YOUR GROUP ID'  # int

db_user = 'DB_USERNAME'
db_pass = 'DB_PASSWORD'
db_db = 'DB_DATABASE'

# PREDEFINED VARS #
text_rules = '((text2)|(text1))'
group_active = 1
admins = []
users = []
data = {}
sleep_tm = 24
wake_tm = 9
WELCOME_MSG = "WELCOME TO THIS GROUP\nBE HAPPY"
ENTER_NAME = "Enter Your Name: "
ENTER_PLACE = "Enter Your Place: "
ACCOUNT_EXISTS = "Account Exists!"
ACCOUNT_SUCCESS = "Account Success!"
MAIN_MENU = "Main Menu: "
SLEEP_MSG = "Enter Sleep Time Like 24:"
WAKE_MSG = "Enter Wake Up Time Like 8:"
GROUP_STOP_MSG = "Group sending message disabled"
GROUP_START_MSG = "Group sending message enabled"
MSG_TO_GROUP_STOP = "Sending message stop"
MSG_TO_GROUP_START = "Sending message start"
# PREDEFINED VARS #

BACK_BTN = '⬅️'
HOME_BTN = '🏠'
ADMIN_SLEEP_BTN = 'Sleeping Time'
ADMIN_WAKE_BTN = 'Waking Time'
ADMIN_STOP_BTN = 'Stop Group'
ADMIN_EXCEL_BTN = 'Excel File'
REGISTER_BTN = 'Register'

admin_reply_keyboard = [[BACK_BTN, HOME_BTN], [ADMIN_SLEEP_BTN, ADMIN_WAKE_BTN], [ADMIN_STOP_BTN, ADMIN_EXCEL_BTN]]

# FUNCTIONS #
admins_file = open('group_admin.csv', "r")
lines = admins_file.readlines()
for line in lines:
    admins.append(line.strip())
admins_file.close()

rules_file = open('rules.txt', "r")
temp_rules = rules_file.readlines()
rules = ''
for rl in temp_rules:
    rules = rules + str(rl)
