# URL Shortener

This is a simple URL shortener web application built with Python and Flask.

## Features

- Shorten long URLs into shorter, more manageable links.
- Track the number of times each shortened URL has been accessed.
- User authentication system to allow users to manage their URLs.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- HTML/CSS
- Bootstrap

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/url-shortener.git
   ```

2. Navigate to the project directory:

   ```bash
   cd url-shortener
   ```

3. Install dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file in the project root directory and define the following variables:

   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///site.db
   ```

5. Run the application:

   ```bash
   python app.py
   ```

   The application should now be running on http://localhost:5000.

## Deployment

The application can be deployed to platforms like Heroku for production use. Ensure to set the appropriate environment variables for production deployment.
