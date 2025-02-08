from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QListWidget

# Demo user database (username -> (password, role))
demo_users = {
    "admin": ("password123", "teacher"),
    "gabrielle": ("tartanhacks2025", "student"),
    "mrsmith": ("teach2025", "teacher"),
    "student1": ("studypass", "student"),
}

# Sample recordings available to students
available_recordings = [
    "Lesson 1 - Introduction to Python",
    "Lesson 2 - Data Structures",
    "Lesson 3 - Object-Oriented Programming",
    "Lesson 4 - Web Development Basics",
]

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login Form")

        # Layout
        layout = QVBoxLayout()

        # Username input
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # Password input
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        layout.addWidget(self.password_input)

        # Login Button
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username in demo_users and demo_users[username][0] == password:
            role = demo_users[username][1]
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}! You are logged in as a {role}.")
            self.open_dashboard(role)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_dashboard(self, role):
        if role == "teacher":
            self.teacher_dashboard = TeacherDashboard()
            self.teacher_dashboard.show()
        else:
            self.student_dashboard = StudentDashboard()
            self.student_dashboard.show()
        self.close()  # Close login window

class TeacherDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher Dashboard")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome, Teacher!"))
        self.setLayout(layout)

class StudentDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Dashboard")
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Available Recordings:"))

        # List of recordings
        self.recordings_list = QListWidget()
        self.recordings_list.addItems(available_recordings)
        layout.addWidget(self.recordings_list)

        # Watch button
        self.watch_button = QPushButton("Watch Recording")
        self.watch_button.clicked.connect(self.watch_recording)
        layout.addWidget(self.watch_button)

        self.setLayout(layout)

    def watch_recording(self):
        selected_item = self.recordings_list.currentItem()
        if selected_item:
            QMessageBox.information(self, "Now Playing", f"You are watching: {selected_item.text()}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a recording to watch.")

if __name__ == "__main__":
    app = QApplication([])
    window = LoginApp()
    window.show()
    app.exec()
