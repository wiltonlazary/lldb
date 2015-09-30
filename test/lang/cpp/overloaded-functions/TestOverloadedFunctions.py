"""
Tests that functions with the same name are resolved correctly.
"""

import lldb
from lldbtest import *
import lldbutil

class CPPStaticMethodsTestCase(TestBase):
    
    mydir = TestBase.compute_mydir(__file__)
    
    def setUp(self):
        TestBase.setUp(self)
        self.line = line_number('main.cpp', '// breakpoint')

    @expectedFailureWindows("llvm.org/pr24489: Name lookup not working correctly on Windows")
    def test_with_run_command(self):
        """Test that functions with the same name are resolved correctly"""
        self.build()
        self.runCmd("file a.out", CURRENT_EXECUTABLE_SET)

        lldbutil.run_break_set_by_file_and_line (self, "main.cpp", self.line, num_expected_locations=1, loc_exact=True)

        self.runCmd("process launch", RUN_SUCCEEDED)

        # The stop reason of the thread should be breakpoint.
        self.expect("thread list",
                    STOPPED_DUE_TO_BREAKPOINT,
                    substrs = ['stopped', 'stop reason = breakpoint'])

        self.expect("expression -- Dump(myB)",
                    startstr = "(int) $0 = 2")

        self.expect("expression -- Static()",
                    startstr = "(int) $1 = 1")

if __name__ == '__main__':
    import atexit
    lldb.SBDebugger.Initialize()
    atexit.register(lambda: lldb.SBDebugger.Terminate())
    unittest2.main()
