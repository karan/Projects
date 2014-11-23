Mega Project List
========

A list of practical projects that anyone can solve in any programming language (See [solutions](https://github.com/thekarangoel/Projects-Solutions)). These projects are divided in multiple categories, and each category has its own folder.

To get started, simply fork this repo.

## [CONTRIBUTING](https://github.com/thekarangoel/Projects/blob/master/CONTRIBUTING.md)

See ways of [contributing](https://github.com/thekarangoel/Projects/blob/master/CONTRIBUTING.md) to this repo. You can contribute **solutions** (will be published in this [repo](https://github.com/thekarangoel/Projects-Solutions)) to existing problems, **add new projects** or remove existing ones. Make sure you follow all instructions properly.


## [Solutions](https://github.com/thekarangoel/Projects-Solutions)

You can find implementations of these projects in many other languages by other users in [this repo](https://github.com/thekarangoel/Projects-Solutions).

## Donations

If *Projects* has helped you in any way, and you'd like to help the developer, please consider donating.

**- Gittip: [https://www.gittip.com/karan/](https://www.gittip.com/karan/)**

**- Flattr: [https://flattr.com/profile/thekarangoel](https://flattr.com/profile/thekarangoel)**

================================




Graph
--------

**Graph from links** - Create a program that will create a graph or network from a series of links.

**Eulerian Path** - Create a program which will take as an input a graph and output either a Eulerian path or a Eulerian cycle, or state that it is not possible.  A Eulerian Path starts at one node and traverses every edge of a graph  through every node and finishes at another node.  A Eulerian cycle is a eulerian Path that starts and finishes at the same node.

**Connected Graph** - Create a program which takes a graph as an input and outputs whether every node is connected or not.

**Dijkstra’s Algorithm** - Create a program that finds the shortest path through a graph using its edges.


Data Structures
---------

**Inverted index** - An [Inverted Index](http://en.wikipedia.org/wiki/Inverted_index) is a data structure used to create full text search. Given a set of text files, implement a program to create an inverted index. Also create a user interface to do a search using that inverted index which returns a list of files that contain the query term / terms. The search index can be in memory.


Networking
---------

**FTP Program** - A file transfer program which can transfer files back and forth from a remote web sever.

**Bandwidth Monitor** - A small utility program that tracks how much data you have uploaded and downloaded from the net during the course of your current online session. See if you can find out what periods of the day you use more and less and generate a report or graph that shows it.

**Port Scanner** - Enter an IP address and a port range where the program will then attempt to find open ports on the given computer by connecting to each of them. On any successful connections mark the port as open.

**Mail Checker (POP3 / IMAP)** - The user enters various account information include web server and IP, protocol type (POP3 or IMAP) and the application will check for email at a given interval.

**Country from IP Lookup** - Enter an IP address and find the country that IP is registered in. *Optional: Find the Ip automatically.*

**Whois Search Tool** - Enter an IP or host address and have it look it up through whois and return the results to you.

**Site Checker with Time Scheduling** - An application that attempts to connect to a website or server every so many minutes or a given time and check if it is up. If it is down, it will notify you by email or by posting a notice on screen.



Threading
---------

**Create A Progress Bar for Downloads** - Create a progress bar for applications that can keep track of a download in progress. The progress bar will be on a separate thread and will communicate with the main thread using delegates.

**Bulk Thumbnail Creator** - Picture processing can take a bit of time for some transformations. Especially if the image is large. Create an image program which can take hundreds of images and converts them to a specified size in the background thread while you do other things. For added complexity, have one thread handling re-sizing, have another bulk renaming of thumbnails etc.


Web
---------

**Page Scraper** - Create an application which connects to a site and pulls out all links, or images, and saves them to a list. *Optional: Organize the indexed content and don’t allow duplicates. Have it put the results into an easily searchable index file.*

**Online White Board** - Create an application which allows you to draw pictures, write notes and use various colors to flesh out ideas for projects. *Optional: Add feature to invite friends to collaborate on a white board online.*

**Get Atomic Time from Internet Clock** - This program will get the true atomic time from an atomic time clock on the Internet. Use any one of the atomic clocks returned by a simple Google search.

**Fetch Current Weather** - Get the current weather for a given zip/postal code. *Optional: Try locating the user automatically.*

**Scheduled Auto Login and Action** - Make an application which logs into a given site on a schedule and invokes a certain action and then logs out. This can be useful for checking web mail, posting regular content, or getting info for other applications and saving it to your computer.

**E-Card Generator** - Make a site that allows people to generate their own little e-cards and send them to other people. Do not use Flash. Use a picture library and perhaps insightful mottos or quotes.

**Content Management System** - Create a content management system (CMS) like Joomla, Drupal, PHP Nuke etc. Start small. *Optional: Allow for the addition of modules/addons.*

**Web Board (Forum)** - Create a forum for you and your buddies to post, administer and share thoughts and ideas.

**CAPTCHA Maker** - Ever see those images with letters a numbers when you signup for a service and then asks you to enter what you see? It keeps web bots from automatically signing up and spamming. Try creating one yourself for online forms.


Files
---------

**Quiz Maker** - Make an application which takes various questions from a file, picked randomly, and puts together a quiz for students. Each quiz can be different and then reads a key to grade the quizzes.

**Sort Excel/CSV File Utility** - Reads a file of records, sorts them, and then writes them back to the file. Allow the user to choose various sort style and sorting based on a particular field.

**Create Zip File Maker** - The user enters various files from different directories and the program zips them up into a zip file. *Optional: Apply actual compression to the files. Start with Huffman Algorithm.*

**PDF Generator** - An application which can read in a text file, html file or some other file and generates a PDF file out of it. Great for a web based service where the user uploads the file and the program returns a PDF of the file. *Optional: Deploy on GAE or Heroku if possible.*

**Mp3 Tagger** - Modify and add ID3v1 tags to MP3 files. See if you can also add in the album art into the MP3 file’s header as well as other ID3v2 tags.

**Code Snippet Manager** - Another utility program that allows coders to put in functions, classes or other tidbits to save for use later. Organized by the type of snippet or language the coder can quickly look up code. *Optional: For extra practice try adding syntax highlighting based on the language.*


Databases
---------

**SQL Query Analyzer** - A utility application which a user can enter a query and have it run against a local database and look for ways to make it more efficient.

**Remote SQL Tool** - A utility that can execute queries on remote servers from your local computer across the Internet. It should take in a remote host, user name and password, run the query and return the results.

**Report Generator** - Create a utility that generates a report based on some tables in a database. Generates a sales reports based on the order/order details tables or sums up the days current database activity.

**Event Scheduler and Calendar** - Make an application which allows the user to enter a date and time of an event, event notes and then schedule those events on a calendar. The user can then browse the calendar or search the calendar for specific events. *Optional: Allow the application to create re-occurrence events that reoccur every day, week, month, year etc.*

**Budget Tracker** - Write an application that keeps track of a household’s budget. The user can add expenses, income, and recurring costs to find out how much they are saving or losing over a period of time. *Optional: Allow the user to specify a date range and see the net flow of money in and out of the house budget for that time period.*

**TV Show Tracker** - Got a favorite show you don’t want to miss? Don’t have a PVR or want to be able to find the show to then PVR it later? Make an application which can search various online TV Guide sites, locate the shows/times/channels and add them to a database application. The database/website then can send you email reminders that a show is about to start and which channel it will be on.

**Travel Planner System** - Make a system that allows users to put together their own little travel itinerary and keep track of the airline / hotel arrangements, points of interest, budget and schedule.


Graphics and Multimedia
---------

**Slide Show** - Make an application that shows various pictures in a slide show format. *Optional: Try adding various effects like fade in/out, star wipe and window blinds transitions.*

**Stream Video from Online** - Try to create your own online streaming video player.

**Mp3 Player** - A simple program for playing your favorite music files. Add features you though are missing from your favorite music player.

**Watermarking Application** - Have some pictures you want copyright protected? Add your own logo or text lightly across the background so that no one can simply steal your graphics off your site. Make a program that will add this watermark to the picture. *Optional: Use threading to process multiple images simultaneously.*

**Turtle Graphics** - This is a common project where you create a floor of 20 x 20 squares. Using various commands you tell a turtle to draw a line on the floor. You have move forward, left or right, lift or drop pen etc. Do a search online for "Turtle Graphics" for more information. *Optional: Allow the program to read in the list of commands from a file.*

**GIF Creator** A program that puts together multiple images (PNGs, JPGs, TIFFs) to make a smooth GIF that can be exported. *Optional: Make the program convert small video files to GIFs as well.*


Security
-------------

**Caesar cipher** - Implement a Caesar cipher, both encoding and decoding. The key is an integer from 1 to 25. This cipher rotates the letters of the alphabet (A to Z). The encoding replaces each letter with the 1st to 25th next letter in the alphabet (wrapping Z to A). So key 2 encrypts "HI" to "JK", but key 20 encrypts "HI" to "BC". This simple "monoalphabetic substitution cipher" provides almost no security, because an attacker who has the encoded message can either use frequency analysis to guess the key, or just try all 25 keys.


Sources
=======

* [Martyr2’s Mega Project List](http://www.dreamincode.net/forums/topic/78802-martyr2s-mega-project-ideas-list/)
* [Rosetta Code](http://rosettacode.org/)
