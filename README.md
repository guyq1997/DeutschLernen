# German Vocabulary Learning App

A web-based application designed to help users learn and track their German vocabulary progress. The application allows users to manage their vocabulary list, track mastery levels, and systematically study new words.

## Features

- **Dashboard Overview**
  - Total words count
  - Mastered words tracking
  - Words in learning progress
  - New/unfamiliar words
  - Quick word addition

- **Word Management**
  - Add new words with translations
  - Track mastery status for each word
  - Search functionality
  - Categorize words by mastery level

- **Study System**
  - Progressive learning approach
  - Word mastery tracking
  - Reinforcement of learning words

## Technical Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (through SQLAlchemy)
- **Template Engine**: Jinja2

## Installation

1. Clone the repository: 
bash
git clone [repository-url]
cd german-vocabulary-app

2. Create a virtual environment and activate it:
bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:
bash
pip install -r requirements.txt

4. Initialize the database:
bash
flask db upgrade

5. Run the application:
bash
flask run

The application will be available at `http://localhost:5000`

## Project Structure

german-vocabulary-app/
├── app/
│ ├── templates/
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── words.html
│ │ ├── add_word.html
│ │ └── study_words.html
│ ├── main.py
│ ├── models.py
│ └── database.py
├── static/
│ └── styles.css
├── requirements.txt
└── README.md

## Usage

1. **Adding Words**
   - Click on "Neue Wörte" (New Words) on the dashboard
   - Enter the German word and its translation
   - Submit to add to your vocabulary list

2. **Tracking Progress**
   - Dashboard shows overview of vocabulary status
   - Words are categorized as:
     - Gemeisterte (Mastered)
     - Lernende (Learning)
     - Fremde (Unfamiliar)

3. **Studying Words**
   - Use the search functionality to find specific words
   - Update word status as you learn
   - Focus on reinforcing words in the "Learning" category

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
This README provides a comprehensive overview of the application, including its features, setup instructions, and usage guidelines. You might want to customize the following elements:
Add the actual repository URL in the installation section
Add any specific configuration requirements
Include any additional setup steps specific to your deployment environment
Add or modify the license information according to your preferences
Add any additional sections relevant to your project (e.g., Testing, Deployment, etc.)