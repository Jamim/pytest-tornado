import pytest
import sys
from tornado import gen

_used_fixture = False


@gen.coroutine
def dummy(io_loop):
    yield gen.Task(io_loop.add_callback)
    raise gen.Return(True)


@pytest.fixture(scope='module')
def preparations():
    global _used_fixture
    _used_fixture = True


pytestmark = pytest.mark.usefixtures('preparations')


@pytest.mark.xfail(pytest.__version__ < '2.7.0',
                   reason='py.test 2.7 adds hookwrapper, fixes collection')
@pytest.mark.gen_test
def test_uses_pytestmark_fixtures(io_loop):
    assert (yield dummy(io_loop))
    assert _used_fixture

class TestClass:
    def beforeEach(self):
        global _used_fixture
        _used_fixture = False

    @pytest.mark.gen_test
    def test_uses_pytestmark_fixtures(self, io_loop):
        assert (yield dummy(io_loop))
        assert _used_fixture

    if sys.version_info >= (3, 5):
        from tornado.ioloop import IOLoop

        @pytest.mark.gen_test
        def test_type_attrib(self, io_loop: IOLoop):
            assert (yield dummy(io_loop))
            assert _used_fixture
