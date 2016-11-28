pip install aiml
works with python 2.7 only!
-------
import aiml
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")
while True:
    message = raw_input("USER >> ")
    bot_response = kernel.respond(message)
    print("BOT >> " + bot_response)

-------
To choose a topic to discuss, say "I want to talk".
Only "cats" topic is currently available, meow!