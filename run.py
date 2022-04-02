from bot import Bot
import os

if __name__ == "__main__":
    bot = Bot()
    # This is to make boost in cache memory from unix system, like my case.
    if os.name != "nt":
        import uvloop
        uvloop.install()
    bot.run()
