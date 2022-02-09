# Running long simulations

You might want to start long simulations, but this requires a bit of extra work. If you start the simulation in the login session, you need to keep the SSH connection alive and not e.g. close down your computer, close terminal etc. to avoid killing/stopping the simulations process. To avoid this problem you have to start the simulations through a mechanism that allows you to "detach" from the running process.

There are multiple options for running long simulations in a detached session, the most common being `screen` , `tmux` and `byobu`. Here well show how to get started using screen

Start a new screen:
```bash
$ screen
```
and press [Enter] to acknowledge the terms. You should now see a fresh session. In this session you can start your simulations. When the simulations are running, hit [Ctrl+a d] to "detach". You should now be in your login session again. Now try

```bash
$ screen -ls
There is a screen on:
	1463.pts-0.screen-test	(09/09/21 09:48:48)	(Detached)
1 Socket in /run/screen/S-ubuntu.
```

and you should see a single screen that is detached. You can start multiple screens using `screen` again. To re-attach to a detached session, you can do:

```bash
$ screen -r
```

to reattach if you only have one screen, or:

```bash
$ screen -r 146
```

or the few first characters of the screen name to re-attach a particular screen session. When attached, you can then inspect standard output for simulation progress.

You can read more about screen on the internet, e.g. [a guide](https://linuxize.com/post/how-to-use-linux-screen/) or [a cheatsheet](https://kapeli.com/cheat_sheets/screen.docset/Contents/Resources/Documents/index)

As mentioned, you can also use more advanced session managers such as [tmux](https://en.wikipedia.org/wiki/Tmux) and [byobu](https://en.wikipedia.org/wiki/Byobu_(software)). Please consult additional guides for this.
