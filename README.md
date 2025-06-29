# Glitter Client

this was after one semester of learning python in magshimim. befor i did the client i had to find 10 vulnerabilities like a pentester.

This project is a Python-based client for interacting with a social networking server called **Glitter**. It allows users to perform various actions like logging in, posting content (called "glits"), liking posts, adding comments, viewing user history, and sending/approving friendship requests — all through a socket connection using a custom protocol.

## 📦 Features

- **Login/Logout** – Authenticate users using username and password with a simple checksum-based verification.
- **Add Likes** – Automatically send 30 likes to a selected glit (post).
- **Post Glit** – Publish a new post with user-selected background and font colors.
- **Friendship** – Send and immediately approve friendship requests.
- **Watch History** – View posting history of a user by their ID.
- **Add Comment** – Add a comment to a specific glit.

## 🛠️ Technologies Used

- **Python 3**
- **Socket Programming**
- **Custom Protocol using delimiters**
