# SplitNotes
Software for syncing notes with LiveSplit using the LiveSplit server component.

Splitnotes automatically shows notes for the split you are currently on.

## Install
1. Download the latest version of LiveSplit Server Component from [this](https://github.com/LiveSplit/LiveSplit.Server/releases) site.
2. Unzip and move the files to the component folder in your LiveSplit install (...\LiveSplit\Components)
3. Download the latest version of SplitNotes from [this](https://github.com/joelnir/SplitNotes/releases) page.
4. Unzip SplitNotes anywhere.

## How To Use
**Connect to LiveSplit**
1.Launch SplitNotes
2. Launch LiveSplit
3. Go to "Edit Layout" -> "+" -> "Control" -> "LiveSplit Server". Hit ok.
4. In LiveSplit, select "Control" -> "Start Server".
5. SplitNotes should now be connected to LiveSplit. If connection is active the Icon for SplitNotes is green.

**Format your notes**
It is recommended to use a .txt file to store your notes.
Note files should be formatted as following:

* Normal text is treated as notes
* New Line means notes for a specific split is over.
* Text in bracket ([some text]) is ignored from notes, this could be used to write down titles or other comments to keep the note file tidy.

Example:

  [Split1]
  These are some notes for split 1.
  
  These are some notes for split2.
  As you can see a title in brackets is not neccesary.
  A simple new line is enough to separate notes for different splits.
  
  Also som notes for split 3.
  You don't have to [ be afraid to use brackets [ in the middle  of notes].


**Load Notes**


## Features

#### Development
Written in Python using tkinter GUI library.
Made by Joelnir.
