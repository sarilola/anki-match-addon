# Matching Exercises in Anki❓
Remember a concept, word or anything by associating it with a definition or any kind of information related to it.

This add-on creates a new note type and allows you to select it as the template for your notes in Anki. Personally, i'm not good at memorizing through simple flashcards so studying becomes easier to me using this note type for `retrieval practice`.
## How to install 
### Method #1. Through the anki website
I also uploaded this add-on to the [anki website](https://ankiweb.net/shared/info/353070086?cb=1754103047153). Start anki and go to `Tools>Add-ons>Get Add-ons` and paste the add-on code. You will have to restart anki after the installation.
### Method #2. Using the add-on file in this repository (.ankiaddon).
Download the file **"match_concepts.ankiaddon"** and execute it to install it.**❗IMPORTANT❗**After the installation, you will have to restart anki, however, you will have to use the terminal to do it as i don't know why the add-on does not work if you restart anki graphically.

Open your terminal and type `anki` to start it and the add-on should create the note type correctly. **DO THIS ONCE. AFTER THE INSTALLATION AND THE PROPER CREATION OF THE NOTE TYPE YOU ARE GOOD TO GO**.
### Method #3. Pasting the code in this repository in your local anki add-ons folder.
I don't recommend this method actually, but i included it in case none of the other methods worked for you. This is only for windows users, i'm pretty sure there are ways to do this in other OS, but i don't know how to do it at this moment. Open your AppData folder (`Win + R` and type `%appdata%`) and go to `Anki2>addons21`. Create a new folder with any name related to what this add-on does and paste all the files inside the folder [code](https://github.com/sarilola/anki-match-addon/tree/master/code) in it. Start Anki and the add-on is supposed to be working as soon as you start the program and listed in the add-on manager.
## How to use
1. Start Anki on your device.
2. Choose the deck where you want to add the new card.
3. Add a card and select "Matching Exercise" as note type.
4. Fill the fields. In case you need more fields, feel free to modify the code and create your own version with as much fields as you prefer. You can find my `discord` user at the bottom of this document, contact me if you have any question!
5. Click on `Study Now` and start.

The interface is quite simple and intuitive, each concept has its own definition, each definition is numbered so the dropdowns that contain the answers are legible. The definitions shuffle automatically each time the card is loaded in order to avoid memorizing the position and forcing you to actually remember what you are trying to memorize.

![](/images/front.png)

Click on the dropdown and select the number of the answer according to the concept/label on the left.

![](/images/front-working.png)

As soon as you click on the button `Show Answer`, the dropdowns that contain the correct answers will be highlighted in green, and the ones with incorrect answers will be highlihgted in red.

![](/images/back-correct.png)
![](/images/back-incorrect.png)

## Extra tools
To send data from the front to the back of the card, i used [anki persistence](https://github.com/SimonLammer/anki-persistence?tab=readme-ov-file). I highly recommend this in case you are interested in developing anki add-ons.
## Questions or Suggestions?
It's my first time writing anki add-ons, so there may be some mistakes or unnecessary lines of code. But if you have any question related to this or suggestions, contact me, i'll be glad to help ;).

[Discord: sarilolaaa](https://discordapp.com/users/1141563506152448090)
