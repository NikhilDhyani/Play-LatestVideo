global process
import io,sys,os
import subprocess
from bs4 import BeautifulSoup
import requests
import webbrowser
import re
p=0
i=0
list1=[]
def channel(response):
    z=1
    if response.status_code==200:
       
       data = response.text
       soup = BeautifulSoup(data,"lxml")
       
       #Find all h3 tags
       for x in soup.find_all("h3",{"class":"yt-lockup-title"}) :
           for link in x.find_all('a'):
               y=link.get('href')
               if not re.search(r'https://googleads.g.doubleclick.net',y):
                      if re.search(r'/user',y) or re.search(r'/channel',y):
                         
                         z=y
                         
                         return z
       if z==1:
          print("Channel/user doesn't exist or check your spelling. Search only for video")
         
          return(z)
                          
                  
def video_info(response):
    if response.status_code==200:
       data = response.text
       soup = BeautifulSoup(data,"lxml")
       
       #ONLY SELECT THE FIRST H3 TAG
       for x in soup.find_all("h3", {"class":"yt-lockup-title "},limit=1):
           for link in x.find_all('a'):
               print(link.get('title'))
       print("views and uploaded :\n")
       for ul in soup.find_all("ul",{"class":"yt-lockup-meta-info"},limit=1):
           for li in ul.find_all('li'):
               print(li.next)
       for x in soup.find_all("h3",{"class":"yt-lockup-title"}) :
           for link in x.find_all('a'):
               y=link.get('href')
               print("\n")
               print("If result is incorrect check spelling of artist or channel")
               return y 

      
def video(resposne):
    Response = response
    y=1
    
    if  response.status_code==200:
       
        data = response.text
        soup = BeautifulSoup(data,"html.parser")        	
     
        for x in soup.find_all("h3",{"class":"yt-lockup-title"}):
            
            global i
            global list1
            
            i=i+1
            
            global list1
            for link in x.find_all('a'):

                y=link.get('href')
                z=link.get('title')             
                
                global p
                if p==0:
                   # CHECK IF IT IS AN AD OR NOT 
                   if not re.search(r'https://googleads.g.doubleclick.net',y):
                          
                          if re.search(r'/user',y) or re.search(r'/channel',y):                          
                             
                                 p=1
                                 
                                 print("Title[%s](CHANNEL) = %s"%(i-1,z))
                                 
                                 list1.insert(i-1,y)                              
                                
                          else:
                              p=1
                              print("Title[%s] = %s"%(i-1,z))
                              list1.insert(i-1,y)                           
                                 
                else:
                   if not re.search(r'/user',y) or re.search('r/channel',y):
                      print("Title[%s] = %s"%(i-1,z))
                      list1.insert(i-1,y)
                       
                      #Check if it is an ad or not
                      if not re.search(r'https://googleads.g.doubleclick.net',y):
                             if not re.search(r'/user',y) or re.search(r'/channel',y):                             
                                    print "\n"
                   else:
                        print("Title[%s](Channel) = %s"%(i-1,z))
                        list1.insert(i,y)
                        
                        #print("i=%s "%(i))           
    if y==1:
       return y                                           
cond=True         
while(cond):
 name  = (raw_input("please enter the name to search\n>"))

 choice=raw_input("Is it a channel name y or n\n>")
 response = requests.get("https://www.youtube.com/results?search_query="+name)
 if(choice=='y'):   
   k=channel(response)
   if k!=1:
  
      response = requests.get("https://www.youtube.com"+k+"/videos")
    
      z=video_info(response)
     
      choice = raw_input("want to watch y or n\n>")
      if choice=="y":
         link = "https://www.youtube.com"+z
         print(link)
         option=raw_input("vlc(v) or youtube(y)\n>")
         if option=='v':
            myprocess = subprocess.call(['vlc','-vvv',link])
         else:
            webbrowser.open(link)   
         
      par = raw_input("want to continue y or n\n>")   
      if par=='n':
         cond=False
 else:
      
      data = response.text
      soup = BeautifulSoup(data,"lxml")
      response = requests.get("https://www.youtube.com/results?search_query="+name)
      z =video(response)
      print("If result is incorrect check spelling of artist or channel")
      choice = int(raw_input("please enter the choice to play video. If not interested type -1\n>"))
      
      if choice!=-1:
         link = "https://www.youtube.com"+list1[choice]
         option=raw_input("vlc(v) or youtube(y)\n>")
         if option=='v':
            myprocess = subprocess.call(['vlc','-vvv',link])
         else:
            webbrowser.open(link)
      par = raw_input("want to continue y or n\n>")   
      if par=='n':
         cond=False
      i=0
      p=0          
