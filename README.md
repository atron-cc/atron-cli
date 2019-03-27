## Atron CLI
> A tool to intract with your MicroPython board.
> Based on Adafruit MicroPython Tool (ampy)

### Usage

```
$ atron -p /dev/ttyACM0 <command>
```

Commands:

- upload
    - arguments:
        - local_file (default='main.py')
        - remote_file (default='main.py')
    
- rm
    - arguments:
        - local_file

- put
    - arguments:
        - local (directory or file)
        - remote (optional)

- reset
    - flags:
        - hard --hard | -h (default=False)