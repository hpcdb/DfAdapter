import redis
class DataSet_2_Adapter_Example(object):
    def __init__(self):
        self.redis_client = redis.from_url('redis://localhost:6379')

    def has_adaptation(self):
        return self.redis_client.get("adapted") == "t"
    



if __name__ == '__main__':
    ds2Adpt = DataSet_2_Adapter_Example()

    print ds2Adpt.has_adaptation()
