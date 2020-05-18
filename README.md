# MMX_ATA
Marble Machine X Automatic Timing Analyser

# This program was created for the MMX Project

## Goal
In Issue n#19, you said that the finding the delays of the different channels manually is too time consuming. It sounded like a nice challenge, so I wrote a program to do it automatically. 

## How does it work?

![explainer](https://github.com/ReinierZwikker/MMX_ATA/blob/master/MMX_ATA_explainer.png)

In the (very beautiful) paint graphic that you can see above, I explained the process of getting the timing from .wav files. By putting them in the input_files folder next to the program (timing_tester.py) and then running the program, it will look at all .wav in the folder and see where they suddenly spike and thus where the notes are. It has some parameters, like how big the spike needs to be and how long each spike approximatly is, so it doesn't register a note twice. It then outputs the delay of the first note of each channel with respect to the first note that it hears. It also detects the average note interval and it's standard deviation, so you can easily see how consistent each channel is.



## Future improvements
I could also change the program to look at the average delay, for a more reliable answer or add a suggestion how many spacers are needed to delay the channel so that it plays in time if I know how long one spacers delays the channel. The program is made in python and can be easily modified to better suit the needs of the mmx project.
