# Streamlit Video Viewer Frontend

This project is a Streamlit-based frontend for a video viewer application. It provides an interactive interface for users to view and interact with video content.

## Project Structure

```
streamlit-frontend
├── src
│   ├── app.py                # Main entry point for the Streamlit application
│   └── components
│       └── __init__.py       # Initializes the components package
├── requirements.txt          # Lists the dependencies for the project
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd streamlit-frontend
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Start the Streamlit application by running:
   ```
   streamlit run src/app.py
   ```

## Usage

Once the application is running, you can access it in your web browser at `http://localhost:8501`. The interface will allow you to view and interact with video content.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.