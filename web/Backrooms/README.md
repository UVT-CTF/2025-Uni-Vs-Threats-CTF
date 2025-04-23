# Backrooms
> author: abcjr, category: web

### Description
You find yourself in an endless maze of forgotten tabs, flickering lights, and scripted puppets bound to loops they can’t escape. They walk. They click. They reload. Over and over again.

In this realm, user agents are gods, and every gesture is watched.

To dig deeper, you must speak not like a user, but like the machine.

Strip away the interface. Learn their language. Speak their truth.
The door is there... if you know how to ask.

*"Open, sesame."*

**Running the docker container locally:**
```bash
docker rm -f backrooms
docker build -t backrooms .
docker run --name=backrooms --rm -p8080:8080 -it backrooms
```

### Flag
<details>
  <summary>Click to reveal the flag</summary>
  UVT{st0p_sn00p1n9_4r0und}
</details>
