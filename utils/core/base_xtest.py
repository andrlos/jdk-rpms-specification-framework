import abc

import utils.test_utils as tu

import config.general_parser
import config.global_config
import config.runtime_config
from utils.core.base_test_runner import BaseTestRunner


def defaultMain(argv, runDocs, runTests):
    args = config.general_parser.GeneralParser().parser.parse_args(argv)
    canContinue = config.runtime_config.RuntimeConfig().setFromParser(args)
    if canContinue:
        if config.runtime_config.RuntimeConfig().getDocs():
            passed, ignored, failed = runDocs()
            tu.closeDocSuite(passed, ignored, failed)
        else:
            passed, failed, perMethod = runTests()
            tu.closeTestSuite(passed, failed, perMethod)


class BaseTest(BaseTestRunner):

    def getBuild(self):
        return config.runtime_config.RuntimeConfig().getRpmList().getBuildWithoutSrpm(self.current_arch)

    def getCurrentArch(self):
        return self.current_arch

    @abc.abstractmethod
    def setCSCH(self):
        """Set csch as overwriteing test wishes"""
        self.log("Nothing to set.")

    @abc.abstractmethod
    def getTestedArchs(self):
        """returns array of architectures to run tests/docs on
        Usually native arches as most of the tests are run on
        getBuildWithoutSrpm or getCompleteBuild
        overwrite and return empty array or None if the test is arch-independent"""
        self.log("run on all known arches")
        return config.runtime_config.RuntimeConfig().getRpmList().getNativeArches()