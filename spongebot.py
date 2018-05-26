import os
import time
import random
from slackclient import SlackClient

SLACK_BOT_TOKEN='xoxb-244708223792-371903686711-zLWiT4pDIeG82kT6Vx36Wzxn'
BOT_ID='U6AK1FK4H'

# starterbot's ID as an environment variable
# BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
CLUCK_COMMAND = ""
HOTDOG_COMMAND = "hotdog"
HOTD1 = "a hotdog "
HOTD2 = " a sandwich"

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if command.startswith(CLUCK_COMMAND):
        response = cluckify(command[len(CLUCK_COMMAND):]) + slack_client
    if command.startswith(HOTDOG_COMMAND):
        response = HOTD1 + "is" if (random.randint(0, 9) % 2 == 0) else "isn't"  + HOTD2
        response = cluckify(response) + "?"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def cluckify(s):
    ret = ""
    i = False  #
    for char in s:
        if i:
            ret += char.upper()
        else:
            ret += char.lower()
        if char != ' ':
            if random.randint(0, 9) % 2 == 0:
                i = not i
    return ret

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
