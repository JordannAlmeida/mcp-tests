# AI Interact

AI Interact is a Streamlit-based application that allows users to interact with the Gemini AI model for generating conversational responses. The application is designed to provide a simple and intuitive interface for chatting with the AI.

## Features

- **Chat Interface**: Engage in a conversation with the Gemini AI model.
- **Session Management**: Start new chat sessions to reset the conversation context.
- **Error Handling**: Provides clear error messages for missing API keys or initialization issues.

## Setup and Running

### Prerequisites

- Python 3.12 or higher
- A valid Google API key for accessing the Gemini model

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-interact
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the `.env` file**:
   - Create a `.env` file in the `ai-interact` directory.
   - Add your Google API key:
     ```
     GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
     ```

### Running the Application

1. **Start the Streamlit app**:
   ```bash
   ENVIRONMENT=local streamlit run app.py
   ```

   - Replace `local` with the desired environment (e.g., `production`) to load the appropriate `.env` file.

2. **Access the application**:
   - Open your browser and go to `http://localhost:8501`.

## File Structure

- `app.py`: The main entry point for the Streamlit application.
- `chat_logic.py`: Contains the logic for interacting with the Gemini AI model.
- `requirements.txt`: Lists the Python dependencies.
- `.env`: Stores the Google API key (not included in the repository).

## Environment Variables

- `GOOGLE_API_KEY`: The API key required to access the Gemini AI model. This must be set in the `.env` file.

## Usage

1. Enter your query in the chat input field.
2. View the AI's response in the chat interface.
3. Use the "New Chat" button in the sidebar to reset the conversation.

## Troubleshooting

- **API Key Not Found**: Ensure the `.env` file is correctly set up with a valid `GOOGLE_API_KEY`.
- **Unexpected Errors**: Check the console logs for detailed error messages.

## License

This project is licensed under the MIT License. See the LICENSE file for details.