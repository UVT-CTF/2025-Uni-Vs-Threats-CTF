# Flag Shredder
> author: MrProperCTF, category: forensics

### Description
Our top operative was moments away from exfiltrating a critical piece of intel when their USB drive was hastily wiped. All that remains is this disk image: freeflags.img.

On it, you'll find a suspicious executable that seems to be doing... something.

See if you can solve the case, we are counting on you!
### Flag
<details>
  <summary>Click to reveal the flag</summary>
  UVT{D3l3t3d_But_N0t_D3stRoy3d}
</details>

## Solution

After mounting or analyzing the image, we discover a Python script named something like `flag_factory.py` or similar. This file runs a loop that creates fake flag files on the desktop at 1-second intervals for 100 seconds.
This in only a red herring since the fake flags are UVT{Flag_Deleted_Try_Harder}, which makes us think about deleted files on the image.

Real flag can be recovered using data recovery tools such as photorec/foremost. Once you run the program you will see that a png file was deleted from the image, after recovering it the flag is in the png file :  UVT{D3l3t3d_But_N0t_D3stRoy3d}
