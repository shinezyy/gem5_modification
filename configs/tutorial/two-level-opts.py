import m5
from m5.objects import *
from cache import *
from optparse import OptionParser
from cache import *

parser = OptionParser()
parser.add_option('--l1i_size', help="L1 instruction cache size")
parser.add_option('--l1d_size', help="L1 data cache size")
parser.add_option('--l2_size', help="Unified L2 cache size")

(options, args) = parser.parse_args()

system = System() # providing functinal informatin

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = TimingSimpleCPU()

# print options
system.cpu.icache = l1icache(options)
system.cpu.dcache = l1dcache(options)
system.l2cache = l2cache(options)

# system.cpu.icache = l1icache()
# system.cpu.dcache = l1dcache()

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)
#l1 cache cannot be connected to l2 directly, because l2 expectes only 1 post
#so l2 bus is needed
system.l2bus = CoherentXBar() 
system.l2bus.forward_latency = 0
system.l2bus.frontend_latency = 0
system.l2bus.response_latency = 0
system.l2bus.snoop_response_latency = 0
system.l2bus.width = 16

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus) # connect l2bus with l1 cache

# system.l2cache = l2cache()
system.l2cache.connectCPUSideBus(system.l2bus)

system.membus = CoherentXBar() # system-wide memory bus
system.l2cache.connectMemSideBus(system.membus)

# set the bus's latency, with is not mentioned in the tutorial
system.membus.forward_latency = 0
system.membus.frontend_latency = 0
system.membus.response_latency = 0
system.membus.snoop_response_latency = 0 
system.membus.width = 16

# system.cpu.icache_port = system.membus.slave # connect cache ports directly to the membus
# system.cpu.dcache_port = system.membus.slave

# in gem5 requests ate sent from a master port to a slave port, and
# in the reverse direction when response

# obj1.master = obj2.slave  <==> obj2.slave = obj1.master
# But the direction of data stream between cache and the membus should be double direction ?


system.cpu.createInterruptController()
system.cpu.interrupts.pio = system.membus.master
system.cpu.interrupts.int_master = system.membus.slave
system.cpu.interrupts.int_slave = system.membus.master

system.system_port = system.membus.slave # x86 specific, allow system to r/w memory

system.mem_ctrl = DDR3_1600_x64() # memory controller
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

process = LiveProcess()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print 'Beginning simulation!'
exit_event = m5.simulate()

print 'Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause())

