# Discord Bot for PTE Study Reminders

This Discord bot sends daily study reminders and practice materials for PTE Academic exam preparation.

## Setup on Glitch

1. Create a new project on Glitch
2. Upload these files to your Glitch project:
   - `bot.py` - The main bot code
   - `requirements.txt` - Python dependencies
   - `start.sh` - Script to install dependencies and start the bot

3. Set up environment variables in Glitch:
   - Click on "Tools" in the bottom left
   - Select "Environment Variables (.env)"
   - Add these variables:
     ```
     DISCORD_TOKEN=your_discord_bot_token
     CHANNEL_ID=your_channel_id
     ```

4. The bot will automatically:
   - Send daily reminders at 7 AM Vietnam time
   - Include practice materials and shadowing exercises
   - Mention relevant role groups for different exercises

## Features

- Daily study reminders with specific tasks
- Role mentions for different study groups
- Rotating shadowing exercise links
- Timezone set to Asia/Ho_Chi_Minh (Vietnam)
- Automatic message scheduling

## Commands

Currently, the bot runs on a schedule and doesn't have user commands. It will:
- Send a welcome message when it starts
- Send daily study reminders at 7 AM Vietnam time

## Troubleshooting

If the bot stops working:
1. Check if your Discord token is valid
2. Verify the channel ID is correct
3. Check Glitch logs for any errors
4. Make sure the bot has proper permissions in Discord

## Keeping the Bot Active

To prevent the Glitch project from going to sleep after 5 minutes of inactivity, you can use UptimeRobot:

1. After deploying your bot to Glitch, copy your project's URL (e.g., https://your-project.glitch.me)

2. Set up UptimeRobot:
   - Go to [UptimeRobot](https://uptimerobot.com/) and create a free account
   - Click "Add New Monitor"
   - Select "HTTP(s)" as the monitor type
   - Enter a friendly name (e.g., "PTE Discord Bot")
   - Paste your Glitch project URL
   - Set monitoring interval to 5 minutes
   - Click "Create Monitor"

This will keep your bot active 24/7 without needing Glitch Pro by pinging your project every 5 minutes.

## Notes

- The bot needs to run continuously to send daily messages
- UptimeRobot's free plan allows up to 50 monitors
- Make sure your Glitch project is set to "Public" for UptimeRobot to access it
