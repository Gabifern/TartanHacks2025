import os
import subprocess
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QListWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
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
unpublished_video_path = "unpublished_videos"

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login Form")
        self.resize(600, 400)

        # Layout
        layout = QVBoxLayout()

        # Username input
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Resizable input
        layout.addWidget(self.username_input)

        # Password input
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Resizable input
        layout.addWidget(self.password_input)

        # Login Button
        self.login_btn = QPushButton("Login")
        self.login_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Resizable button
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
        self.resize(800, 600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome, Teacher!"))

        # Buttons with resizing
        self.view_student_interface_btn = QPushButton("View Student Interface")
        self.view_student_interface_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Resizable button
        self.record_video_btn = QPushButton("Record New Video")
        self.record_video_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Resizable button
        self.view_published_videos_btn = QPushButton("View Published Videos")
        self.view_published_videos_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Resizable button
        self.view_unpublished_videos_btn = QPushButton("View Unpublished Video Library")
        self.view_unpublished_videos_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Resizable button

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
        # Here we call camera.py using subprocess to start recording
        save_folder="unpublished_videos"
        os.makedirs(save_folder, exist_ok=True)
        try:
            # Start the recording process
            subprocess.Popen([sys.executable, 'camera.py', save_folder])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to start camera: {e}")

    def view_published_videos(self):
        self.video_library = VideoLibrary("Published Videos", published_videos)
        self.video_library.show()

    def view_unpublished_videos(self):
        unpublished_videos = os.listdir("unpublished_videos")
        self.video_library = VideoLibrary("Unpublished Videos", unpublished_videos)
        self.video_library.show()
    



class StudentDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Dashboard")
        self.resize(800, 600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Available Recordings:"))

        # List of published videos
        self.recordings_list = QListWidget()
        self.recordings_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Resizable list widget
        self.recordings_list.addItems(published_videos)
        layout.addWidget(self.recordings_list)

        # Watch button with resizing
        self.watch_button = QPushButton("Watch Recording")
        self.watch_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Resizable button
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
    def __init__(self, title, videos, path=""):
        super().__init__()
        self.setWindowTitle(title)
        self.path = path
        self.videos = videos
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))

        # List of videos with resizing
        self.video_list = QListWidget()
        self.video_list.addItems(videos)
        layout.addWidget(self.video_list)

        # Add Watch Video button
        self.watch_button = QPushButton("Watch Video")
        self.watch_button.clicked.connect(self.watch_video)
        layout.addWidget(self.watch_button)
        
        self.setLayout(layout)


    def watch_video(self):
        selected_item = self.video_list.currentItem()
        if selected_item:
            video_file = selected_item.text().strip()
            video_path = os.path.abspath(os.path.join(self.path, "unpublished_videos", video_file))

            if os.path.exists(video_path):
                self.play_video(video_path)
            else:
                QMessageBox.warning(self, "Error", f"Video file not found: {video_path}")  # Debugging
        else:
            QMessageBox.warning(self, "No Selection", "Please select a video")

    def play_video(self, video_path):
        if os.path.exists(video_path):
            try:
                if sys.platform.startswith("win"):
                    os.startfile(video_path)  # Opens in Windows default media player
                elif sys.platform.startswith("darwin"):  # macOS
                    subprocess.run(["open", video_path])
                else:  # Linux
                    subprocess.run(["xdg-open", video_path])
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not open video: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", f"Video file not found: {video_path}")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QSizePolicy

    app = QApplication([])

    # Set the application's palette for the background color
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#beebee"))
    app.setPalette(palette)

    # Start the login window
    window = LoginApp()
    window.show()
    app.exec()