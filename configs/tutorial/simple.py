import m5
from m5.objects import *

system = System() # providing functinal informatin

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = TimingSimpleCPU()

system.membus = coherentXBar() # system-wide memory bus

system.cpu.icache_port = system.membus.slave # connect cache ports directly to the membus
system.cpu.dcache_port = system.membus.slave


