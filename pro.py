import socket
import random
from datetime import datetime
import hashlib
import requests
import json


SERVER_IP = "54.187.16.171"
SERVER_PORT = 1336
MAX_BUFFER = 1024
default_pass = "cyber"
color_list = ["black", "Gold", "SpringGreen", "MediumVioletRed", "OrangeRed", "DarkOrange", "Teal", "Violet", "White"]
search_type = ["SIMPLE", "WILDCARD", "ID"]

def search(connection):
    info = input("What would you like to search? ")
    print(search_type)
    type = input("Search type: ")
    data = f'{{"search_type":"{type}","search_entry":"{info}"}}'
    format_message_send(connection, 300, data)
    recv_print(connection)

def create_user():
    url = "http://cyber.glitter.org.il/users/"
    registration_code = input("registration_code: ")
    screen_name = input("screen_name: ")
    avatar = input("avatar: ")
    description = input("life motto: ")
    privacy = input("privacy: ")
    user_name = input("user_name (can be more than 30 letters): ")
    password = input("password: ")
    gender = input("gender: ")
    mail = input("mail: ")

    data = {
        "registration_code": registration_code,
        "user": {
            "screen_name": screen_name,
            "avatar": avatar,
            "description": description,
            "privacy": privacy,
            "id": -1,
            "user_name": user_name,
            "password": password,
            "gender": gender,
            "mail": mail
        }
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        print("User created successfully!")
    else:
        print(f"Failed to create user. Status code: {response.status_code}")

    print("Response content:")
    print(response.text)

"""
this function will find the password
input: none
output: none
"""
def find_pass():
    name = input("user name: ")
    code = culc_recovery_code(name)
    url = "http://cyber.glitter.org.il/password-recovery-code-request/"
    response_name = requests.post(url, json=name)

    url = "http://cyber.glitter.org.il/password-recovery-code-verification/"
    response = requests.post(url, json=code)
    print(response.text.replace('"', ''))

"""
this function will find the user password recovery code
input: the user name
output: none
"""
def culc_recovery_code(name):
    id = input("enter user id: ")

    now = datetime.now()

    digit_to_letter = {
    '0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E',
    '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J',
    '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O',
    '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T',
    '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y',
    '25': 'Z'
    }
    num_str = str(id)
    middle = ''.join(digit_to_letter[digit] for digit in num_str)
    current_date = now.strftime("%d%m")
    current_time = now.strftime("%H%M")
    data = [name, f"{current_date}{middle}{current_time}"]
    print("code: ",data)
    return data

"""
this function will dis approve friendship request
input: the socket
output: none 
"""
def disapprove_friend(connection):
    rejected = input("id of the rejected")
    disapprove = input("id of the receive")
    data = f"[{disapprove},{rejected}]"
    format_message_send(connection, 430, data)
    recv_print(connection)
"""
this function will unlike a post
input: the socket
output: none
"""
def unlike(connection):
    id = input("enter post id: ")
    format_message_send(connection, 720, id)
    recv_print(connection)


"""
this function will fund a cookie wi the user name
input: none
output: none
"""
def cookies():
    # Get the current date and time
    now = datetime.now()

    #get the user name
    name = input("user name: ")

    # Format the date and time
    current_date = now.strftime("%d%m%Y")
    current_time = now.strftime("%H%M")
    hash_object = hashlib.md5()

    # Encode the input string and update the hash object
    hash_object.update(name.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()
    cookie = f"{current_date}.{hex_dig}.{current_time}.{current_date}"
    print("cookie: ", cookie)


"""
this function will send a wrong login request and extract the checksum from the server answer
input: the socket and the user name
output: the checksum
"""
def extract_checksum(connection, userName):
    data = f'{{"user_name":"{userName}","password":"{default_pass}","enable_push_notifications":true}}'
    format_message_send(connection, 100, data)
    msg = recv_print(connection)
    checksum = msg.split(":")[1].split("{")[0].replace(' ', '')
    print(checksum)
    return checksum
"""
this function will fake the password and send the ligin request
input: the user name the  checksum and the socket
output: none
"""
def fake_pass(name, checksum, connection):
    pass_word = ""
    checksum = int(checksum)
    count = 0

    for char in name:
        checksum -= ord(char)

    print(f"Checksum after subtraction: {checksum}")

    num = 0
    while num < checksum:
        rand = random.randint(65, 90)
        pass_word += chr(rand)
        num += rand
        if checksum <= num:
            if num == checksum:
                break
            else:
                count += 1
                pass_word = pass_word[:-1]
                num -= rand
        if count == 20:
            pass_word = ""
            count = 0
            num = 0
    data = f'{{"user_name":"{name}","password":"{pass_word}","enable_push_notifications":true}}'
    format_message_send(connection, 100, data)
    recv_print(connection)
"""
this function will logout the user
input: the socket
output: none
"""
def logout(connection):
    id = input("Enter user ID: ")
    format_message_send(connection, 200, id)
    recv_print(connection)
"""
this function will add comment to a glit
input: the socket
output: none
"""
def add_comment(connection):
    glit_id = input("Enter glit ID: ")
    sender_id = input("Enter sender ID: ")
    user_name = input("Enter screen name: ")
    content = input("Enter content: ")
    date = input("Enter date: ")
    data = f'{{"glit_id":{glit_id},"user_id":{sender_id},"user_screen_name":"{user_name}","id":-1,"content":"{content}","date":"{date}"}}'
    format_message_send(connection, 650, data)
    recv_print(connection)
"""
this function will allow the user to view every feed history he wants
input: the socket
output: none
"""
def watch_history(connection):
    id = input("Enter the ID of the user you want to watch the history of: ")
    format_message_send(connection, 320, id)
    recv_print(connection)
"""
this function will send a friendship request and will apruve it immidietly
input: the socket
output: none
"""
def friendship(connection):
    sender_id = input("Enter request sender ID: ")
    receiver_id = input("Enter receiver ID: ")
    data = f"[{sender_id},{receiver_id}]"
    # Send the suggestion
    format_message_send(connection, 410, data)
    recv_print(connection)
    # Approve the suggestion
    format_message_send(connection, 420, data)
    recv_print(connection)
"""
this function will post a glit
input: the socket
output: none
"""
def post_glit(connection):
    feed_owner_id = input("Feed owner ID: ")
    publisher_id = input("Publisher ID: ")
    publisher_screen_name = input("Publisher screen name: ")
    publisher_avatar = input("Publisher avatar: ")
    print(", ".join(color_list))
    background_color = input("Background color: ")
    date = input("Date: ")
    content = input("Content: ")
    print(", ".join(color_list))
    font_color = input("Font color: ")

    data = f'{{"feed_owner_id":{feed_owner_id},"publisher_id":{publisher_id},"publisher_screen_name":"{publisher_screen_name}","publisher_avatar":"{publisher_avatar}","background_color":"{background_color}","date":"{date}","content":"{content}","font_color":"{font_color}","id":-1}}'

    format_message_send(connection, 550, data)
    recv_print(connection)
"""
this function will add likes to a glit
inpout: the socket
output: none
"""
def add_likes(connection):
    try:
        glit_id = int(input("Enter post ID: "))
        likes_amount = input("how many post would you want on the post? ")
        screen_name = input("Enter name to display: ")
        user_id = int(input("Enter user ID: "))
        message_data = f'{{"glit_id":{glit_id},"user_id":{user_id},"user_screen_name":"{screen_name}","id":-1}}'

        for count in range(int(likes_amount)):
            format_message_send(connection, "710", message_data)
            recv_print(connection)

    except ValueError:
        print("Invalid input! Please enter valid numeric values for Post ID and User ID.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Try Again!")
"""
this function will print the recuve messaage
input: the socket
output: the returned message
"""
def recv_print(connection):
    full_msg = connection.recv(MAX_BUFFER).decode()
    print(full_msg)
    return full_msg
"""
this function will format the message and will send it to the server
input: the socket, the message kind, the message data
output: the message
"""
def format_message_send(connection, message_id, message_data):
    message = f"{message_id}#{{gli&&er}}{message_data}##"
    print(message)
    connection.sendall(message.encode())
    return message

def main():
    try:
        userName = input("Enter user name: ")
        #connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            server_address = (SERVER_IP, SERVER_PORT)
            sock.connect(server_address)

            #fake the password
            checksum = extract_checksum(sock, userName)
            fake_pass(userName, checksum, sock)
            format_message_send(sock, 110, checksum)
            msg = recv_print(sock)
            #find the password
            start_index = msg.find('"password":"') + len('"password":"')
            end_index = msg.find('"', start_index)
            password = msg[start_index:end_index]
            #print it
            print("Password:", password)
            while True:
                choice = input("""
        [1] Add likes to a post
        [2] Post a glit
        [3] Suggest a friendship that will be approved immediately
        [4] Watch people's history
        [5] Add comment
        [6] Logout
        [7] Exit
        [8] get cookie by user name
        [9] unlike post
        [10] disapprove friendship request
        [11] get password with user name and id
        [12] create user
        [13] search with different search type 
                """)
                if choice == '1':
                    add_likes(sock)
                elif choice == '2':
                    post_glit(sock)
                elif choice == '3':
                    friendship(sock)
                elif choice == '4':
                    watch_history(sock)
                elif choice == '5':
                    add_comment(sock)
                elif choice == '6':
                    logout(sock)
                elif choice == '7':
                    break
                elif choice == '8':
                    cookies()
                elif choice == '9':
                    unlike(sock)
                elif choice == '10':
                    disapprove_friend(sock)
                elif choice == '11':
                    find_pass()
                elif choice == '12':
                    create_user()
                elif choice == '13':
                    search(sock)
                else:
                    print("Invalid choice! Please enter a valid number from the options above.")
    except ValueError as e:
        print(f"{e}")
    except ConnectionRefusedError:
        print("Connection refused. Please check the server configuration.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
