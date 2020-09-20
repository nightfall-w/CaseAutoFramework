import configparser
import os

"""
读取配置文件信息
"""


class ConfigParser():
    config_dic = {}

    @classmethod
    def get_config(cls, sector, item):
        value = None
        try:
            value = cls.config_dic[sector][item]
        except KeyError:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.conf')
            cf = configparser.ConfigParser()
            cf.read(config_path, encoding='utf8')
            value = cf.get(sector, item)
            cls.config_dic[sector][item] = value
        finally:
            return value
