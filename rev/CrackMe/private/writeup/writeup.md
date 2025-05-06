# IMPORTANT
This writeup is best consumed with the auxiliary files. There should be a zip around here somewhere conaining them. 
I will obviously refer to the files by their filename.

# In the beginning
We had a page prompting us for a password (photos/initialpage.jpg). Looking at the network tab after hitting the "check password" button we can see that the page does not communicate with the outside world. 
The next step that I would take would be to just get a local copy of the code for testing, you won't be surprised when I also tell you that is what I did. I use firefox and in my case it's right click and "save page as".
The result of saving the page is crackme_original.html and the folder crackme_original_files. Let's look at the code...

Did you look at the code with me ? No ? Then you are not getting much out of this writeup, are you? Come on, let's look at the code.
We can see that it is minified, as all self respecting JS code served over the network is. We can use something like https://unminify.com/ to unminify it (main_unminified.js).

# Real talk
I looked a bit at the unminifed.js to try and understand it. I felt it was natural to find the button click handler and start from there. The developer tools in firefox showed me the event handler without hassle (eventhandler.jpg), the only issue being is that it is showing it in the minified code. We have to do something about our testing setup as we cannot debug the minified code properly. What I did was copy the crackme_original.html and modify the line in it that loads the minified js to load our unminified js instead (crackme_unminified.html).

Now we can debug something a little more palpable (unminifieddebug.jpg). Now that i knew where to look I spend some time looking around, I got nowhere because I felt like I was fighting a computer. A computer can follow some rules as many times as needed but my focus reserves quickly deplete the more I keep doing repetitive stuff like trying to unobfuscate code by hand. So I started looking for some tools to help out, it turns out that https://obf-io.deobfuscate.io/ can do a good job with that. (main_deobfuscated.js).

We can do the same trick again by modifying the crackme_original.html to use our main_deobfuscated.js and we can start debugging.

# The VM
What I ended up doing was looking at the code, doing some debugging and annotating what I felt like the functions did. I think that this is applicable to all VM reversing but when you are debugging you get the feeling that you want to zoom out a bit. I do that by tracing what the VM is executing in some way.
Something tells me that there might have been a better way, but what I ended up doing was to manually insert console.log statements printing out the operations done by the VM and the operands (main_annotated.js). Guess what we do now ? We do the modification to run our annotated file ()

# Tracing the flag
Like any good scientist we start simple, let's see a trace for the case when we input a single character as the password (log.jl). I annotated the log as well, we can shift our focus inside of that log.
After seeing the first log I felt pretty good about myself and decided that i'll skip doing the log for two chars by putting my assumption to the test, that case 10: from the switch is basically an if construct. I patched case 10 in the switch to never jump to the code handling the else part and produced another log (log_2.jl). The only important piece of info to be extracted from that log is that the code checks 21 times that some modified input char is some value. So our password must be 21 chars, right ? Yes, it turns out to be right. 
Now that we know the length of the password, we can do another cool trick and just overwrite the inputArray with a static array, this allows us to better debug and test to see what is the correct input, so I created an array containing 21 values, from 0 to 20, the idea is to use that to see what the 
correct input is. We can just leave the case 10 patch and focus on the comparison result and the shuffles.
I did not annotate all of the log_3.jl file, I just did one example of what I had to do for 21 values, it was a bit tedious but I felt like it might take more to automate than to just do by hand.
You can find my annotation by searching for "# EXAMPLE" in the log_3.jl file.
```
22	resultSet[1699] = resultSet[1][resultSet[1692](2)]; = 43
		checking equals to 83
8	resultSet[1694] = 43(resultSet[1699]) === 83(resultSet[1693]) = false
```
Opcode 8 does the check, that is easy to see. At opcode 22 we load from resultSet[1][2] the modified, scrambled input char value. We need to figure out what was this supposed to be.
I think that I skipped a step, initially I wasn't making such beautiful logs and I did not really know where the data that was checked came from. But we can just follow references in reverse and we can easily arrive at switch case 14, where we swap some values from the array and we modify one of them. We can also look at the logs and code and determine that that is the only place where items from the array resultSet[1] will get modified.
I also modified log output to be easier to follow. The final trick that I used was to use VSCode's search function to follow the swaps and operations done.
So coming back at the example, opcode 22 checks resultSet[1][2]. Since I rewritten the logging code to output a[N] when accessing resultSet[1][N] we can search for a[2] (search.jpg), you can see in the photo that i get a nice chronological list of accesses to a[2]. Keep in mind that at the start a[] contains the input password as is. Let's start from the end, we can see that we have a line wher a[2] is swapped with a[2], and then a[2] will get modified, it is also worthy to note that whatever is at a[2] must be 83 after the operations, so looking at the operations done:
```
ichar ^= 220091176
ichar &= 255
```
since after the operations ichar must be 83, we can reverse the ops and get the initial value, we can do this by:
```
val = (83 ^ 220091176) & 255 = 123
```
good, we have found that at a[2] we must have the value 123. But let's not forget that the code also scrambles the array values, let's look again at the VSCode (or whatever other tool output) and let's see where does the value in a[2] come from. We can see that there is a swap(a[2],a[3]) made before. Cool, well, let's see where the value from a[3] comes from. It comes from nowhere, by searching for a[3] we can see that it is not swapped and comes directly from input array, so this means that at index 3 in the input array we must have 123, which is the character '{'.
I just did all of this by hand and got the flag. Cool stuff.