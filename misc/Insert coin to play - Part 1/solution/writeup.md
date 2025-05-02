# Insert coin to play - Part 1


## Short description 

`The player is only able to get 5 coins since only 5 are inside the level so he must find a way to get more`

## Solution

The player must find the address of the score variable in order to change its value.
We open cheat engine and scan for all the adresses that have the value `0`
Then we collect a coin and nextscan for the new value and so on till we are left with only `1` coin and we find `4` addresses for the coin variable.

We change the variable value to anything above 9/10 and then we collect the last coin to update the score and we get the flag.