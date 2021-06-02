import pynput


def main():
    global recording, keyList, update

    recording = False
    keyList = []
    update = None

    # set listeners and start

    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()


def on_press(key):
    global recording, update, keyList

    if recording:
        if key not in keyList:
            keyList.append(key)

            if update != None:
                update(keyList)


# def on_release(key):
#     global recording, update, keyList
#     if recording:
#         keyList.remove(key)

#         if update != None:
#             update(keyList)


def toggleRecording():
    global recording, keyList
    recording = not recording
    keyList.clear()


if __name__ == '__main__':
    main()