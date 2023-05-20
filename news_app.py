#Importing the libraries
import io
import webbrowser
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk,Image

#Creating NewsApp class
class NewsApp:

    def __init__(self):
        # fetch data using requests library
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey'
                            '=2adafe470f26400e9ec47c6fa28281b8').json()     #.json() helps us to get the json data as python object
        # loading initial gui
        self.load_gui()
        # load the first news item
        self.load_news_item(3)


    # Function to load GUI window
    def load_gui(self):
        self.root=Tk()
        self.root.title("My News App")
        self.root.geometry('350x650')
        self.root.resizable(0,0)
        self.root.configure(bg='black')


    def clear(self):
        ''' All entities like label, button on gui window are pack_slaves
         which get deleted one by one '''
        for i in self.root.pack_slaves():
            i.destroy()

    # Function to load news items
    def load_news_item(self,index):
        #clear the screen for the next news item
        self.clear()

        #loading the image
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350,250))
            photo = ImageTk.PhotoImage(im)
        except:
            # default image will be loaded in case image can't be displayed from API
            img_url = "https://example.com/default_image.jpg"
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)

        #placing image on the label
        label = Label(self.root,image=photo)
        label.pack()

        #fetching heading of the news
        heading = Label(self.root,text=self.data['articles'][index]['title'],bg='black',
                        fg= 'white',wraplength=350,justify='center')
        heading.pack(pady=(10,20))
        heading.config(font=('verdana',15))

        #fetching news descriptions
        detail = Label(self.root, text=self.data['articles'][index]['description'], bg='black',
                        fg='white', wraplength=350, justify='center')
        detail.pack(pady=(2, 20))
        detail.config(font=('verdana', 10))

        # Creating frame for placing buttons
        frame = Frame(self.root,bg='white')
        frame.pack(expand=True,fill=BOTH)

        if index!=0:
            prev = Button(frame,text='Prev',width=16,height=3,command=lambda :self.load_news_item(index-1))
            prev.pack(side=LEFT)

        read = Button(frame, text='Read More', width=16, height=3,
                      command=lambda :self.read_more(self.data['articles'][index]['url']))
        read.pack(side=LEFT)

        if index!=len(self.data['articles'])-1:
            next = Button(frame, text='Next', width=16, height=3,command=lambda :self.load_news_item(index+1))
            next.pack(side=LEFT)

        self.root.mainloop()

    def read_more(self,link):
        webbrowser.open(link)

obj = NewsApp()