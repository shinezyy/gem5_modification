# Mybench.py

binary_dir  = '/ext_home/program_files/spec/benchspec/CPU2006/401.bzip2/exe/'
data_dir    = '/ext_home/program_files/spec/benchspec/CPU2006/'

'''
#400.perlbench
perlbench = LiveProcess()
perlbench.executable =  binary_dir+'400.perlbench_base.alpha-gcc'
perlbench.cmd = [perlbench.executable] + ['-I./lib', 'attrs.pl']
perlbench.output = 'attrs.out'
'''

#401.bzip2
bzip2 = LiveProcess()
bzip2.executable =  binary_dir+'401.bzip2_base.alpha-gcc'
data=data_dir+'401.bzip2/data/all/input/input.program'
bzip2.cmd = [bzip2.executable] + [data, '1']
bzip2.output = 'input.program.out'

'''
#403.gcc
gcc = LiveProcess()
gcc.executable =  binary_dir+'403.gcc_base.alpha-gcc'
data=data_dir+'403.gcc/data/test/input/cccp.i'
output='/import/home1/mjwu/work_spec2006/403.gcc/m5/cccp.s'
gcc.cmd = [gcc.executable] + [data]+['-o',output]
gcc.output = 'ccc.out'
'''
