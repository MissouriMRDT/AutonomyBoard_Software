from core.rovecomm import RoveCommPacket
from core.rovecomm_TCP import RoveCommPacket as RoveCommPacketTCP
import core
import logging
from datetime import datetime


class CsvHandler(logging.handlers.WatchedFileHandler):

    def __init__(self, filename, format_string, encoding=None, delay=False):
        """
        Initializes the handler
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        f = open(f'{filename[:-4]}-{timestamp}{filename[-4:]}', 'w')
        f.write(format_string + '\n')
        f.close()

        logging.handlers.WatchedFileHandler.__init__(self, f'{filename[:-4]}-{timestamp}{filename[-4:]}', 'a', encoding, delay)


class RoveCommHandlerUDP(logging.Handler):

    def __init__(self, target_host, target_port):
        """
        Initializes the handler with given network variables
        """
        logging.Handler.__init__(self)
        self.target_host = target_host
        self.target_port = target_port

    def emit(self, s):
        """
        Encodes and sends the log message over RoveComm
        """
        if core.rovecomm_node is None:
            logging.warning('UDP Handler called with no socket')
            return

        msg = self.format(s)
        # Max string size is 255 characters, truncate the rest and flag it
        if len(msg) > 255:
            msg = msg[:252] + "..."

        packet = RoveCommPacket(
            4242,
            's',
            tuple([char.encode('utf-8') for char in msg]),
            "",
            self.target_port
        )
        packet.SetIp(self.target_host)
        core.rovecomm_node.write(packet)


class RoveCommHandlerTCP(logging.Handler):
    def __init__(self, target_host, target_port):
        """
        Initializes the handler
        """
        logging.Handler.__init__(self)
        self.target_host = target_host
        self.target_port = target_port

    def emit(self, s):
        """
        Encodes and sends the log message over RoveComm
        """
        if core.rovecomm_node_tcp is None:
            logging.warning('TCP Handler called with no socket')
            return

        msg = self.format(s)
        # Max string size is 255 characters, truncate the rest and flag it
        if len(msg) > 255:
            msg = msg[:252] + "..."

        packet = RoveCommPacketTCP(
            4242,
            's',
            tuple([char.encode('utf-8') for char in msg]),
            "",
            self.target_port
        )
        packet.SetIp(self.target_host)
        core.rovecomm_node_tcp.write(packet)