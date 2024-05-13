while 1:
    idaapi.continue_process()
    idaapi.wait_for_next_event(WFNE_SUSP, -1)
    name_func = get_func_name(get_reg_value('rip'))
    if get_reg_value('rip') == 0x0007FF7C2781B79: break
    if name_func in "xor_instr":
        print(name_func,hex(get_wide_word(get_reg_value('r9')-3)),hex(get_wide_word(get_reg_value('r9')-1)))
    if name_func in "cmp_inst":
        print(name_func,hex(get_wide_word(get_reg_value('r10')-1)))