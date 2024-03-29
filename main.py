import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY:
    print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    exit(1)

if not ANTHROPIC_API_KEY:
    print("Anthropic API key not found. Please set the ANTHROPIC_API_KEY environment variable.")
    exit(1)

if not TELEGRAM_BOT_TOKEN:
    print("Telegram Bot token not found. Please set the TELEGRAM_BOT_TOKEN environment variable.")
    exit(1)

# Set up OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Set up Anthropic client
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Function to create a chat completion with OpenAI
def create_chat_completion(model, messages):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
        n=1,
        stop=None,
        presence_penalty=0,
        frequency_penalty=0,
    )
    return response

# Function to generate an image with OpenAI
def generate_image(model, prompt, size="1024x1024", quality="standard"):
    response = openai_client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )
    return response.data[0].url

# Function to generate a response with Anthropic
def generate_anthropic_response(conversation, model):
    response = anthropic_client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=0.0,
        system="You are a helpful assistant.",
        messages=conversation
    )
    
    # Concatenate the text content of all ContentBlock objects
    response_text = ""
    for content_block in response.content:
        response_text += content_block.text
    return response_text

# Function to save messages to JSON and TXT files
def save_messages(user_id, messages, filename):
    with open(f"{filename}_{user_id}.json", "w") as f:
        json.dump(messages, f, indent=2)
    with open(f"all_conversations_{user_id}.txt", "a") as f:
        for message in messages:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} | {message['role']}: {message['content']}\n")

# Function to load messages from JSON file
def load_messages(user_id, filename):
    try:
        with open(f"{filename}_{user_id}.json", "r") as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = []
    return messages

# Telegram bot command handlers
async def start_command(update, context):
    user_id = update.effective_user.id
    context.user_data['conversation'] = load_messages(user_id, "chat_history")
    context.user_data['image_model'] = None  # Disable image generation by default
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the AI Conversation Bot! Send me a message to start chatting.")

async def new_conversation_command(update, context):
    user_id = update.effective_user.id
    save_messages(user_id, context.user_data['conversation'], "chat_history")
    context.user_data['conversation'] = []
    context.user_data['image_model'] = None  # Disable image generation by default
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Starting a new conversation.")

async def opus_command(update, context):
    context.user_data['model'] = 'claude-3-opus-20240229'
    context.user_data['image_model'] = None  # Disable image generation
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to Claude 3 Opus model.")

async def sonnet_command(update, context):
    context.user_data['model'] = 'claude-3-sonnet-20240229'
    context.user_data['image_model'] = None  # Disable image generation
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to Claude 3 Sonnet model.")

async def haiku_command(update, context):
    context.user_data['model'] = 'claude-3-haiku-20240307'
    context.user_data['image_model'] = None  # Disable image generation
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to Claude 3 Haiku model.")

async def gpt35_command(update, context):
    context.user_data['model'] = 'gpt-3.5-turbo'
    context.user_data['image_model'] = None  # Disable image generation
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to GPT-3.5-turbo model.")

async def gpt4_command(update, context):
    context.user_data['model'] = 'gpt-4'
    context.user_data['image_model'] = None  # Disable image generation
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to GPT-4 model.")

async def gpt4turbo_command(update, context):
    context.user_data['model'] = 'gpt-4-turbo-preview'
    context.user_data['image_model'] = None  # Disable image generation
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Switched to GPT-4-turbo-preview model.")

async def dalle2_command(update, context):
    context.user_data['image_model'] = 'dall-e-2'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send me a prompt to generate a DALL-E 2 image.")

async def dalle3_command(update, context):
    context.user_data['image_model'] = 'dall-e-3'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Send me a prompt to generate a DALL-E 3 image.")

async def help_command(update, context):
    help_text = "Available commands:\n" \
                "/start - Start a new conversation\n" \
                "/new - Start a new conversation\n" \
                "/opus - Switch to Claude 3 Opus model\n" \
                "/sonnet - Switch to Claude 3 Sonnet model\n" \
                "/haiku - Switch to Claude 3 Haiku model\n" \
                "/gpt35 - Switch to GPT-3.5-turbo model\n" \
                "/gpt4 - Switch to GPT-4 model\n" \
                "/gpt4turbo - Switch to GPT-4-turbo-preview model\n" \
                "/dalle2 - Switch to DALL-E 2 model\n" \
                "/dalle3 - Switch to DALL-E 3 model\n" \
                "/help - List all available commands"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

async def message_handler(update, context):
    if update.message:
        user_id = update.effective_user.id
        username = update.effective_user.username
        prompt = update.message.text
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        model = context.user_data.get('model', 'gpt-3.5-turbo')
        image_model = context.user_data.get('image_model', None)
        
        try:
            conversation = context.user_data.setdefault('conversation', [])
            
            if model.startswith('claude'):
                response = generate_anthropic_response(conversation + [{"role": "user", "content": prompt}], model)
            elif model.startswith('gpt'):
                response = create_chat_completion(model, conversation + [{"role": "user", "content": prompt}])
                response = response.choices[0].message.content
            
            conversation.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response}
            ])
            
            if image_model is None:
                await send_response(update, context, response)
            elif image_model == 'dall-e-2':
                image_url = generate_image('dall-e-2', prompt)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{prompt.replace(' ', '_')}_{timestamp}.png"
                
                if not os.path.exists("generated"):
                    os.makedirs("generated")
                
                response = requests.get(image_url)
                with open(os.path.join("generated", filename), "wb") as f:
                    f.write(response.content)
                
                with open(os.path.join("generated", filename), "rb") as f:
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)
            elif image_model == 'dall-e-3':
                image_url = generate_image('dall-e-3', prompt)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{prompt.replace(' ', '_')}_{timestamp}.png"
                
                if not os.path.exists("generated"):
                    os.makedirs("generated")
                
                response = requests.get(image_url)
                with open(os.path.join("generated", filename), "wb") as f:
                    f.write(response.content)
                
                with open(os.path.join("generated", filename), "rb") as f:
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)
            save_messages(user_id, conversation, "chat_history")
        except Exception as e:
            await send_error_message(update, context, f"Oops, something went wrong: {str(e)}")
            print(f"Error: {e}")
    else:
        print("No message received.")

async def send_response(update, context, response):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def send_error_message(update, context, error_message):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start_command)
    application.add_handler(start_handler)
    
    new_conversation_handler = CommandHandler('new', new_conversation_command)
    application.add_handler(new_conversation_handler)
    
    opus_handler = CommandHandler('opus', opus_command)
    application.add_handler(opus_handler)
    
    sonnet_handler = CommandHandler('sonnet', sonnet_command)
    application.add_handler(sonnet_handler)
    
    haiku_handler = CommandHandler('haiku', haiku_command)
    application.add_handler(haiku_handler)
    
    gpt35_handler = CommandHandler('gpt35', gpt35_command)
    application.add_handler(gpt35_handler)
    
    gpt4_handler = CommandHandler('gpt4', gpt4_command)
    application.add_handler(gpt4_handler)
    
    gpt4turbo_handler = CommandHandler('gpt4turbo', gpt4turbo_command)
    application.add_handler(gpt4turbo_handler)
    
    dalle2_handler = CommandHandler('dalle2', dalle2_command)
    application.add_handler(dalle2_handler)
    
    dalle3_handler = CommandHandler('dalle3', dalle3_command)
    application.add_handler(dalle3_handler)
    
    help_handler = CommandHandler('help', help_command)
    application.add_handler(help_handler)
    
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    application.add_handler(message_handler)
    
    application.run_polling()
    print("AI Conversation Bot started. Press Ctrl+C to stop.")