# import ArduinoCom as ar
import DatabaseController as db
import InterfaceController as ifc
import KeyRecorder as kr

# if you are going to shipt this product add sentry.io or other exception logger
# and some sort of update checker, see: 
# https://www.pyinstaller.org/
# https://www.pyupdater.org/


def main():
    db.main()
    ifc.main()
    kr.main()

    db.initDB()
    db.insertKey(1, "primerateclaaaa", "Ctrl+A")

    # -- interface loop --

    window = ifc.getWindow(db)

    while True:
        event, values = window.read()

        if ifc.closeEvent(event):
            ifc.closeAction(event, db)
            db.close()
            break
        if ifc.keyClickEvent(event):
            ifc.setKeyClicked(event, db)
        if ifc.resetKeyButtonPressedEvent(event):
            ifc.resetKeyClicked(event, db)
        if ifc.cancelKeyButtonPressedEvent(event):
            ifc.cancelKeyEdition(event, db)
            kr.recording = False
        if ifc.recordKeyButtonPressedEvent(event):
            ifc.recordKeyClicked(event)
            kr.update = ifc.putKeysClicked
            kr.toggleRecording()
        if ifc.inputKeyCombinationEvent(event):
            ifc.doNotLetWrite(event, values)

    window.close()

    # ar.main()
    # time.sleep(1)  # wait for the serial connection to initialize
    # ar.led_on_off()


if __name__ == '__main__':
    main()
