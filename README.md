# SplitNotes
Software for syncing notes with LiveSplit using the LiveSplit server component.  
  
Splitnotes automatically shows notes for the split you are currently on.  

![Screenshot 1](http://i.imgur.com/CMlF2pj.png) 
![Screenshot 2](http://i.imgur.com/4Ei2IiJ.png)

## Install
1. Download the latest version of LiveSplit Server Component from [this](https://github.com/LiveSplit/LiveSplit.Server/releases) site.
2. Unzip and move the files to the component folder in your LiveSplit install (...\LiveSplit\Components)
3. Download the latest version of SplitNotes from [this](https://github.com/joelnir/SplitNotes/releases) page.
4. Unzip SplitNotes anywhere.

## How To Use  
**Connect to LiveSplit**  
1. Launch Splitnotes.exe  
2. Launch LiveSplit  
3. Go to "Edit Layout" -> "+" -> "Control" -> "LiveSplit Server". Hit ok. 
4. In LiveSplit, select "Control" -> "Start Server".  
5. SplitNotes should now be connected to LiveSplit. If connection is active the Icon for SplitNotes is green.  

**Format your notes**  
It is recommended to use a .txt file to store your notes.  
Note files should be formatted as following:
  
* Normal text is treated as notes
* Text in bracket ([some text]) is ignored from notes, this could be used to write down titles or other comments to keep the note file tidy.
* A line only containing a split separator, such as a word (for example "\<split\>") or a simple newline, signals that notes for a specific split is over. You can set what you want to use as a split separator in the settings menu of SplitNotes.
  
Example with newline as separator:  
  
>[Split1]  
>these are some notes for split 1.  
>  
>These are some notes for split2.  
>As you can see a title in brackets is not neccesary.  
>A simple new line is enough to separate notes for different splits.  
>  
>Also some notes for split 3.  
>You don't have to [ worry abut using brackets [ in the middle  of a row].  

Example with "-end-" as separator:  
  
>[Split1]  
>these are some notes for split 1.  
>-end-  
>These are some notes for split2.  
>  
>Now it is fine to use linebreaks in the middle of the notes.  
>This will still be on the notes for split 2  
>-end-  
>Also some notes for split 3.  
>You don't have to [ worry abut using brackets [ in the middle  of a row].  
  
**Load Notes**  
1. Right-Click in SplitNotes and select "Load Notes".  
2. Choose your text file.  
3. Make sure that notes for the right amount of splits have been loaded.  
  
**Change Settings**  
1. Right-Click in SplitNotes and select "Settings"  
2. The settings menu will show up. Here you can set things like font, font size, text and background color, split separator and the server port. 
  
## Features  
  
* Automatically displayed notes based on the active split in LiveSplit.
* Ability to preview notes in the software when no run is going on by using the right and left arrow keys.
* Two different font sizes to make sure that notes are easy to read.
* Double layout to preview notes for both current and next split.
* Multiple settings to change the look of the text.
* Ability to set a custom port for interaction with the LiveSplit Server.

#### Development
Written in mainly procedural Python using tkinter GUI library.  
Made by Joelnir.
