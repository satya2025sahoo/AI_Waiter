---

# AI Waiter

AI Waiter is a voice-based system that allows customers to place orders in a restaurant by speaking. This AI assistant uses Google's Gemini model with RAG (Retrieval-Augmented Generation) to fetch data from a vector database and provide efficient responses. The system is optimized for devices without a GPU and stores local data for faster interactions.

## Features
- **Voice Interaction**: Customers can place orders through voice commands, with the system processing natural language using speech recognition.
- **AI-driven Responses**: The AI uses the Gemini model and ChromaDB for fast data retrieval and responses.
- **Memory Capabilities**: LlamaIndex is used to recall previous interactions and maintain conversation context.
- **Cross-Platform Compatibility**: The system is designed to run on machines without GPUs, ensuring broad compatibility.

## Project Structure

- `AI.py`: Contains the core AI logic using Gemini and ChromaDB for data retrieval and interaction with customers.
- `SpeechToText.py`: Handles the conversion of customer speech to text using speech recognition libraries.
- `app.py`: Manages the overall flow of the system, integrating speech recognition, AI, and response mechanisms.
- `voice_service.py`: Responsible for text-to-speech conversion, enabling the AI to respond verbally to the customer.
- `restaurant_file.txt`: Stores the restaurant menu items and prices, which are used by the AI to process orders.

## Workflow

1. **Voice Input**: The system listens to the customer’s voice input using the `SpeechToText.py` module.
2. **Order Processing**: The spoken input is converted to text and processed by the AI (via `AI.py`) to match the relevant menu items.
3. **Response Generation**: The AI fetches the corresponding order details from the `restaurant_file.txt` and responds using `voice_service.py` to communicate the order and price back to the customer.
4. **Memory Retention**: Previous orders or interactions are stored using LlamaIndex for continuity in conversations, enhancing the user experience.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/AI_Waiter.git
   ```

2. Navigate to the project directory:
   ```bash
   cd AI_Waiter
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Requirements

Refer to `requirements.txt` for the list of necessary packages, including:
- `openai`
- `chromadb`
- `pyttsx3` for text-to-speech
- `speech_recognition`
- `etc.`

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
