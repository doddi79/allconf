__all__ = [
    'IStubMaker',
]
from allconf.structs import *


class IStubMaker(abc.ABC):
    @abc.abstractmethod
    def render_stub_classes_from_descriptor_file(self, file: str, is_private: bool = True,
                                                 class_name: str = 'AllConfConfigStub') -> str:
        """Renders a Python module file with type hinting stub classes from the
        AllConf config type descriptor file.
        """
        pass

    @abc.abstractmethod
    def render_stub_classes_to_file(self, input_file: str, output_file: str,
                                    overwrite_existing: bool = False, is_private: bool = True,
                                    class_name: str = 'AllConfConfigStub'):
        """Writer the results of the `render_stub_classes_from_descriptor_file`
        call to the given output file.
        """
        pass
