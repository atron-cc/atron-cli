## Atron CLI

> A tool to intract with your MicroPython board.
> Based on Adafruit MicroPython Tool (ampy)

### Usage

```
$ atron -p /dev/ttyACM0 <command>
```

**Note** In non-windows platforms default port is /dev/ttyUSB0.

### Commands

##### Upload

The `upload` command will upload a python file to pyboard. Selected python file will be automatically minify.

Example(s):

```
$ atron --port /dev/ttyACM0 upload main.py
$ atron --port /dev/ttyACM0 upload blink.py main.py
```

##### Reset

The `reset` command will reset the pyboard. Default reset mode is `soft-reset`.

Example(s):

```
$ atron --port /dev/ttyACM0 reset
$ atron --port /dev/ttyACM0 reset --hard
```

##### Rm

The `rm` command will remove selected file from pyboard.

Example(s):

```
$ atron --port /dev/ttyACM0 rm main.py
```

##### Put

The `put` command will put file or directory to selected path in pyboard.
Second argument (called remote) is optional.

Example(s):

```
$ atron --port /dev/ttyACM0 put main.py
$ atron --port /dev/ttyACM0 put main.py hello.py
$ atron --port /dev/ttyACM0 put example
```

##### Run

The `run` command will run a python file from computer in pyboard. All of python codes in selected file will pass to pyboard in `raw repl` mode. If you want to see output from pyboard do not pass `--no-output` to the command.

Example(s):

```
$ atron --port /dev/ttyACM0 run main.py
$ atron --port /dev/ttyACM0 run main.py --no-output
```

##### Raw Command

The `raw-command` is like raw-repl mode. Atron will get a command, execute it on pyboard and then show result to you.

Example(s):

```
$ atron --port /dev/ttyACM0 raw-command
```