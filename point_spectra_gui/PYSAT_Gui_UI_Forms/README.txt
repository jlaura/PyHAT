# Process

Start UIconversion.bat
then run compare.bat

# How it works

- "UI Files" holds many *.UI
- process all these UI files with "UIconversion.bat"
- UI conversion converts all the *.ui files to *.py and puts them into "PythonUI"
- compare takes all the *.py files, and compares it against "10_mainwindow_empty_UI.py"
- take the differences and place them into FINISHED

All the files in FINISHED can then be copied and placed into their respective UI modules


Example of how this works, and how this looks
* if you are viewing this in Notepad
* make sure to have Word Wrap turned off
* this way formatting of the below example 
* is not lost 
**Note that example.py is the python version of whatever was in ui. (IT IS NOT directly copying the insides of .ui file.)


 ~/UI files/example.ui 
  |------------------| 
  | <some content>   | 
  | <more xml cont>  | 
  | <this is wrong>  | 
  | <formatting>     | 
  | <technically>    | 
  | <speaking>       | 
  |                  | 
  |------------------| 
        |
        |
        |
   convert        
   using           
   UIconversion.bat 
        |
        |
        v
 ~/PythonUI/example.py 
  |------------------| 
  |  some content    | 
  |  more xml cont   | 
  |  this is wrong   | 
  |  formatting      | 
  |  technically     | 
  |  speaking        | 
  |                  | 
  |------------------| 
        |
        |
        |
   compare these    
   two files using  
   compare.bat
        |
        |
        v
 ~/PythonUI/mainwindow_empty.py
  |------------------| 
  |  some content    | 
  |  more xml cont   | 
  |                  | 
  |                  | 
  |                  | 
  |                  | 
  |                  | 
  |------------------| 
        |
        |
        |
   this is the end
   output.        
   It gives us the
   differences    
        |
        |
        v
 ~/PythonUI/finished.py
  |------------------|   
  |                  |   
  |                  |   
  |  this is wrong   |   
  |  formatting      |  
  |  technically     |  
  |  speaking>       |  
  |                  |  
  |------------------|  
