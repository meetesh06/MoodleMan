import sys

class Log:
  @staticmethod
  def jsonError(msg):
    print("{error: true, msg: \"" + msg + "\"}")
    sys.exit(1)

  @staticmethod
  def local(msg):
    print("(*) ", msg)

  @staticmethod
  def localException(msg):
    print("(E) ", msg)
