# TartanHacks

Our project is a video management and editing platform aimed at educators, providing functionality for them to record, edit, and select videos for student viewing. The core features of the app focus on video privacy, editing capabilities, and content selection for educational purposes.

1. Video Recording and Editing:
Teachers can record videos, with the added ability to edit them. The editing process involves removing people from the frame of the whiteboard, ensuring that no one obstructs the educational content.
OpenCV is used for the person eliminator tool, which helps to process the unedited video and create a cleaner, unobstructed version by removing individuals from the scene. This allows for a more focused learning experience for students.
2. Video Management:
Teachers have access to both the unedited video, which includes all people in the frame, and the edited video, where the people are removed.
Teachers can decide which version of the video (edited or unedited) to publish to students, offering flexibility in how the content is shared.
3. Student Dashboard:
Students are given access to the final published videos, whether edited or unedited, providing them with a view of the content that best supports their learning needs.
4. Privacy and User Control:
By allowing teachers to choose whether to post the edited or unedited version of the video, your platform gives educators control over the content they share, with a strong focus on privacy and clarity in educational materials.

Key Technologies:
PyQt5 for creating the GUI that handles user interactions, including logging in, navigating dashboards, and managing video content.
OpenCV for implementing the person eliminator, which edits the video to remove people from the whiteboard area.
Video File Management for storing, editing, and displaying both the unedited and edited versions of videos.

Goals:
The platform aims to improve the learning experience by offering a streamlined way for educators to manage and customize video content.
The key advantage is video clarity, as teachers can remove distractions (people) in the video, helping students focus on the core content.
Flexibility for teachers to decide the level of privacy and focus in the content they share with students.
Overall, this project provides a dynamic solution for educators to efficiently manage their teaching videos, edit them for clarity, and ensure that students get the best possible learning experience through focused, unobstructed content.
