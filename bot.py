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
import logging
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
"https://study.pteintensive.com/shadowing/Australian%20Mining%20Industry",
"https://study.pteintensive.com/shadowing/Baby%20Hearing",
"https://study.pteintensive.com/shadowing/Barley%20Grains",
"https://study.pteintensive.com/shadowing/Beauty%20Contests",
"https://study.pteintensive.com/shadowing/Becoming%20Carbon-neutral",
"https://study.pteintensive.com/shadowing/Behavioral%20Science",
"https://study.pteintensive.com/shadowing/Bill",
"https://study.pteintensive.com/shadowing/Biodiversity",
"https://study.pteintensive.com/shadowing/Bird%20Nests",
"https://study.pteintensive.com/shadowing/Black%20Swan%20%EF%BC%88B%EF%BC%89",
"https://study.pteintensive.com/shadowing/Blue",
"https://study.pteintensive.com/shadowing/Blue%20(B)",
"https://study.pteintensive.com/shadowing/Bookkeeper%20Fraud",
"https://study.pteintensive.com/shadowing/Botswana",
"https://study.pteintensive.com/shadowing/Brain",
"https://study.pteintensive.com/shadowing/Brain%20Secrets",
"https://study.pteintensive.com/shadowing/Business%20School%20Admission",
"https://study.pteintensive.com/shadowing/Carbon%20Dioxide%20Emission",
"https://study.pteintensive.com/shadowing/Central%20Aim",
"https://study.pteintensive.com/shadowing/Child%20Psychology",
"https://study.pteintensive.com/shadowing/Choice%20of%20Book",
"https://study.pteintensive.com/shadowing/Civil%20War%20and%20Lincoln",
"https://study.pteintensive.com/shadowing/Climate%20Effects",
"https://study.pteintensive.com/shadowing/Closure%20Activities",
"https://study.pteintensive.com/shadowing/Colloquialism",
"https://study.pteintensive.com/shadowing/Companies",
"https://study.pteintensive.com/shadowing/Constellation",
"https://study.pteintensive.com/shadowing/Contribution%20to%20Book",
"https://study.pteintensive.com/shadowing/Copyright",
"https://study.pteintensive.com/shadowing/Credit%20Unions",
"https://study.pteintensive.com/shadowing/Danny%20Danziger",
"https://study.pteintensive.com/shadowing/Deaf%20Children",
"https://study.pteintensive.com/shadowing/December%20Sales",
"https://study.pteintensive.com/shadowing/Department%20Stores",
"https://study.pteintensive.com/shadowing/Different%20Dimensions",
"https://study.pteintensive.com/shadowing/Diplomacy",
"https://study.pteintensive.com/shadowing/Disaster",
"https://study.pteintensive.com/shadowing/Divorce",
"https://study.pteintensive.com/shadowing/Domestication",
"https://study.pteintensive.com/shadowing/Drug%20Overdose%20Deaths",
"https://study.pteintensive.com/shadowing/Ear%20Fluid",
"https://study.pteintensive.com/shadowing/Economic%20Depression",
"https://study.pteintensive.com/shadowing/Educational%20Demand",
"https://study.pteintensive.com/shadowing/Electric%20Car",
"https://study.pteintensive.com/shadowing/Elephant",
"https://study.pteintensive.com/shadowing/Emigrants",
"https://study.pteintensive.com/shadowing/Energy%20Efficiency",
"https://study.pteintensive.com/shadowing/English%20Revolution%20(B)",
"https://study.pteintensive.com/shadowing/Enough%20Fluid",
"https://study.pteintensive.com/shadowing/European%20Wildcats",
"https://study.pteintensive.com/shadowing/Examination",
"https://study.pteintensive.com/shadowing/Fast%20Food",
"https://study.pteintensive.com/shadowing/Faster%20Communications",
"https://study.pteintensive.com/shadowing/Fence",
"https://study.pteintensive.com/shadowing/Fiscal%20Year",
"https://study.pteintensive.com/shadowing/Flags",
"https://study.pteintensive.com/shadowing/Flattened%20World",
"https://study.pteintensive.com/shadowing/Flood%20Control",
"https://study.pteintensive.com/shadowing/Flu%20Season",
"https://study.pteintensive.com/shadowing/Foreign%20Plant",
"https://study.pteintensive.com/shadowing/Founding%20Fathers",
"https://study.pteintensive.com/shadowing/Girls%20v.s.%20Boys",
"https://study.pteintensive.com/shadowing/Global%20Changes",
"https://study.pteintensive.com/shadowing/Global%20Management",
"https://study.pteintensive.com/shadowing/Globalization",
"https://study.pteintensive.com/shadowing/Grand%20Canyon",
"https://study.pteintensive.com/shadowing/Hainan",
"https://study.pteintensive.com/shadowing/Hazard%20Assessment",
"https://study.pteintensive.com/shadowing/Healthcare",
"https://study.pteintensive.com/shadowing/Hemisphere",
"https://study.pteintensive.com/shadowing/Heterogeneous%20Student",
"https://study.pteintensive.com/shadowing/Humanities",
"https://study.pteintensive.com/shadowing/Hybrid%20Rice",
"https://study.pteintensive.com/shadowing/Hydrogen%20Fuel",
"https://study.pteintensive.com/shadowing/Industrial%20Revolution",
"https://study.pteintensive.com/shadowing/Information%20Technology",
"https://study.pteintensive.com/shadowing/Infrastructure",
"https://study.pteintensive.com/shadowing/Injury%20or%20Disease",
"https://study.pteintensive.com/shadowing/Innovative%20Product",
"https://study.pteintensive.com/shadowing/Internal%20Combustion%20Engine",
"https://study.pteintensive.com/shadowing/Introvert%20and%20Extrovert",
"https://study.pteintensive.com/shadowing/Introvert%20and%20Extrovert%20(B)",
"https://study.pteintensive.com/shadowing/Introverts'%20Thinking",
"https://study.pteintensive.com/shadowing/Language%20Appearance",
"https://study.pteintensive.com/shadowing/Language%20Diversity",
"https://study.pteintensive.com/shadowing/Largest%20Moon",
"https://study.pteintensive.com/shadowing/Leader%20Waves",
"https://study.pteintensive.com/shadowing/Learner%20Experience",
"https://study.pteintensive.com/shadowing/Learning%20Method",
"https://study.pteintensive.com/shadowing/Legal%20System",
"https://study.pteintensive.com/shadowing/Legal%20Writing",
"https://study.pteintensive.com/shadowing/Lenient%20Parents",
"https://study.pteintensive.com/shadowing/Lincoln",
"https://study.pteintensive.com/shadowing/Linguistic%20Diversity",
"https://study.pteintensive.com/shadowing/Linguistic%20Morality",
"https://study.pteintensive.com/shadowing/Loggerhead%20Turtle",
"https://study.pteintensive.com/shadowing/Love",
"https://study.pteintensive.com/shadowing/MBA%20Students",
"https://study.pteintensive.com/shadowing/Madagascar",
"https://study.pteintensive.com/shadowing/Magnetar",
"https://study.pteintensive.com/shadowing/Malaria%20Vaccine",
"https://study.pteintensive.com/shadowing/Man-made%20Light",
"https://study.pteintensive.com/shadowing/Market%20Research",
"https://study.pteintensive.com/shadowing/Marketing%20Management",
"https://study.pteintensive.com/shadowing/Matthew%20Brady",
"https://study.pteintensive.com/shadowing/Microbes",
"https://study.pteintensive.com/shadowing/Microscopic%20Invaders",
"https://study.pteintensive.com/shadowing/Modern%20Buildings",
"https://study.pteintensive.com/shadowing/Most%20Important%20Things",
"https://study.pteintensive.com/shadowing/Naked%20Biome",
"https://study.pteintensive.com/shadowing/Natural%20Environment",
"https://study.pteintensive.com/shadowing/Nectar",
"https://study.pteintensive.com/shadowing/Negative%20Immigration",
"https://study.pteintensive.com/shadowing/Neurotransmitter",
"https://study.pteintensive.com/shadowing/New%20Textbook",
"https://study.pteintensive.com/shadowing/Night%20Sky",
"https://study.pteintensive.com/shadowing/Noise",
"https://study.pteintensive.com/shadowing/Norms%20and%20Values",
"https://study.pteintensive.com/shadowing/Nutritionally%20Bankrupt",
"https://study.pteintensive.com/shadowing/Online%20Shopping",
"https://study.pteintensive.com/shadowing/Only%20Family",
"https://study.pteintensive.com/shadowing/Organic%20Molecules",
"https://study.pteintensive.com/shadowing/Orientalists",
"https://study.pteintensive.com/shadowing/Paracas%20Glyphs",
"https://study.pteintensive.com/shadowing/Parkinson",
"https://study.pteintensive.com/shadowing/Pay%20Scheme",
"https://study.pteintensive.com/shadowing/Personal%20Libraries",
"https://study.pteintensive.com/shadowing/Pluto",
"https://study.pteintensive.com/shadowing/Political%20Problems",
"https://study.pteintensive.com/shadowing/Population%20Growth",
"https://study.pteintensive.com/shadowing/Private%20Equity",
"https://study.pteintensive.com/shadowing/Productive%20Capacity",
"https://study.pteintensive.com/shadowing/Protein",
"https://study.pteintensive.com/shadowing/Psychologist",
"https://study.pteintensive.com/shadowing/Psychology",
"https://study.pteintensive.com/shadowing/Question%20Doddging",
"https://study.pteintensive.com/shadowing/Rates%20of%20Depression",
"https://study.pteintensive.com/shadowing/Recycling",
"https://study.pteintensive.com/shadowing/Regular%20Exercise",
"https://study.pteintensive.com/shadowing/Restaurant%20Location",
"https://study.pteintensive.com/shadowing/Roman%20Army",
"https://study.pteintensive.com/shadowing/Root%20Network",
"https://study.pteintensive.com/shadowing/Rural%20Population",
"https://study.pteintensive.com/shadowing/Russia",
"https://study.pteintensive.com/shadowing/Sad%20Truth",
"https://study.pteintensive.com/shadowing/School%20Shooting",
"https://study.pteintensive.com/shadowing/Selective%20History",
"https://study.pteintensive.com/shadowing/Self-motivation",
"https://study.pteintensive.com/shadowing/Semiconductor%20Industry",
"https://study.pteintensive.com/shadowing/Sexual%20Infections",
"https://study.pteintensive.com/shadowing/Shakespeare",
"https://study.pteintensive.com/shadowing/Shrimp%20Farm",
"https://study.pteintensive.com/shadowing/Single%20Research",
"https://study.pteintensive.com/shadowing/Slang",
"https://study.pteintensive.com/shadowing/Social%20Media",
"https://study.pteintensive.com/shadowing/Source%20of%20Funding",
"https://study.pteintensive.com/shadowing/Specimen",
"https://study.pteintensive.com/shadowing/Statistical%20Chance",
"https://study.pteintensive.com/shadowing/Statistical%20Information",
"https://study.pteintensive.com/shadowing/Statistics",
"https://study.pteintensive.com/shadowing/Summary%20and%20Abstract",
"https://study.pteintensive.com/shadowing/Summerhill%20School",
"https://study.pteintensive.com/shadowing/Surgical%20Infections",
"https://study.pteintensive.com/shadowing/Tasmania",
"https://study.pteintensive.com/shadowing/Tea%20Ceremony",
"https://study.pteintensive.com/shadowing/Tele-banking",
"https://study.pteintensive.com/shadowing/Telecommunication",
"https://study.pteintensive.com/shadowing/Tesla%20%26%20Edison",
"https://study.pteintensive.com/shadowing/The%20Awards",
"https://study.pteintensive.com/shadowing/The%20UN",
"https://study.pteintensive.com/shadowing/Tissues%20and%20Organs",
"https://study.pteintensive.com/shadowing/Toasted%20Food",
"https://study.pteintensive.com/shadowing/Trump",
"https://study.pteintensive.com/shadowing/Tsunami",
"https://study.pteintensive.com/shadowing/Tulip",
"https://study.pteintensive.com/shadowing/Tutor",
"https://study.pteintensive.com/shadowing/Twitter",
"https://study.pteintensive.com/shadowing/USA%20Uniforms",
"https://study.pteintensive.com/shadowing/Urban%20Forests",
"https://study.pteintensive.com/shadowing/Use%20of%20IT",
"https://study.pteintensive.com/shadowing/Useful%20Resource",
"https://study.pteintensive.com/shadowing/Values%20of%20Literature",
"https://study.pteintensive.com/shadowing/Vanilla",
"https://study.pteintensive.com/shadowing/Volcano%20Behaviors",
"https://study.pteintensive.com/shadowing/War%20on%20Women",
"https://study.pteintensive.com/shadowing/Wildlife",
"https://study.pteintensive.com/shadowing/William%20Shakespeare",
"https://study.pteintensive.com/shadowing/Window%20in%20Painting",
"https://study.pteintensive.com/shadowing/Wolf",
"https://study.pteintensive.com/shadowing/Work",
"https://study.pteintensive.com/shadowing/Working%20Unions",
"https://study.pteintensive.com/shadowing/X-ray",
"https://study.pteintensive.com/shadowing/Yellow",
"https://study.pteintensive.com/shadowing/Yield%20of%20Plants",

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
            # Find and replace the shadowing link in the message
            message = message.replace("https://study.pteintensive.com/shadowing/Self-motivation", SHADOWING_LINKS[current_link_index])
            message = message.replace("https://study.pteintensive.com/shadowing/Semiconductor%20Industry", SHADOWING_LINKS[current_link_index])
            message = message.replace("https://study.pteintensive.com/shadowing/Sexual%20Infections", SHADOWING_LINKS[current_link_index])
            message = message.replace("https://study.pteintensive.com/shadowing/Shakespeare", SHADOWING_LINKS[current_link_index])
            message = message.replace("https://study.pteintensive.com/shadowing/Shrimp%20Farm", SHADOWING_LINKS[current_link_index])
            message = message.replace("https://study.pteintensive.com/shadowing/Single%20Research", SHADOWING_LINKS[current_link_index])
            message = message.replace("https://study.pteintensive.com/shadowing/Slang", SHADOWING_LINKS[current_link_index])
            
            await channel.send(message)
            
            # Move to next link
            current_link_index = (current_link_index + 1) % len(SHADOWING_LINKS)
    else:
        print(f"Could not find channel with ID: {CHANNEL_ID}")

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
