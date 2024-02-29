# semiauto
This repository contains examples of three levels of test execution:

1) manual testing
2) semiautomatic testing
3) fully automatic testing

## manual test
Manual test is described in file [manual_test.txt](https://github.com/HiddenTrail/semiauto/blob/main/manual_test.txt).

## semiautomatic test
Semiautomatic test uses the [Dialogs library](https://robotframework.org/robotframework/latest/libraries/Dialogs.html).
The test itself is written as Robot Framework test case but it offers instructions to tester via dialogs made with [Dialogs library](https://robotframework.org/robotframework/latest/libraries/Dialogs.html).

Semiautomatic test can be executed by:
```
rf.sh semiauto.robot
```

## fully automatic test
Fully automatic test uses [Playwright Node Module](https://github.com/microsoft/playwright) based [BrowserLibrary](https://github.com/MarketSquare/robotframework-browser) keyword [Upload File By Selector](https://marketsquare.github.io/robotframework-browser/Browser.html#Upload%20File%20By%20Selector) to upload file.
Image comparison is done between expected test picture and the actual picture uploaded to file share service. Four different image comparison algorithms are used to compare images:
1) algorithm based on [OpenCV](https://opencv.org/)
2) algorithm based on [Pillow](https://python-pillow.org/)
3) algorithm based on [scikit-image](https://scikit-image.org/)
4) algorithm based on [ImageHash](https://github.com/JohannesBuchner/imagehash)

All pictures are rescaled to same dimensions before comparison and transformed to grayscale images.
These algorithms all return value between 0.0 (no match) and 1.0 (full match). 
For keyword `Assert Images Are Similar` all values should be 1.0 to succeed and for keyword `Assert Images Are Not Similar` all values should be less than 1.0.

Keywords and algorithms are implemented as [Robot Framework Python library](https://github.com/HiddenTrail/semiauto/blob/main/libs/ImageSimilarityLibrary.py).

Fully automatic test can be executed by:
```
rf.sh fullauto.robot
```

# installation
## semiautomatic test
To run semiautomatic test some installations are needed:
+ [Python](https://www.python.org/)
+ [Pip](https://pip.pypa.io/en/stable/)
+ [Node.js](https://nodejs.org/en)
+ [Robot Framework](https://robotframework.org/)
+ [BrowserLibrary](https://github.com/MarketSquare/robotframework-browser)
+ [tkinter](https://docs.python.org/3/library/tkinter.html) (needed by [Dialogs library](https://robotframework.org/robotframework/latest/libraries/Dialogs.html))

To install these (in addition to Python, Pip & Node.js) run:
```
pip install robotframework
pip install robotframework-browser
rfbrowser init
```
Tkinter installation on MacOS:
```
brew install python-tk@x.xx
```
where x.xx matches Python version, for example `3.11`

Tkinter installation on Linux (Ubuntu):
```
sudo apt install python3-tk
```

## fully automatic test
The same installation are needed for fully automatic test as in semiautomatic test except for [tkinter](https://docs.python.org/3/library/tkinter.html).

In addition the image libraries software need to be installed:
```
pip install opencv-python
pip install pillow
pip install scikit-image
pip install ImageHash
```
