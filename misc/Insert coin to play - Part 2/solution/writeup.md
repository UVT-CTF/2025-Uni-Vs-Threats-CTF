# Write-up | Insert coin to play - Part 2

Compared to the part 1 now you can't find the score address by searching for the score value since it's obfuscated

Attach the cheat engine to the game, activate `mono features`, then `dissect mono` after which you find the function `addScore` and then you `execute/invoke method` on usually the third address which is the score and it will increment the score value, thus obtaining the flag.