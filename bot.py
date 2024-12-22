import os
import discord
import datetime
import asyncio
import logging
from aiohttp import web
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(level=logging.INFO)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Channel ID where messages will be sent
CHANNEL_ID = int(os.getenv('CHANNEL_ID', '0'))

# List of shadowing links to cycle through
SHADOWING_LINKS = [
    "https://study.pteintensive.com/shadowing/Aboriginal%20People",
    "https://study.pteintensive.com/shadowing/Abstract%20Preparation",
    "https://study.pteintensive.com/shadowing/Actor%20Training",
    "https://study.pteintensive.com/shadowing/Adulthood",
    "https://study.pteintensive.com/shadowing/Agricultural%20Problems",
    "https://study.pteintensive.com/shadowing/Agricultural%20Science",
    "https://study.pteintensive.com/shadowing/Akimbo",
    "https://study.pteintensive.com/shadowing/Alphabet",
    "https://study.pteintensive.com/shadowing/Antarctic",
    "https://study.pteintensive.com/shadowing/Aromatic%20Substance",
    "https://study.pteintensive.com/shadowing/Atlantis",
    "https://study.pteintensive.com/shadowing/Attendance",
    "https://study.pteintensive.com/shadowing/Attendance%20to%20Theater",
    "https://study.pteintensive.com/shadowing/Augustus",
    "https://study.pteintensive.com/shadowing/Australian%20Mining%20Industry"
]

# Keep track of current link index
current_link_index = 0

# Daily messages for each day of the week
DAILY_MESSAGES = {
    'Sunday': """Reminder for Sunday
Luyện đọc DI, thu âm và chấm điểm gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Làm 1 bài SST, gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> @🐯Target 42🐯 
Chép 10 câu WFD, kết hợp nghe thụ động <@&1024927443703828512> <@&1024927397184819230> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Ôn 10 câu RFIB, RWFIB  <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 15 câu Read Aloud   <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 30 câu RS <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc shadowing bài: sử dụng đường link này: <@&1024927443703828512> <@&1093855479618338816>
https://study.pteintensive.com/shadowing/Self-motivation 
Sau đó bấm vào practice để qua APEUNI để ghi âm và gửi lên Discord""",

    'Monday': """Monday
Luyện đọc DI, thu âm và chấm điểm gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Làm 1 bài SST, gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> @🐯Target 42🐯 
Chép 10 câu WFD, kết hợp nghe thụ động <@&1024927443703828512> <@&1024927397184819230> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Ôn 10 câu RFIB, RWFIB  <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 15 câu Read Aloud   <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 30 câu RS <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc shadowing bài: sử dụng đường link này: <@&1024927443703828512> <@&1093855479618338816>
https://study.pteintensive.com/shadowing/Semiconductor%20Industry  
Sau đó bấm vào practice để qua APEUNI để ghi âm và gửi lên Discord""",

    'Tuesday': """Tuesday
Luyện đọc RL, thu âm và chấm điểm gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Làm 1 bài SWT rồi gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> @🐯Target 42🐯 
Chép 10 câu WFD, kết hợp nghe thụ động <@&1024927443703828512> <@&1024927397184819230> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Ôn 10 câu RFIB, RWFIB  <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 15 câu Read Aloud   <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 30 câu RS <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc shadowing bài: sử dụng đường link này: <@&1024927443703828512> <@&1093855479618338816>
https://study.pteintensive.com/shadowing/Sexual%20Infections 
Sau đó bấm vào practice để qua APEUNI để ghi âm và gửi lên Discord""",

    'Wednesday': """Wednesday
Luyện đọc DI, thu âm và chấm điểm gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Làm 1 bài SST, gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> @🐯Target 42🐯 
Chép 10 câu WFD, kết hợp nghe thụ động <@&1024927443703828512> <@&1024927397184819230> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Ôn 10 câu RFIB, RWFIB  <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 15 câu Read Aloud   <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 30 câu RS <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc shadowing bài: sử dụng đường link này: <@&1024927443703828512> <@&1093855479618338816>
https://study.pteintensive.com/shadowing/Shakespeare 
Sau đó bấm vào practice để qua APEUNI để ghi âm và gửi lên Discord""",

    'Thursday': """Thursday
Chép template Essay <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Làm 1 bài SST, gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> @🐯Target 42🐯 
Chép 10 câu WFD, kết hợp nghe thụ động <@&1024927443703828512> <@&1024927397184819230> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Ôn 10 câu RFIB, RWFIB  <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 15 câu Read Aloud   <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 30 câu RS <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc shadowing bài: sử dụng đường link này: <@&1024927443703828512> <@&1093855479618338816>
https://study.pteintensive.com/shadowing/Shrimp%20Farm 
Sau đó bấm vào practice để qua APEUNI để ghi âm và gửi lên Discord""",

    'Friday': """Friday
Luyện đọc DI, thu âm và chấm điểm gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Làm 1 bài SST, gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> @🐯Target 42🐯 
Chép 10 câu WFD, kết hợp nghe thụ động <@&1024927443703828512> <@&1024927397184819230> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Ôn 10 câu RFIB, RWFIB  <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 15 câu Read Aloud   <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 30 câu RS <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc shadowing bài: sử dụng đường link này: <@&1024927443703828512> <@&1093855479618338816>
https://study.pteintensive.com/shadowing/Single%20Research 
Sau đó bấm vào practice để qua APEUNI để ghi âm và gửi lên Discord""",

    'Saturday': """Saturday
Luyện đọc RL, thu âm và chấm điểm gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Làm 1 bài SWT rồi gửi lên Discord <@&1024927443703828512> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> @🐯Target 42🐯 
Chép 10 câu WFD, kết hợp nghe thụ động <@&1024927443703828512> <@&1024927397184819230> <@&1093855479618338816> <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Ôn 10 câu RFIB, RWFIB  <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 15 câu Read Aloud   <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc 30 câu RS <@&1024927341664800882> <@&1093125221373972531> <@&1024927138828271687> 
Luyện đọc shadowing bài: sử dụng đường link này: <@&1024927443703828512> <@&1093855479618338816>
https://study.pteintensive.com/shadowing/Slang 
Sau đó bấm vào practice để qua APEUNI để ghi âm và gửi lên Discord"""
}

async def send_daily_message():
    global current_link_index
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Get current day of the week
        day = datetime.datetime.now().strftime('%A')
        # Send the corresponding message for the day
        if day in DAILY_MESSAGES:
            # Get the message and replace the shadowing link
            message = DAILY_MESSAGES[day]
            # Find and replace the shadowing link in the message with current link
            for old_link in [
                "https://study.pteintensive.com/shadowing/Self-motivation",
                "https://study.pteintensive.com/shadowing/Semiconductor%20Industry",
                "https://study.pteintensive.com/shadowing/Sexual%20Infections",
                "https://study.pteintensive.com/shadowing/Shakespeare",
                "https://study.pteintensive.com/shadowing/Shrimp%20Farm",
                "https://study.pteintensive.com/shadowing/Single%20Research",
                "https://study.pteintensive.com/shadowing/Slang"
            ]:
                message = message.replace(old_link, SHADOWING_LINKS[current_link_index])
            
            await channel.send(message)
            
            # Move to next link
            current_link_index = (current_link_index + 1) % len(SHADOWING_LINKS)
    else:
        logging.error(f"Could not find channel with ID: {CHANNEL_ID}")

@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')
    
    # Send test message
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Bot is now running on Glitch! 🚀")
        logging.info(f"Test message sent to channel {CHANNEL_ID}")
    else:
        logging.error(f"Could not find channel with ID: {CHANNEL_ID}")
    
    # Set up scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_daily_message,
        CronTrigger(hour=7, minute=0),  # Run every day at 7 AM
        timezone='Asia/Ho_Chi_Minh'  # Set to Vietnam timezone
    )
    scheduler.start()

# Set up web server for UptimeRobot pings
async def setup_webserver():
    app = web.Application()
    app.router.add_get("/", lambda request: web.Response(text="Bot is alive!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 3000)
    await site.start()
    logging.info("Web server started on port 3000")

# Run the bot
async def run_bot():
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        logging.error("No Discord token found in environment variables!")
        return
    try:
        # Start web server for UptimeRobot
        await setup_webserver()
        # Start the bot
        await bot.start(token)
    except Exception as e:
        logging.error(f"Error running bot: {e}")

if __name__ == "__main__":
    # Run both the web server and bot
    asyncio.run(run_bot())
