import win32com.client as wc

if __name__ == '__main__':
    print("Welcome to speaker")
    while True:
        x = input("Enter what you want you to pronouce: ")
        if(x == "q"):
            command.Speak("Bye bye Friend")
            break
        command = wc.Dispatch("Sapi.SpVoice")
        command.Speak(x)
