import pvporcupine

import VoskModels



def main():
    """
        Runs the Jarvis speech recognition system.
        Initializes the speech recognizer and starts listening for commands. (Continuous | Single-shot)
    """
    print("Jarvis speech recognition")
    print("Choose recognition mode:")
    print("1. Continuous listening")
    print("2. Single-shot recognition")
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")

    speech_recognizer = VoskModels.MultilingualVosk('en')

    try:
        if choice == '1':
            print("\n--- Continuous Listening Mode ---")
            for recognized_text in speech_recognizer.listen_continuous():
                print(f"You said: '{recognized_text}'")
                
                if recognized_text.lower() in ['exit', 'quit', 'stop']:
                    print("Stopping...")
                    break
        else:
            print("\n--- Single-shot Recognition Mode ---")
            recognized_text = speech_recognizer.recognize_once()
            if recognized_text:
                print(f"You said: '{recognized_text}'")
            else:
                print("No speech recognized.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        speech_recognizer.cleanup()


if __name__ == '__main__':
    main()