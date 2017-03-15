import logging
import socket
from logging.handlers import SysLogHandler


class ContextFilter(logging.Filter):
  hostname = socket.gethostname()

  def filter(self, record):
    record.hostname = ContextFilter.hostname
    return True

  def log_to_file(getTitle,netID,createdCourseID):

      logger = logging.getLogger()
      logger.setLevel(logging.INFO)

      f = ContextFilter()
      logger.addFilter(f)

      syslog = SysLogHandler(address=('logs5.papertrailapp.com', 27968))
      formatter = logging.Formatter('%(asctime)s %(hostname)s Auto_Organizations: %(message)s',
                                    datefmt='%b %d %H:%M:%S')

      syslog.setFormatter(formatter)
      logger.addHandler(syslog)

      logging.info('The organization '"{}"' was created by '"{}"', with the ID '"{}"''.format(getTitle, netID, createdCourseID))











