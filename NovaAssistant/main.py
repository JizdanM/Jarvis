import pvporcupine

import STT
import TTS

"""
    Potential large changes in the project:
    Potential names for change/inspiration: Nova, Corvus, Vega | Nyx, Echo, Iris
"""

def main():
    """
        Runs Nova's speech recognition system.
        Initializes the speech recognizer and starts listening for commands. (Continuous | Single-shot)
    """
    debug = 0 # 0 for continuous listening, 1 for single-shot recognition

    speech_recognizer = STT.SpeechCapture()

    try:
        if debug == 0:
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