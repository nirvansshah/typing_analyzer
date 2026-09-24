# Typing Analyzer

Typing Speed Test Program written in Python
What it does
This is a program I made to test how fast you can type.
You type a paragraph, and it tells you your speed (WPM) and your accuracy. It has 3 rounds, and after you finish, it shows you a graph of your results.

Features
Gets Harder: The paragraphs get more difficult if you're doing well.
Shows Your Score: Tells you your Words Per Minute (WPM) and accuracy percentage.
Highlights Mistakes: Shows you which words you typed wrong in red.
Shows a Graph: At the end of 3 rounds, a graph pops up to show if you improved.
Auto-Start: The clock starts as soon as you type your first letter.

How to Run It
Install the requirements: Open your computer's terminal and run this command. This will install the libraries the program needs to work.

pip install -r requirements.txt

If you don’t want to use requirements.txt, you can just install manually:
pip install PyQt5 matplotlib

Run the program: In the same terminal, run this command.

python typing_speed_analyzer.py

The program window should now open. Make sure the paragraphs.txt file is in the same folder.
