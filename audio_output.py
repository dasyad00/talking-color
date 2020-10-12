import pyttsx3

engine = pyttsx3.init()


def say(message):
    engine.say(message)
    engine.runAndWait()


if __name__ == "__main__":
    say("TACO")
    say("turned on")
