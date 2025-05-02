# Solution
Given a memory dump `cornelia-memory.raw` (after unzipping the archive) we analyze it using volatility3:

1. Scan for files:
```
sudo python3 vol.py -f cornelias-memory.raw windows.filescan
```

2. Filter for relevant filenames:
```
sudo python3 vol.py -f cornelias-memory.raw windows.filescan | grep -i cornelia  
sudo python3 vol.py -f cornelias-memory.raw windows.filescan | grep -i sawat
```

3. Dump the identified files (replacing `<address>` with the virtual address):
First, we can create a `dumps` directory to output the files there in order to be easier to navigate. Then, we mention this directory as the output path. We also use the address we got as an output from the previous commands, e.g. `0xb78741195900`.
```
sudo python3 vol.py -f cornelias-memory.raw -o dumps windows.dumpfiles --virtaddr <address>
```

Recovered files:

- `master-plan.txt`
- `kind-reminder.txt`
- `README-first.txt` (these 3 from `cornelia` search)
- `company-intel.7z` (from `sawat` search)

4. Read the text files:
```
cat dumps/file._master-plan_.dat  
cat dumps/file._kind-reminder_.dat  
cat dumps/file._README_.dat
```

The password is found in one of these files:
```
!!c4nN0L0ng3rIgn0r3Th1s
```

5. Extract the archive:
```
7z x dumps/file._company-intel_.dat -p"!!c4nN0L0ng3rIgn0r3Th1s"
```

The archive contains:
- A `.png` file 
- An optional `.txt` context file

The flag is inside the `.png` image, written on it.
