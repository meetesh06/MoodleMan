from moodle import MoodleSubmission
from moodle import JavaHandler
from moodle import Log
import json

import sys
import os
n = len(sys.argv)
assert(n == 2)

p1 = MoodleSubmission(sys.argv[1], JavaHandler)

marks = 0
result = {}
numTests = 1
result["totalTests"] = numTests
for i in range(numTests):
  testcase1Input=os.getcwd() + "/testcases/test"+str(i)+".in"
  testcase1Output=os.getcwd() + "/testcases/test"+str(i)+".out"
  r = p1.evalMatch(testcase1Input, testcase1Output)
  testCaseId = "test" + str(i)
  result[testCaseId] = r
  if (r):
    marks = marks + 1
  else:
    marks = marks + 0

result["marks"] = marks
finalRes = json.dumps(result)

print(finalRes)