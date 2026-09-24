import sys
import random
import time
try:
    import matplotlib.pyplot as plt
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout,
        QPushButton, QComboBox
    )
    from PyQt5.QtGui import QFont
    from PyQt5.QtCore import Qt
except ImportError:
    error_message = "Please install required Libraries:\n\npip install PyQt5 matplotlib"
    print(error_message)
    sys.exit(1)  # Exit the program gracefully

# global stuff
round_num = 0
the_paragraph = ""
startTime = 0
resultsList = []
all_feedback = []

# reads the paragraphs from the txt file
def get_paragraphs(filename="paragraphs.txt"):
    all_paragraphs = {"Easy": [], "Medium": [], "Hard": []}
    level = ""
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("["):
                    level = line.replace("[", "").replace("]", "")
                elif line != "":
                    if level in all_paragraphs:
                        all_paragraphs[level].append(line)
    except:
        print("oops, paragraphs.txt file is missing!")
    return all_paragraphs

# wpm calc
def get_wpm(mytext, time_in_mins):
    words = mytext.split()
    num_words = len(words)
    
    if time_in_mins > 0:
        wpm_score = num_words / time_in_mins
    else:
        wpm_score = 0
    return wpm_score

# accuracy calc
def get_accuracy(original, typed):
    og_words = original.split()
    my_words = typed.split()
    good_words = 0
    
    # check how many words match
    for i in range(len(og_words)):
        if i < len(my_words):
            if og_words[i] == my_words[i]:
                good_words = good_words + 1
            
    if len(og_words) > 0:
        acc = (good_words / len(og_words)) * 100
    else:
        acc = 0
    return acc

# efficiency calc
def get_efficiency(mytext, num_words):
    if num_words > 0:
        eff = len(mytext) / num_words
    else:
        eff = 0
    return eff

# gives you tips
def get_tips(wpm, acc):
    tips = []
    if wpm < 25:
        tips.append("Try to type faster. Practice makes perfect.")
    elif wpm < 45:
        tips.append("Good speed, keep it up.")
    else:
        tips.append("Wow, you are fast!")

    if acc < 80:
        tips.append("Slow down and focus on not making mistakes.")
    elif acc < 95:
        tips.append("Pretty good accuracy.")
    else:
        tips.append("Amazing accuracy! Almost no mistakes.")
        
    return tips

# shows mistakes in red
def show_mistakes(original, typed):
    og_words = original.split()
    my_words = typed.split()
    html = ""

    for i in range(len(og_words)):
        og_word = og_words[i]
        
        if i < len(my_words):
            my_word = my_words[i]
            if og_word == my_word:
                html += " " + og_word
            else:
                # make it red and bold if wrong
                html += f" <span style='color:red; font-weight:bold;'>{og_word}</span>"
        else:
            # if word is missing
            html += f" <span style='color:red; font-weight:bold;'>{og_word}</span>"
            
    return html

# makes the graphs at the end
def make_graphs():
    rounds = [1, 2, 3]
    wpms = []
    accs = []
    effs = []

    for r in resultsList:
        wpms.append(r["wpm"])
        accs.append(r["accuracy"])
        effs.append(r["efficiency"])

    plt.figure(figsize=(10, 8))

    # wpm plot
    plt.subplot(3, 1, 1)
    plt.plot(rounds, wpms, 'o-b')
    plt.title("Typing Speed")
    plt.ylabel("WPM")

    # accuracy plot
    plt.subplot(3, 1, 2)
    plt.bar(rounds, accs, color='green')
    plt.title("Typing Accuracy")
    plt.ylabel("Accuracy %")

    # efficiency plot
    plt.subplot(3, 1, 3)
    plt.plot(rounds, effs, 's-m')
    plt.title("Keystroke Efficiency")
    plt.ylabel("Chars per Word")
    plt.xlabel("Round")

    plt.tight_layout()
    plt.show()

# main program
def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Typing Test")
    window.setGeometry(100, 100, 800, 700)

    paragraphs = get_paragraphs()

    # all the stuff for the screen
    title = QLabel("Typing Speed Test")
    title.setFont(QFont("Arial", 20))
    title.setAlignment(Qt.AlignCenter)

    roundLabel = QLabel("Round 1 of 3")
    roundLabel.setFont(QFont("Arial", 12))
    roundLabel.setAlignment(Qt.AlignCenter)

    paragraphBox = QLabel("")
    paragraphBox.setWordWrap(True)
    paragraphBox.setStyleSheet("background-color: #eeeeee; padding: 10px; border-radius: 5px;")
    paragraphBox.setMinimumHeight(80)

    typingBox = QTextEdit()
    typingBox.setFont(QFont("Courier", 11))
    typingBox.setMinimumHeight(150)

    feedbackBox = QTextEdit()
    feedbackBox.setReadOnly(True)
    feedbackBox.setStyleSheet("background-color: #f0f8ff; padding: 10px; border-radius: 5px;")

    styleMenu = QComboBox()
    styleMenu.addItems(["Touch Typing", "Hunt-and-Peck"])

    startButton = QPushButton("Start")
    submitButton = QPushButton("Submit")
    restartButton = QPushButton("Restart")
    submitButton.setEnabled(False)

    # functions for the buttons
    def pick_paragraph():
        global the_paragraph, startTime, round_num
        startTime = 0
        
        # figure out difficulty
        difficulty = "Easy" # default
        if round_num == 1:
            last_wpm = resultsList[0]["wpm"]
            if last_wpm > 25:
                difficulty = "Medium"
            if last_wpm > 45:
                difficulty = "Hard"
        elif round_num == 2:
            avg_wpm = (resultsList[0]["wpm"] + resultsList[1]["wpm"]) / 2
            if avg_wpm > 25:
                difficulty = "Medium"
            if avg_wpm > 45:
                difficulty = "Hard"

        the_paragraph = random.choice(paragraphs[difficulty])
        paragraphBox.setText(f"Difficulty: {difficulty}\n\n{the_paragraph}")
        roundLabel.setText(f"Round {round_num + 1} of 3")
        typingBox.clear()
        startButton.setEnabled(True)

    def start_test():
        global startTime
        if startTime == 0:
            typingBox.setFocus()
            startTime = time.time()
            submitButton.setEnabled(True)
            startButton.setEnabled(False)

    # auto start when user types
    def typing_started():
        if startTime == 0 and len(typingBox.toPlainText()) > 0:
            start_test()

    def submit_test():
        global round_num
        endTime = time.time()
        time_taken = (endTime - startTime) / 60
        
        my_text = typingBox.toPlainText()
        num_words = len(my_text.split())

        # get scores
        wpm = get_wpm(my_text, time_taken)
        accuracy = get_accuracy(the_paragraph, my_text)
        efficiency = get_efficiency(my_text, num_words)

        resultsList.append({"wpm": wpm, "accuracy": accuracy, "efficiency": efficiency})

        tips = get_tips(wpm, accuracy)
        mistakes = show_mistakes(the_paragraph, my_text)

        # build the feedback string piece by piece
        feedback_html = "<h3>Round " + str(round_num + 1) + " Results</h3>"
        feedback_html += "<p><b>Speed:</b> " + str(round(wpm, 1)) + " WPM</p>"
        feedback_html += "<p><b>Accuracy:</b> " + str(round(accuracy, 1)) + "%</p>"
        feedback_html += "<p><b>Efficiency:</b> " + str(round(efficiency, 2)) + " chars/word</p>"
        feedback_html += "<h4>Your Text (Mistakes in Red):</h4>"
        feedback_html += "<p style='font-family: Courier;'>" + mistakes + "</p>"
        feedback_html += "<h4>Tips:</h4>"
        feedback_html += "<ul><li>" + "</li><li>".join(tips) + "</li></ul>"
        
        all_feedback.append(feedback_html)
        feedbackBox.setHtml("<hr>".join(all_feedback))

        round_num = round_num + 1
        submitButton.setEnabled(False)

        if round_num == 3:
            startButton.setEnabled(False)
            roundLabel.setText("Done! Check out your graphs!")
            make_graphs()
        else:
            pick_paragraph()

    def restart_game():
        global round_num, resultsList, all_feedback
        round_num = 0
        resultsList = []
        all_feedback = []
        typingBox.clear()
        feedbackBox.clear()
        pick_paragraph()
        submitButton.setEnabled(False)

    # make the screen layout
    layout = QVBoxLayout()
    layout.addWidget(title)

    top_bar = QHBoxLayout()
    top_bar.addWidget(QLabel("My Typing Style:"))
    top_bar.addWidget(styleMenu)
    top_bar.addWidget(startButton)
    top_bar.addWidget(submitButton)
    top_bar.addWidget(restartButton)

    layout.addLayout(top_bar)
    layout.addWidget(roundLabel)
    layout.addWidget(paragraphBox)
    layout.addWidget(QLabel("Type here:"))
    layout.addWidget(typingBox)
    layout.addWidget(QLabel("Feedback:"))
    layout.addWidget(feedbackBox)

    # connect buttons to functions
    startButton.clicked.connect(start_test)
    submitButton.clicked.connect(submit_test)
    restartButton.clicked.connect(restart_game)
    typingBox.textChanged.connect(typing_started) # for auto-start

    pick_paragraph() # start the first round

    # show the app
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())

# run the code
if __name__ == "__main__":
    main()
