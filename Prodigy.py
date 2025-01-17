import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern 
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
        else:
            result = "Sorry I cannot understand"
    return result


#Creating tkinter GUI
import tkinter 
from tkinter import *

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatBox.config(state=NORMAL)
        ChatBox.insert(END, "You: " + msg + '\n\n')
        ChatBox.config(foreground="#446665", font=("Verdana", 12 ))
    
        ints = predict_class(msg)
        res = getResponse(ints, intents)
        
        ChatBox.insert(END, "Prodigy: " + res + '\n\n')
            
        ChatBox.config(state=DISABLED)
        ChatBox.yview(END)
 

root = Tk()
root.title("Prodigy- AI chatbot of DAV School")
root.geometry("1366x768")
#root.attributes('-fullscreen', True)
root.iconbitmap('logo.ico')
root.resizable(width=FALSE, height=FALSE)

#Create Label to show logo
photo = PhotoImage(file="chatboticon.png")
photolabel = Label(image=photo)

#Create Label
header = Label(root, 
		 text="Hi! I am Prodigy \n The AI Chatbot here to guide you \n Go ahead and send me a message",
		 fg = "blue",
		 font = "Helvatica 20 italic")
#school image
schoolphoto = PhotoImage(file="chatboticon.png")

#Create Chat window
ChatBox = Text(root, bd=0, bg="white",height="8", width="50", font="Arial",)

ChatBox.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(root, command=ChatBox.yview, cursor="heart")
ChatBox['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(root, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#f9a602", activebackground="#3c9d9b",fg='#000000',
                    command= send )

#Create the box to enter message
EntryBox = Text(root, bd=0, bg="white", fg="green",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
#chatboticon.place(x=6, y=6)
photolabel.place(x=10, y=6)
header.place(x=400, y=50)
scrollbar.place(x=1336,y=6, height=615)

#ChatBox.place(x=6,y=6, height=386, width=360)
ChatBox.place(x=900,y=6, height=650, width=435)
EntryBox.place(x=900, y=660, height=90, width=350)
SendButton.place(x=1255, y=660, height=90,width=100)

root.mainloop()
