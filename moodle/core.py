from zipfile import ZipFile
import tempfile
from .log import Log
import shutil
from .handlers import GeneralHandler
"""
This module contains the classes that are used to interact with moodle submissions directly.
"""

# ref: https://stackoverflow.com/questions/16474848/python-how-to-compare-strings-and-ignore-white-space-and-special-characters
def compareStringsIgnoreWhiteSpace(a, b):
  """
  Compares strings by ignoring whitespace.
  :param a: First string.
  :param b: Second string.        
  :return: returns bool.
  """
  return [c for c in a if c.isalpha()] == [c for c in b if c.isalpha()]

def ensureCallable(obj, method):
  """
  Ensures a method exists and can be called given an object, otherwise throws an error and exits.
  :param obj: Object to check.
  :param method: Name of the method.        
  :return: returns nothing.
  """
  canCall = hasattr(obj, method) and callable(getattr(obj, method))
  if (canCall == False):
    raise Exception("ensureCallable failed for: " + method)

class MoodleSubmission:
  """
  MoodleSubmission takes an individual moodle submission zip and contains methods to 
  validate, compile and eval it.
  The class also takes care of allocation and cleanup of temporary directories/files. 
  """
  def __init__(self, path, subHandler):
    """
        Construct a new 'MoodleSubmission' object and does the following.
        1. Ensures that the provided submission is a valid zip file.
        2. If the zip is valid, extracts the submission to a temporary directory.
        3. Creates a submission handler object and passes the extracted file path to it.
        4. Calls the submission handler methods to initialize the submission.

        :param path: Path to the submission.zip file (recommended absolute paths)
        :param subHandler: A submission handler class that extends GeneralHandler (JavaHandler, CppHandler, etc. See handlers.py)        
        :return: returns nothing
    """

    try:
      if (issubclass(subHandler, GeneralHandler) == False):
        Log.localException("[ERROR] Submission handler must extend GeneralHandler!")
        Log.jsonError("Error code 101 (broken submission handler)")
    except Exception as ex:
      Log.localException(ex)
      Log.jsonError("Error code 102 (broken submission handler)")

    try:
      self.zip = ZipFile(path)
      self.zip.testzip()
      Log.local("Zip file is valid!")
      self.dir = tempfile.mkdtemp()
      self.zip.extractall(self.dir)
      Log.local("Extraction to temporary directory successful!")
      self.handle = subHandler(self.dir)
    except Exception as ex:
      Log.localException(ex)
      Log.jsonError("Failed to open zip")
    
    self.callHandlerMethods()

  

  def callHandlerMethods(self):
    """
    Calls the validate and compile method from the supplied submission handler.
    :return: returns nothing
    """
    try:
      # Ensure the methods exist and can be called
      ensureCallable(self.handle, "validate")
      ensureCallable(self.handle, "compile")
      Log.local("'validate' and 'compile' are callable.")

      # Call validate
      res = self.handle.validate()
      Log.local("validate returned: " + str(res[0]) + ", " + str(res[1]))
      if (res[0] == False):
        Log.jsonError(res[1])

      # Call compile
      res = self.handle.compile()
      Log.local("compile returned: " + str(res))
      if (res != 0):
        Log.jsonError("Compilation failed [exit status " + str(res) + "]")
    except Exception as ex:
      Log.localException(ex)
      Log.jsonError("Submission handler failed, ensure the methods exist")
    
  def eval(self, input):
    """
    Calls the eval method from the supplied handler.
    :param input: Path to input file to be evaluated.
    :return: returns the result obtained as string.
    """
    return self.handle.eval(input)



  def evalMatch(self, input, output, comparator=compareStringsIgnoreWhiteSpace):
    """
    Calls the eval method from the supplied handler and compares the obtained result against the expected result.
    :param input: Path to input file to be evaluated.
    :param output: Path to expected output file.
    :param comparator: (default=compareStringsIgnoreWhiteSpace) the comparator used to match the obtained results. 
    :return: returns bool.
    """
    obtainedRes = self.handle.eval(input)
    expectedRes = open(output, "r").read()
    if (comparator(obtainedRes, expectedRes)):
      return True
    else:
      return False

  def __del__(self):
    try:
      shutil.rmtree(self.dir)
    except Exception as ex:
      return