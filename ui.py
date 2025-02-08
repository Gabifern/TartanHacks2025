from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QListWidget
from PyQt5.QtGui import QPalette, QColor

# Demo user database (username -> (password, role))
demo_users = {
    "admin": ("password123", "teacher"),
    "gabrielle": ("tartanhacks2025", "student"),
    "mrsmith": ("teach2025", "teacher"),
    "student1": ("studypass", "student"),
}

# Video storage
published_videos = [
    "Lesson 1 - Introduction to Python",
    "Lesson 2 - Data Structures",
]
unpublished_videos = [
    "Lesson 3 - Object-Oriented Programming (Draft)",
    "Lesson 4 - Web Development Basics (Draft)",
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

        # Buttons
        self.view_student_interface_btn = QPushButton("View Student Interface")
        self.record_video_btn = QPushButton("Record New Video")
        self.view_published_videos_btn = QPushButton("View Published Videos")
        self.view_unpublished_videos_btn = QPushButton("View Unpublished Video Library")

        # Connect buttons
        self.view_student_interface_btn.clicked.connect(self.view_student_interface)
        self.record_video_btn.clicked.connect(self.record_video)
        self.view_published_videos_btn.clicked.connect(self.view_published_videos)
        self.view_unpublished_videos_btn.clicked.connect(self.view_unpublished_videos)

        # Add buttons to layout
        layout.addWidget(self.view_student_interface_btn)
        layout.addWidget(self.record_video_btn)
        layout.addWidget(self.view_published_videos_btn)
        layout.addWidget(self.view_unpublished_videos_btn)

        self.setLayout(layout)

    def view_student_interface(self):
        self.student_dashboard = StudentDashboard()
        self.student_dashboard.show()

    def record_video(self):
        QMessageBox.information(self, "Recording", "Recording functionality will be implemented.")

    def view_published_videos(self):
        self.video_library = VideoLibrary("Published Videos", published_videos)
        self.video_library.show()

    def view_unpublished_videos(self):
        self.video_library = VideoLibrary("Unpublished Videos", unpublished_videos)
        self.video_library.show()

class StudentDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Dashboard")
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Available Recordings:"))

        # List of published videos
        self.recordings_list = QListWidget()
        self.recordings_list.addItems(published_videos)
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

class VideoLibrary(QWidget):
    def __init__(self, title, videos):
        super().__init__()
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))

        # List of videos
        self.video_list = QListWidget()
        self.video_list.addItems(videos)
        layout.addWidget(self.video_list)

        self.setLayout(layout)
    
if __name__ == "__main__":
    app = QApplication([])
    palette=QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))  

    window = LoginApp()
    window.show()
    app.exec()
