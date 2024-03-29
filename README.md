# AI Telegram Chatbot

This is a Telegram bot that allows you to converse with the AI assistant Claude from Anthropic, as well as use the GPT-3.5-turbo, GPT-4, and GPT-4-turbo-preview models from OpenAI. Additionally, the bot can generate images using the DALL-E 2 and DALL-E 3 models.

## Features

- Conversation with Anthropic's Claude AI assistant
- Conversation with OpenAI's GPT-3.5-turbo, GPT-4, and GPT-4-turbo-preview models
- Image generation using DALL-E 2 and DALL-E 3 models
- Ability to switch between different models
- Saving of conversation history

## Requirements

- Python 3.7 or higher
- Telegram bot token
- Anthropic API key
- OpenAI API key

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/masllsam/ai_telegram.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add your API keys and Telegram bot token:

   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   OPENAI_API_KEY=your_openai_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

4. Run the bot:

   ```
   python main.py
   ```

## Usage

The bot supports the following commands:

- `/start`: Start a new conversation
- `/new`: Start a new conversation
- `/opus`: Switch to Claude 3 Opus model
- `/sonnet`: Switch to Claude 3 Sonnet model
- `/haiku`: Switch to Claude 3 Haiku model
- `/gpt35`: Switch to GPT-3.5-turbo model
- `/gpt4`: Switch to GPT-4 model
- `/gpt4turbo`: Switch to GPT-4-turbo-preview model
- `/dalle2`: Switch to DALL-E 2 model
- `/dalle3`: Switch to DALL-E 3 model
- `/help`: List all available commands

To generate an image, simply send a message to the bot while the DALL-E 2 or DALL-E 3 model is selected.

## License

This project is licensed under the [MIT License](LICENSE).
