from src.settings import build_root as module


class TestBuildRoot:
    """src.settings.build_root.BuildRoot."""

    test_cls = module.BuildRoot

    def test_path(self):
        test_obj = self.test_cls()


class TestPyHuntersConfig:
    """src.settings.build_root.PyHuntersConfig."""

    test_cls = module.PyHuntersConfig

    def test_path(self):
        test_obj = self.test_cls.initialize()
        breakpoint()
