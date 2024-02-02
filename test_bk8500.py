from bk8500 import bk8500

bk8500 = bk8500(com_port='COM38',debug=True)
bk8500.enable_remote()
bk8500.enable_cc_mode()
bk8500.set_cc_mode_current(current=0.15)
bk8500.enable_input()
bk8500.disable_input()
