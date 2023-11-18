import os
import sys
import unittest

# Add project root to PYTHONPATH so MLU modules can be imported
scriptPath = os.path.dirname(os.path.realpath(__file__))
projectRoot = os.path.abspath(os.path.join(scriptPath ,".."))
sys.path.insert(0, projectRoot)

from com.nwrobel import mypycommons
import com.nwrobel.mypycommons.time

import common

class Time_ModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        #super(File_ModuleTest, self).setUpClass
        self.helper = common.TestHelper()

    def test_getTimedeltaFromFormattedDuration(self):
        timeD = mypycommons.time.getTimedeltaFromFormattedDuration('0:03:01')
        self.assertEqual(timeD.total_seconds(), 181)

if __name__ == '__main__':
    unittest.main()
