import os
from pathlib import Path
from .log import Log

# This module contains the handlers for handling different type of projects.
# The module currently contains an implementation for
# 1) Java: JavaHandler


class GeneralHandler:
  """
  `GeneralHandler` is an abstract class the provides basic functionality.
  `validate`, `compile` and `eval` methods bust be defined by the subclasses.
  """
  def __init__(self, workPath):
    """
    [Note: should only be called by the constructor of a subclass]
    
    `workPath`: The location of the project to process.

    `return`: returns nothing.
    """
    self.workPath = workPath
    self.paths = []
    self.validated = False
    self.mainFilePath = ""
    self.compiled = False

  def getWorkPath(self, path):
    """
    Equivalent of `dirname` in bash.

    eg: `getWorkPath`("/a/b/c/d.java) returns "/a/b/c"
    
    `path`: The path to the entry point of the project.

    `return`: Returns the dirname.
    """
    return str(path.parents[0])
  
  def getCompilationLogPath(self, path):
    """
    Returns path to a `outCompilation` file that will exist in the same location as the `GeneralHandler.getWorkPath`.

    `path`: The path to the entry point of the project.

    `return`: Returns the dirname + "/outCompilation"
    """
    return self.getWorkPath(path) + "/outCompilation"

  def getEvalLogPath(self, path):
    """
    returns path to a `outEval` file that will exist in the same location as the `GeneralHandler.getWorkPath`.

    `path`: The path to the entry point of the project.
    
    `return`: Returns the dirname + "/outEval"
    """
    return self.getWorkPath(path) + "/outEval"

  def pushPathContext(self, path):
    """
    Pushes the existing working directory onto a stack and navigates to a given directory.

    `path`: Path to goto.
    
    `return`: returns nothing.
    """
    self.paths.append(os.getcwd())
    os.chdir(path)
  
  def popPathContext(self):
    """
    Pops one element from the stack and navigates to it.
    
    `return`: returns nothing.
    """
    os.chdir(self.paths.pop())

  def genericValidator(self, searchType, entryFile):
    """
    Searches for a given `entryFile` recursively in the project directory and returns its path if found.
    
    `searchType`: Regex for file type, eg: "\*.java", "\*.[tT][xX][tT]", etc...

    `entryFile`: Name of the entryFile to search for "Main.java" (note that this is expected to be unique in this validator).
    
    `return`: Tuple(status: bool, entryFilePath: string). If status is false 'entryFilePath' contains the error message.
    """
    result = list(Path(self.workPath).rglob(searchType))
    if (len(result) > 0):
      foundRes = False
      res = ""
      for currFile in result:
        if (currFile.parts[-1] == entryFile):
          if (foundRes == False):
            res = currFile
            foundRes = True
          else:
            return False, "Validator Failed [multiple entry points found, expected one "+entryFile+" file]"
      if (foundRes):
        return True, res
      else:
        return False, "Validator Failed [no entry point found, expected file "+entryFile+" was not found]"
    else:
      return False, "Validator Failed [no " + searchType + " files found]"

  def genericCompiler(self, mainFilePath, compilationCommand):
    """
    Navigates to the directory where the `mainFilePath` exists and executes the `compilationCommand`.
    
    `mainFilePath`: Path to the entryFile, eg: "a/b/c/Main.java"
    
    `compilationCommand`: Command to execute in the directory to compile, eg: "javac Main.java"
    
    `return`: (returnStatus: int) returns the exit status of the compilation process.
    """
    self.pushPathContext(self.getWorkPath(mainFilePath))
    cmd = compilationCommand + " >"+self.getCompilationLogPath(mainFilePath)+" 2>&1"
    res = os.system(cmd)
    self.popPathContext()
    return res

  def genericEval(self, mainFilePath, runCommand, inputFile):
    """
    Navigates to the directory where the `mainFilePath` exists and executes the `runCommand` passing `inputFile` as STDIN to the program.
    
    `mainFilePath`: Path to the entryFile, eg: "a/b/c/Main.java"
    
    `runCommand`: Command to execute in the directory. It gets executed as [runCommand] < [inputFile].
    
    `inputFile`: Path to the inputfile to be passed as STDIN
    
    `return`: Returns the obtained result as string
    """
    self.pushPathContext(self.getWorkPath(mainFilePath))
    cmd = runCommand + " < " + inputFile + " > " + self.getEvalLogPath(mainFilePath) + " 2>&1"
    os.system(cmd)
    obtainedRes = open(self.getEvalLogPath(mainFilePath), "r").read()
    return obtainedRes

class JavaHandler(GeneralHandler):
  """
  `JavaHandler` extends `GeneralHandler` to support java submissions.
  It expects that there will be a unique entry point (default="Main.java") somewhere in the project.
  The handler recursively searches the project for a this unique entry point.
  It goes to the directory where the entry point exists and compiles it using javac. 
  """
  def __init__(self, workPath, entryFilename="Main.java", compileCommand="javac Main.java", evalCommand="java Main"):
    """
    `workPath`: The location of the project to process.
    
    `entryFilename`: (default="Main.java") Name of the entry file of the project.
    
    `compileCommand`: (default="javac Main.java") Compilation command.
    
    `evalCommand`: (default="java Main") Eval command.
    
    `return`: returns nothing.
    """
    super().__init__(workPath)
    self.entryFilename = entryFilename
    self.compileCommand = compileCommand
    self.evalCommand = evalCommand
    
  # Ensures that the extracted folder contains the Main.java (the entry file)
  def validate(self):
    """
    Validates that the project contains a unique entry point (`self.entryFilename`). 
    
    `return`: Tuple(status: bool, entryFilePath: string). If status is false 'entryFilePath' contains the error message.
    """
    res = GeneralHandler.genericValidator(self, "*.java", self.entryFilename)
    self.validated = res[0]
    self.mainFilePath = res[1]
    return res
  
  # Compiles the given file
  def compile(self):
    """
    Compiles the project using `javac`.
    
    `return`: (returnStatus: int) returns the exit status of the compilation process.
    """
    if (self.validated == False):
      Log.jsonError("Tried to compile an invalidated submission.")
    res = GeneralHandler.genericCompiler(self, self.mainFilePath, self.compileCommand)
    self.compiled = (res == 0)
    return res

  # Evaluate
  def eval(self, inputFile):
    """
    Evaluates the program by passing the input file as `STDIN` to the compiled program.
    
    `inputFile`: path the input file
    
    `return`: Returns the obtained result as string
    """
    if (self.compiled == False):
      Log.jsonError("Cannot eval without successful compilation!")
    return GeneralHandler.genericEval(self, self.mainFilePath, self.evalCommand, inputFile)
