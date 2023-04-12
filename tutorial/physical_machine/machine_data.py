import pprint
import random


class Host:
    def __init__(self, ip, core, memory, disk):
        self.ip = ip
        self.core = core
        self.memory = memory
        self.disk = disk

    def __str__(self):
        return vars(self).__str__()

    def __repr__(self):
        return self.__str__()


def get_host_info(search_ip=None):
    data = []
    for i in range(5):
        ip = f"192.168.10.{i + 1}"
        core = random.randint(100, 200)
        memory = f"{random.randint(500, 2048)}G"
        disk = f"{random.randint(1024, 4096)}G"
        if search_ip:
            if ip == search_ip:
                data.append(Host(ip, core, memory, disk))
        else:
            data.append(Host(ip, core, memory, disk))
    return data


if __name__ == '__main__':
    pprint.pprint(get_host_info())  # 测试获取所有机器
    pprint.pprint(get_host_info("192.168.10.3"))  # 测试获取某个机器
    pprint.pprint(get_host_info("192.168.10.9"))  # 测试获取某个不存在机器
