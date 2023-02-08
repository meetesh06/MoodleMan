### Package for assignment submissions from moodle.

This package provides a set of APIs to make evaluation of moodle assignment submissions easier.
The idea is to create a reusable set of classes to replace hard to read/debug bash scripts we are currently using.
Most assignments follow a simple structure:

1. validate and extract submission.zip file / return if error
2. compile (if needed) / return if error
3. \[compiledProgram\] < testcase1.in > out1
...
4. compare out1 to testcase1.out
...
5. return number of passed testcases

The [SubmissionHandler](./doc/moodle/handlers.html) Class is extended for different languages like Java, Cpp, etc. to make this task easier.

See documentation: [docs/moodle](./doc/moodle/index.html).


## Example projects
### Java
For a given moodle assignment where students are required to submit Java projects with Main.java as entry file.
See [examples/Java](./examples/Java).

```python
from moodle import MoodleSubmission
from moodle import JavaHandler
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
```

Running this example

```bash
git clone git@github.com:meetesh06/MoodleManagerPy.git
cd MoodleManagerPy/examples/Java
PYTHONPATH="${PYTHONPATH}:../../" python Assignment1.py sub1.zip
```

```
{"totalTests": 1, "test0": [true, "Able was I saw Elba\n", "Able was I saw Elba"], "marks": 1}
```

```bash
PYTHONPATH="${PYTHONPATH}:../../" python Assignment1.py sub2.zip
```

```
{"totalTests": 1, "test0": [false, "Able was I sae Elba\n", "Able was I saw Elba"], "marks": 0}
```

```bash
PYTHONPATH="${PYTHONPATH}:../../" python Assignment1.py bad.zip
```

```
{error: true, msg: "Failed to open zip file!"}
```

```bash
PYTHONPATH="${PYTHONPATH}:../../" python Assignment1.py random.zip
```

```
{error: true, msg: "Failed to open zip file!"}
```

> It would be a good idea to replace **../../** with absolute path or install the package via pip.

### Cpp
For a given moodle assignment where students are required to submit Cpp projects with main.cpp as entry file.
See [examples/Cpp](./examples/Cpp).
