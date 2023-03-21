from flask import Flask
from controller.Application import Application
from resources.FrameReceiver import FrameReceiver

application = Application()
app = application.create_app(resources = [FrameReceiver])

if __name__ == "__main__":
    application.run()

