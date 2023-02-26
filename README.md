Experimental bot that automatically posts in a specific forum thread.
The thread's goal is to count to 100 000.
This bot automatically posts new numbers everytime another user posts a reply.
Usage:

1. Copy the .env.example file to a new file called .env
2. Open the .env file and fill the username and password
3. Go to thread url: https://forum.kajgana.com/threads/%D0%90%D1%98%D0%B4%D0%B5-%D0%B4%D0%B0-%D0%B8%D0%B7%D0%B1%D1%80%D0%BE%D0%B8%D0%BC%D0%B5-%D0%B4%D0%BE-100-000.54309/page-9999
4. Find the last number posted on the thread
5. From cmd run this:
   python bot.py <last_number_posted\_\_on_the_thread>

Make sure someone else posted the last number (and not you) to dodge unwanted concatenated replies
