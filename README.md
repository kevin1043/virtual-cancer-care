# Virtual Cancer Care

Virtual Cancer Care is a web-based application that utilizes three prediction-based models to predict the chances of lung cancer, breast cancer, and ALL (leukemia) cancer. The leukemia cancer prediction model is based on advanced image classification technology, making it one of the most advanced cancer prediction tools available.

## Introduction

The Virtual Cancer Care website is currently under development and provides prediction tools for lung cancer, breast cancer, and ALL (leukemia) cancer. Users are required to sign up and log in to access the prediction tools, ensuring confidentiality and privacy. The website also features a unique report generation feature that allows users to generate a PDF report summarizing the chances of predictions made by the website. Additionally, a dashboard is available for users to log their predictions and track their health progress over time.

## Tech Stack

- Django 3.2: A high-level Python web framework for building web applications.
- Python 3.6: The programming language used for developing the application.
- TensorFlow: An open-source machine learning framework used for the leukemia cancer prediction model based on image classification.
- Djongo: A database connector that allows Django to use MongoDB as the backend database.


## Installation

To run the Virtual Cancer Care project locally, follow these steps in your terminal:

```bash
# Install Python 3.6 or later
pip install python==3.6

# Install Django 3.2
pip install django==3.2

# Install TensorFlow
pip install tensorflow

# Install Djongo
pip install djongo

# Clone the repository from GitHub
git clone <repository-url>

# Navigate to the project directory
cd Virtual-Cancer-Care

# Run the Django development server
python manage.py runserver

Note: Make sure to update the settings.py file with appropriate database credentials if you wish to use a MongoDB backend using Djongo.

## Disclaimer

It is important to note that the predictions made by Virtual Cancer Care are based on the available dataset and should not be taken as a definitive diagnosis. The website is currently under development and should not be considered as a substitute for professional medical advice. Users are advised to consult a qualified healthcare provider for accurate cancer diagnosis and treatment options.

Thank you for your interest in Virtual Cancer Care. Feel free to reach out to us for any inquiries or suggestions.
