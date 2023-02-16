# Download-rename-links
In short, this lets you download a series of urls you have written in newlines in a txt file. It renames the files to 1.mp3, 2.mp3, etc.

I wrote this because I constantly need to download audio for japanese words and keep track of what audio belongs to what word in my excel file.
The goal was to find a way to download a list of URLs with a program that would read all the URLs I previously generated with Microsoft Excel based on japanese words (by altering a URL parameters with a formula), and just renamed the downloaded files according to the number for that word in excel (first word in excel being URL number 1 in the list, so starting from 1.mp3).

As my python skills couldn't quite achieve this goal, I asked ChatGPT, and after several "revisions" of the code, I think I got the ultimate mp3 link Download&Renamer tool.

So here's how it works:

  1. Create a txt file named "urls.txt" containing all the URLs you want to download, in newlines.
  2. Execute LinkDownloader.py (by executing "Python LinkDownloader.py")
  3. It's going to ask you what line of the text file do you want to start from (this is because a previous code crashed when trying to download the list of files and I wanted to retry downloading from the last sucessfull download, but it's really not necessary now as I implemented ways to avoid this issue, but I left it there just in case)
  4. It's going to start downloading several urls (in parallel!) and retrying failed downloads.
  5. When it finishes, it will generate a txt file named "errors.txt" with a list of URLs it couldn't download and why, if for whatever reason fails to download a URL after several tries and the program finishes without having downloaded it.


The server I wanted to download files from gave me this "maximum tries exceeded" error, so I made ChatGPT implement a way for the code to retry downloading those later. 

I also didn't notice I had an empty line in my txt file which resulted in a "invalid url" error, so that's why I also made ChatGPT implement a way to tell me which urls couldn't be downloaded at the end of the process and why. Although if you have an empty line like I did, it won't tell you which url is it that failed, because there is no url to display... maybe just check your txt file then)

I tried this with a list of over 2000 URLs and it successfully downloaded all of them!

