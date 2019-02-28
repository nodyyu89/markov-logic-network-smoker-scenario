# markov-logic-network-smoker-scenario
A simple python script makes use of Pracmln for social modeling and link prediction in complex network

To start:
please pip install pracmln first before running the main.py 

Pracmln is a time and pc memory consuming package, so it is recommended to run it in a server

2019-2-28:
It is noticed that the newest update of pracmln 1.2.3 contains some functions(located in dnutils) that is not applicable in windows system. Some import error occured when call the signal_.SIGNKILL and other relevant functions.
It is recommended to use pracmln 1.2.2 to run this script
