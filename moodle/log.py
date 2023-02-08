import sys
import tempfile
import datetime

class Log:
  """
  Contains methods to separate outputs to different streams.

  The frontend should see a simplified error message whereas we maintain detailed logs for execution separately.
  """

  PrintLocal=None

  @staticmethod
  def initLocalLog(path):
    Log.PrintLocal = type('', (), {})()
    Log.PrintLocal.name = path
    Log.local("Start new session")

  @staticmethod
  def initTempLog():
    Log.PrintLocal = tempfile.NamedTemporaryFile()


  @staticmethod
  def printLog():
    if (Log.PrintLocal == None):
      Log.jsonError("backend error, invalid read to log!")
    print("=== Printing Log file ===")
    with open(Log.PrintLocal.name) as f:
      for line in f:
        print(line, end ="")

  @staticmethod
  def jsonError(msg):
    """
    In case of an irrecoverable error, create a JSON format response with error message and quit.

    `msg`: Message to send to the frontend.

    `return`: no return.
    """
    print("{error: true, msg: \"" + msg + "\"}")
    sys.exit(1)

  @staticmethod
  def local(msg):
    """
    Adds a progress message to the local log.

    `msg`: Message to log.

    `return`: returns nothing.
    """
    if (Log.PrintLocal != None):
      try:
        with open(Log.PrintLocal.name, 'a') as f:
          f.write(str(datetime.datetime.now())+" (*) " + str(msg) + "\n")
      except Exception as ex:
        Log.jsonError("Unexpected logging error occurred!")

  @staticmethod
  def localException(msg):
    """
    Adds an error message to the local log.

    `msg`: Message to log.

    `return`: returns nothing.
    """
    if (Log.PrintLocal != None):
      try:
        with open(Log.PrintLocal.name, 'a') as f:
          f.write(str(datetime.datetime.now())+" (E) " + str(msg) + "\n")
      except Exception as ex:
        Log.jsonError("Unexpected logging error occurred!")
