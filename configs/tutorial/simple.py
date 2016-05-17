import m5
from m5.objects import *

system = System() # providing functinal informatin

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = TimingSimpleCPU()

system.membus = CoherentXBar() # system-wide memory bus

system.membus.forward_latency = 1 # set the bus's latency, with is not mentioned in the tutorial
system.membus.frontend_latency = 1 
system.membus.response_latency = 1 
system.membus.snoop_response_latency = 1 
system.membus.width = 16

system.cpu.icache_port = system.membus.slave # connect cache ports directly to the membus
system.cpu.dcache_port = system.membus.slave

# in gem5 requests ate sent from a master port to a slave port, and
# in the reverse direction when response

# obj1.master = obj2.slave  <==> obj2.slave = obj1.master
# But the direction of data stream between cache and the membus should be double direction ?


system.cpu.createInterruptController()
print type(system.cpu.interrupts.pio)
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

