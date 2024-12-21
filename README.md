# Discord Daily Reminder Bot

A Discord bot that sends daily reminders at 7 AM (Singapore time) with specific messages for each day of the week.

## Setup

1. Create a Discord Bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Copy the bot token (you'll need this later)
   - Enable "Message Content Intent" under Privileged Gateway Intents

2. Add Bot to Your Server:
   - In the Developer Portal, go to "OAuth2" → "URL Generator"
   - Select scopes: `bot`
   - Select permissions: `Send Messages`, `View Channels`
   - Copy the generated URL and open it in a browser to add the bot to your server

3. Get Channel ID:
   - In Discord, enable Developer Mode (Settings → App Settings → Advanced → Developer Mode)
   - Right-click the channel where you want the bot to send messages
   - Click "Copy ID"

4. Set Environment Variables:
   - Create a `.env` file based on `.env.example`
   - Add your bot token and channel ID:
     ```
     DISCORD_TOKEN=your_bot_token_here
     CHANNEL_ID=your_channel_id_here
     ```

## Deploy to Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy to Vercel:
   ```bash
   vercel login
   vercel
   ```

3. Set Environment Variables in Vercel:
   - Go to your project settings in Vercel dashboard
   - Add the following environment variables:
     - `DISCORD_TOKEN`
     - `CHANNEL_ID`

## Features

- Sends daily reminders at 7 AM Singapore time
- Different messages for each day of the week
- Automatically mentions relevant roles
- Includes study tasks and shadowing exercises

## Files

- `bot.py`: Main bot code with message scheduling
- `api/index.py`: Vercel serverless function
- `vercel.json`: Vercel deployment configuration
- `requirements.txt`: Python dependencies
