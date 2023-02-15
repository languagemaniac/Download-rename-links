# Download-rename-links
In short, this lets you download a series of urls you have written in newlines in a txt file. It renames the files to 1.mp3, 2.mp3, etc.

I wrote this because I constantly need to download audio for japanese words and keep track of what audio belongs to what word in my excel file.
The goal was to find a way in which a program would read all the urls I previously generated with Microsoft Excel based on japanese words, and just renamed the downloaded files according to the number for that word in excel (the line number, starting from 1).

As my python skills couldn't quite achieve this goal, I asked ChatGPT, and after several "revisions" of the code, I think I got the ultimate mp3 link Download&Rename tool.

So here's how it works:

  1. Create a txt file named "urls.txt" containing all the urls you want to download in newlines.
  2. Execute downloader.py (by executing "Python downloader.py")
  3. It's going to ask you what line of the text file do you want to start from (this is because a previous code crashed when trying to download a file and couldn't keep downloading and I wanted to retry downloading from the last sucessfull download) but it's really not necessary now as I implemented ways to avoid this issue)
  4. It's going to start downloading several urls in parallel!

Now, the server I wanted to download files from gave me this "maximum tries exceeded" error, so I made ChatGPT implement a way for the code to retry downloading those later. 

I also didn't notice I had an empty line in my txt file which resulted in a "invalid url" error, so I also made chatgpt implement a way to tell me which urls couldn't be downloaded at the end of the process and why. It writes that in the file "errors.txt", although if you have an empty line, it won't tell you which url is it that failed, because there is no url to display... maybe just check your txt file then)
