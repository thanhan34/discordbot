from http.server import BaseHTTPRequestHandler
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot import run

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Bot is running!'.encode())
        
        # Start the bot if it's not already running
        if 'DISCORD_TOKEN' in os.environ:
            try:
                run()
            except Exception as e:
                print(f"Error starting bot: {e}")
        return

def main():
    if 'DISCORD_TOKEN' in os.environ:
        run()

if __name__ == '__main__':
    main()
