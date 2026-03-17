import os
import tempfile
from octopai.core.converter import URLConverter


def test_converter_initialization():
    """测试转换器初始化"""
    converter = URLConverter()
    assert converter is not None


def test_convert_url():
    """测试URL转换"""
    # 注意：这个测试需要真实的API密钥才能运行
    # 这里只测试基本功能，不实际调用API
    converter = URLConverter()
    assert hasattr(converter, 'convert')
