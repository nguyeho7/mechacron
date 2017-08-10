# mechacron
A crontab-based personal assistant which utilizes a thermal printer to communicate

Our main goal is to have a framework to easily add cronjob tasks (Decepticalls)
to a raspberry connected to a thermal printer. Each Decepticall will implement 2 
functions, daily\_summary() and weekly\_summary(). The output if each function
will be a string of a certain max length. Ideally, they should be formated to be
readable on the paper. The output can be empty. Mechacron will wrap around 
each Decepticall and print their output at given intervals.

Currently planned Decepticalls are:
- a facebook page guestbook, where people can leave messages to be printed
- a google calendar with both daily and weekly summaries
- a bookdepository based telegram/facebook chatbot that parses links and 
	estimates upcoming arrival dates 
- a homework deadline reminder based on CTU api (?)
- anime reminders based on MAL
- lightweight RSS (?)
