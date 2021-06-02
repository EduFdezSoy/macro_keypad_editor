import PySimpleGUI as sg
import DatabaseController
import Utils


def main():
    global recording, window, layout

    # flags, constants and global variables
    recording = False
    window = None

    # THEME
    sg.theme('DarkPurple')

    # ICON
    # with open(Utils.resource_path('images/icon.gif'), 'rb') as icon_gif:
    #     icon_base64 = base64.b64encode(icon_gif.read())
    # sg.set_options(icon=icon_base64)

    #region interface declaration

    keySize = (20, 14)
    keyPad = (10, 10)

    keyColumn = [
        [
            sg.Button('F1', size=keySize, pad=keyPad, key='-key01'),
            sg.Button('F2', size=keySize, pad=keyPad, key='-key02'),
            sg.Button('F3', size=keySize, pad=keyPad, key='-key03')
        ],
        [
            sg.Button('F4', size=keySize, pad=keyPad, key='-key04'),
            sg.Button('F5', size=keySize, pad=keyPad, key='-key05'),
            sg.Button('F6', size=keySize, pad=keyPad, key='-key06')
        ],
        [
            sg.Button('F7', size=keySize, pad=keyPad, key='-key07'),
            sg.Button('F8', size=keySize, pad=keyPad, key='-key08'),
            sg.Button('F9', size=keySize, pad=keyPad, key='-key09')
        ],
    ]

    # not used right now as I dont know how the F we will comm with the keypad
    keyConfigSelector = [[sg.Text("Rows:"),
                          sg.Input("3", size=(10, 1))],
                         [sg.Text("Columns:"),
                          sg.Input("3", size=(7, 1))]]

    btnPad = ((8, 5), (12, 5))
    keyCombinationSetting = [[sg.Text('Name:', pad=((10, 10), (10, 1)))],
                             [
                                 sg.Input('KeyName',
                                          metadata=0,
                                          key="-keyName-",
                                          pad=((10, 10), (1, 5)),
                                          size=(30, 2))
                             ], [sg.Text('Key:', pad=((10, 10), (10, 1)))],
                             [
                                 sg.Input('Key Combination',
                                          metadata=0,
                                          key="-keyComb-",
                                          enable_events=True,
                                          pad=((10, 15), (1, 5)),
                                          size=(17, 2)),
                                 sg.Button('Record', key="-record-")
                             ],
                             [
                                 sg.Button('Save', key="-save-", pad=btnPad),
                                 sg.Button('Cancel',
                                           key="-cancel-",
                                           pad=btnPad),
                                 sg.Button('Reset', key="-reset-", pad=btnPad)
                             ]]

    bottomButtons = [
        sg.Button('Donate', key="-donate-", pad=((15, 5), (10, 5))),
        sg.Button('Exit', key="-close-", pad=btnPad)
    ]

    layout = [[
        # sg.Column(keyConfigSelector),
        sg.Column(keyColumn),
        sg.Column(
            [[sg.Frame('', keyCombinationSetting, size=keySize, pad=keyPad)],
             bottomButtons],
            vertical_alignment='top')
    ]]


#endregion


def getWindow(db: DatabaseController):
    location = db.getConf('location')
    x = None
    y = None

    if location != None:
        loc = location[1][1:-1].split(',')
        x = loc[0]
        y = loc[1]

    global window
    window = sg.Window("keyPad Config", layout, location=(x, y), finalize=True)

    keys = db.getAllKeys()

    # set first key as selected
    window['-keyName-'](keys[0][1])
    window['-keyName-'].metadata = keys[0][0]
    window['-keyComb-'](keys[0][2])

    for row in keys:
        # put all keyNames
        window['-key' + str(row[0]).zfill(2)](row[1] + '\n\n' + row[2])

    return window


# events


def closeEvent(event):
    return event == "-close-" or event == sg.WIN_CLOSED


def resetKeyButtonPressedEvent(event):
    return event == "-reset-"


def recordKeyButtonPressedEvent(event):
    return event == "-record-"


def cancelKeyButtonPressedEvent(event):
    return event == "-cancel-"


def keyClickEvent(event):
    return "-key" in event


def inputKeyNameEvent(event):
    return event == "-keyName-"


def inputKeyCombinationEvent(event):
    return event == "-keyComb-"


# actions


def closeAction(event, db: DatabaseController):
    location = window.CurrentLocation()
    db.setConf('location', str(location))


def setKeyClicked(event, db: DatabaseController):
    keyId = event.strip("-key")
    keyStruct = db.getKey(keyId)

    if keyStruct == None:
        try:
            keyStruct = (int(keyId), 'F' + keyId, '')
        except Exception:
            return

    window['-keyName-'].metadata = keyStruct[0]
    window['-keyName-'](keyStruct[1])
    window['-keyComb-'](keyStruct[2])
    window[event].set_focus(True)

    print(keyStruct)


def resetKeyClicked(event, db: DatabaseController):
    keyID = window['-keyName-'].metadata
    db.insertKey(keyID, 'F' + str(keyID), '')
    setKeys(db)
    setKeyClicked("-key" + str(window['-keyName-'].metadata).zfill(2), db)


def cancelKeyEdition(event, db: DatabaseController):
    setKeyClicked("-key" + str(window['-keyName-'].metadata).zfill(2), db)
    setKeys(db)
    window['-save-'](disabled=False)
    window['-reset-'](disabled=False)


def recordKeyClicked(event):
    global recording
    recording = not recording
    if recording:
        window[event].set_focus(True)
        window['-save-'](disabled=True)
        window['-reset-'](disabled=True)
    else:
        window['-save-'](disabled=False)
        window['-reset-'](disabled=False)


def putKeysClicked(keyList):
    setKeyCombination(formatKeyList(keyList))


def doNotLetWrite(event, values):
    txt = []
    for i in str(values[event]).split('+'):
        txt.append(Utils.validate_keys(i))

    window[event](formatKeyList(txt))


# functions


def setKeys(db: DatabaseController):
    keys = db.getAllKeys()
    for row in keys:
        # put all keyNames
        window['-key' + str(row[0]).zfill(2)](row[1] + '\n\n' + row[2])


def formatKeyList(keylist):
    string = ""

    for key in keylist:
        string += str(key).strip("'").strip('Key.').capitalize()
        string += '+'

    return string[0:-1]


def setKeyCombination(keysStr):
    window['-keyComb-'](keysStr)


# main

if __name__ == '__main__':
    main()