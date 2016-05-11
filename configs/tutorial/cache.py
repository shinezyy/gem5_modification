from m5.objects import BaseCache

class l1cache(BaseCache):
    assoc = 2
    hit_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    is_top_level = True

    def connectCPU(self, cpu):
        # interface
        raise NotImplementedError

    def connectBus(self, bus):
        self.mem_side = bus.slave

class l1icache(l1cache):
    size = '16kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class l1dcache(l1cache):
    size = '64kB'

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

class l2cache(BaseCache):
    size = '256kB'
    assoc = 8
    hit_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave
