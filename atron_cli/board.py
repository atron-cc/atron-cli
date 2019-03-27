import serial
import time
import ampy
from ampy.pyboard import PyboardError
from ampy.files import PyboardError as FilesError
from ampy.files import DirectoryExistsError


COMMAND_CTRL_A = b'\r\x01'
COMMAND_CTRL_B = b'\r\x02'
COMMAND_CTRL_C = b'\r\x03'
COMMAND_CTRL_D = b'\r\x04'


class BoardException(BaseException):
    pass


class Board:
    def __init__(self, device, baudrate=115200):
        try:
            self.board = ampy.pyboard.Pyboard(
                device=device,
                baudrate=baudrate,
            )
            self.files = ampy.files.Files(self.board)
        except (PyboardError, OSError, IOError):
            raise BoardException('failed to access ' + device)
        except FilesError:
            raise BoardException('failed to access files on ' + device)

    def close(self):
        self.board.close()

    def soft_reset(self):
        serial = self.board.serial

        serial.write(COMMAND_CTRL_C)
        time.sleep(0.1)
        serial.write(COMMAND_CTRL_C)

        n = serial.inWaiting()
        while n > 0:
            serial.read(n)
            n = serial.inWaiting()

        time.sleep(0.1)
        serial.write(COMMAND_CTRL_D)
        data = self.board.read_until(1, b'soft reboot\r\n')
        if not data.endswith(b'soft reboot\r\n'):
            raise BoardException('could not soft_reset')
