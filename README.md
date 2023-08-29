# Practice Platform With Auto Algorithm Grading

- A user-friendly web application designed to help individuals enhance their logical thinking skills through solving algorithmic problems.

## Features

- **Auto algorithm grading:** Upon submission, the database stores who sent it, what problem it's for, and the code itself. Then, it talks to the Evaluator API, sharing details like the problem ID, the code, how many tests to run, and how long it should take. This API tests the code using Linux commands and gives back a report with the results, which are then saved in the database.
- **Detailed problem pages:** Featuring an intuitive interface with problem lists, detailed problem descriptions, and an interactive code editor.
- **Secure user functions:** Implemented a secure user authentication for login and registration, allowing each user to have a profile with a picture and a description.

## Technologies
- Django
- Python
- JavaScript
- Bootstrap
