# Welcome To PicOS
## what is PicOS?
PicOS is an operating system that is like IOS, but it is made by me. and it runs on a raspberrypi pico 1WH, this OS was designed to be used with the 3.5" waveshare st7796s. i recentley (oct 13 2026) got one on amazon.com and used it at first for a simple drawing device, then i added a clear button, and then i thought about making a simple game tablet, and then the idea hit me like a comercial airplane: "_**Make a Phone**_" and so i did. and here is V03 of the OS.
## why (_Not_) PicOS?
Picos was made for me specificly. it has no wireless usage so that i can use it at school. so if you can find a better version of PicOS, go for it.
## Apps
Apps? of course i added apps. why wouldnt I?
### list
the 8 default apps on here include:
app store
clock
info
settings
calc(ulator)
notes
paint
photos
### make your own
go down to developer at the bottom.
### app info
here is some info on each app (all logos and functionality were based on MacOS apps)
#### store
you can get apps (all are free. i dont have a money system yet and i likely never will) Logo based on app store logo from MacOS
#### clock
this app tells you the time in millitary time logo based on "clock" app on MacOS.
#### info
gives system data, logo based off of "tips" app on MacOS
#### settings
system settings for basic stuff. like password and stuff. Logo based on MacOS "system settings" app
#### calc(ulator)
has 9 buttons (1-9) no 0 button, and no function buttons, good luck cheating on a math test with this, HA!
#### notes
(should) let you type a note (it currently just shows a black screen)
#### paint
lets you make and save drawings (adding editing drawings & multicolor soon!)
#### photos
stores your drawings
## Home and wallpaper
the wall paper is a black screen with a green tp left corner and a cyan bottom right corner
home screen has the wallpaper behind the apps too.
## image system
images work in a very strange way, at the top of a file there is a header with dimentions in it.
(Ex: 30x30) and below that each of the 30 (in this case) lines are filled with values 0-f (_yes, lowercase_)
and it goes a,r,g,b EX: (2x2;0f0000f0;00f00f00)
