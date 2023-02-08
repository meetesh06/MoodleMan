from moodle import MoodleSubmission
from moodle import JavaHandler, GeneralHandler

class Hello(GeneralHandler):
  def joke(self):
    print("It runs in your jeans.")

p1 = MoodleSubmission("./moodleZip/sub3.zip", JavaHandler)

r = p1.evalMatch("/home/meetesh06/fileMan/test1", "/home/meetesh06/fileMan/test1.out")

if (r):
  print("Test1 pass")
else:
  print("Test1 fail")
