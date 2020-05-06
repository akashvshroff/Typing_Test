# Outline
  * A simple typing test GUI built using Python, tkinter and SQL. The test uses the time function and the Levenshtein distance to calculate wpm and accuracy. More details below.

# Purpose
  * The project was extremely engaging in production and helped me further understand the nuances of GUIs with Tkinter and SQL. It taught me how to convert an intangible vision into a tangible, achievable outline which can then be realised using as simple code as possible. Through this undertaking, I learnt the importance of documentation and the need for clear and concise code. Moreover, it was extremely fun trying to beat my friends in terms of typing speed and accuracy.

# Description
  * Tkinter is used to create a GUI on which the program rests, using its notebook feature in order to create a UI that allows for tabs such as Getting Started, Typing Test and Leaderboard.
  * In the Start tab, the user inputs their name, can read the instructions for the typing test and then use buttons for easy movement between tabs.
  * The Typing Test tab, there is a textbox that will display the string to type, a main entry box to input the string, buttons that include Start, Stop, Reset and buttons to traverse between tabs. When the user hits start, the string is displayed and the time is recorded and when the user hits stop, the time is noted.
  * The entry box will then display the user's accuracy and the words per minute. The accuracy is calculated using the  Levenshtein distance between the string to type and the inputted string. This system maps the two strings and notes the number of conversions is takes to get from one string to the other, displaying it as a percentage. The words per minute is derived by calculating the number of words in the inputted string by the time * 60. The calculation of the Levenshtein distance was conducted by the package fuzzywuzzy.
  * The program then passes the information (Name, WPM, Accuracy and wpm + acc) to an SQL database. This continues and the user can then click the update leaderboard button on the leaderboard tab which displays the top 5 scores. by retrieving the Scores table from the database, sorted in descending order by sum.
  * If the user enters a different name in the menu, the typing test strings reset and the next user can continue the test.
  * Buttons and tabs are constantly enabled and disabled to create a set path for the user, thereby averting errors.
