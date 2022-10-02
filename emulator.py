class emulator():
    def __init__(self):
        self.flag = {'C': 0, 'ZF': 0}
        # Reset mem
        self.pc = 0
        self.regc = 0
        self.dcc = 0
        self.sp = -1
        # Reset mem
        self.mem = ['00000000'] * 64
        self.stack = ['00000000'] * 64
        self.ram = ['0000000000000000'] * 64
        self.counter = '00000000'
        # All commands
        self.com_list = {'00000000': (self.inc_pc, False),
                         '11111111': (self.end, False),
                         '00000001': (self.push, True),
                         '00000010': (self.dup, False),
                         '00000011': (self.read, False),
                         '00000100': (self.write, False),
                         '00000101': (self.drop, False),
                         '00000110': (self.ldc, False),
                         '00000111': (self.stc, False),
                         '00001000': (self.swap, False),
                         '00001001': (self.ror, False),
                         '00001010': (self.rol, False),
                         '00001011': (self.add, False),
                         '00001100': (self.addc, False),
                         '00001101': (self.sub, False),
                         '00001110': (self.mul, False),
                         '00001111': (self.inc, False),
                         '00010000': (self.dec, False),
                         '00010001': (self.incc, False),
                         '00010010': (self.dcc, False),
                         '00010011': (self.cmp, False),
                         '00010100': (self.cmpc, False),
                         '00010101': (self.jc, False),
                         '00010110': (self.jnc, False),
                         '00010111': (self.jmp, False),
                         '00011000': (self.djz, False),
                         '00011001': (self.djnz, False)
                         }

    def start_emul(self):
        self.flag = {'C': 0, 'ZF': 0}
        # Reset mem
        self.pc = 0
        self.regc = 0
        self.dcc = 0
        self.sp = -1
        # Reset mem
        self.mem = ['00000000'] * 64
        self.stack = ['00000000'] * 64
        self.ram = ['0000000000000000'] * 64
        self.counter = '00000000'

    def set_ram(self, compiled_ram):
        cnt = 0
        for coms in compiled_ram:
            self.ram[cnt] = coms
            cnt += 1
        print("COMPILED RAM:", compiled_ram)

    def get_ram(self, addr):
        return self.ram[addr]

    def set_flag(self, flag, val):
        self.flag[flag] = val

    def get_flag(self, flag):
        return self.flag[flag]

    def write_to_mem(self, addr, val):
        self.mem[int(addr, 2)] = val

    def get_from_mem(self, addr):
        return self.mem[int(addr, 2)]

    def end(self):
        pass

    def new_execute(self):
        if self.com_list[self.ram[self.pc][:8]][1] is not True:
            self.com_list[self.ram[self.pc][:8]][0]()
        else:
            self.com_list[self.ram[self.pc][:8]][0](self.ram[self.pc][8:])

    def inc_pc(self):
        self.pc += 1
        pass

    def dup(self):
        self.stack[self.sp + 1] = self.stack[self.sp]
        self.sp += 1
        self.pc += 1
        pass

    def read(self):
        self.stack[self.sp] = self.get_from_mem(self.stack[self.sp])
        self.pc += 1
        pass

    def write(self):
        self.write_to_mem(self.stack[self.sp], self.stack[self.sp - 1])
        self.stack[self.sp] = '00000000'
        self.stack[self.sp - 1] = '00000000'
        self.sp -= 2
        self.pc += 1
        pass

    def drop(self):
        self.stack[self.sp] = '00000000'
        self.sp -= 1
        self.pc += 1
        pass

    def ldc(self):
        self.counter = str(self.stack[self.sp])
        self.stack[self.sp] = '00000000'
        self.sp -= 1
        self.pc += 1
        pass

    def stc(self):
        self.sp += 1
        self.stack[self.sp] = str(str(self.counter))
        self.counter = '00000000'
        self.pc +=1

    def swap(self):
        buff = self.stack[self.sp]
        self.stack[self.sp] = self.stack[self.sp - 1]
        self.stack[self.sp - 1] = buff
        self.pc += 1
        pass

    def ror(self):
        pass

    def rol(self):
        pass

    def add(self):
        sum = bin(int(self.stack[self.sp], 2) + int(self.stack[self.sp - 1], 2))[2:].zfill(8)
        if len(sum) > 8:
            self.flag['C'] = 1
            sum = sum[1:]
        else:
            self.flag['C'] = 0
        self.stack[self.sp] = '00000000'
        self.sp -= 1
        self.pc += 1
        self.stack[self.sp] = sum
        pass

    def addc(self):
        sum = bin(int(self.stack[self.sp], 2) + int(self.stack[self.sp - 1], 2) + self.get_flag('C'))[2:].zfill(8)
        if len(sum) > 8:
            self.flag['C'] = 1
        else:
            self.flag['C'] = 0
        self.stack[self.sp] = '00000000'
        self.sp -= 1
        self.pc += 1
        self.stack[self.sp] = sum
        pass

    def sub(self):
        sub = bin(int(self.stack[self.sp], 2) - int(self.stack[self.sp - 1], 2))[2:].zfill(8)
        if len(sub) > 8:
            self.flag['C'] = 1
            sub = sub[1:]
        else:
            self.flag['C'] = 0
        if sub == '00000000':
            self.set_flag('ZF', 1)
        else:
            self.set_flag('ZF', 0)
        self.stack[self.sp] = '00000000'
        self.sp -= 1
        self.pc += 1
        self.stack[self.sp] = sub
        pass

    def mul(self):
        mul = bin(int(self.stack[self.sp], 2) * int(self.stack[self.sp - 1], 2))[2:].zfill(16)
        if len(mul) > 16:
            self.flag['C'] = 1
        self.stack[self.sp] = mul[8:]
        self.stack[self.sp - 1] = mul[:8]
        self.pc += 1

    def inc(self):
        inc = bin(int(self.stack[self.sp], 2) + 1)[2:].zfill(8)
        if len(inc) > 8:
            self.flag['C'] = 1
        self.stack[self.sp] = inc
        self.pc += 1
        pass

    def dec(self):
        dec = bin(int(self.stack[self.sp], 2) - 1)[2:].zfill(8)
        if len(dec) > 8:
            self.flag['C'] = 1
        self.stack[self.sp] = dec
        self.pc += 1
        pass

    def incc(self):
        self.counter = bin(int(self.counter, 2) + 1)[2:].zfill(8)
        self.pc += 1
        pass

    def decc(self):
        self.counter = bin(int(self.counter, 2) - 1)[2:].zfill(8)
        self.pc += 1
        pass

    def cmp(self):
        if int(self.stack[self.sp], 2) > int(self.stack[self.sp - 1], 2):
            self.set_flag('C', 1)
        else:
            self.set_flag('C', 0)
        self.pc += 1
        pass

    def cmpc(self):
        pass

    def jc(self):
        if self.get_flag('C') == 1:
            self.pc = int(self.stack[self.sp], 2)
        else:
            self.pc += 1
        self.stack[self.sp] = '00000000'
        self.sp -= 1
        pass

    def jnc(self):
        if self.get_flag('C') == 0:
            self.pc = int(self.stack[self.sp], 2)
        else:
            self.pc += 1
        self.stack[self.sp] = '00000000'
        self.sp -= 1
        pass

    def jmp(self):
        self.pc = int(self.stack[self.sp], 2)
        self.stack[self.sp] = '00000000'
        self.sp -= 1

    def djz(self):
        self.counter = bin(int(self.counter, 2) - 1)[2:].zfill(8)
        if self.counter == '00000000':
            self.set_flag('ZF', 1)
        else:
            self.set_flag('ZF', 0)
        if self.get_flag('ZF') == 1:
            self.pc = int(self.stack[self.sp], 2)
        else:
            self.pc += 1
        self.stack[self.sp] = '00000000'
        self.sp -= 1

    def djnz(self):
        self.counter = bin(int(self.counter, 2) - 1)[2:].zfill(8)
        if self.counter == '00000000':
            self.set_flag('ZF', 1)
        else:
            self.set_flag('ZF', 0)

        if self.get_flag('ZF') != 1:
            self.pc = int(self.stack[self.sp], 2)
        else:
            self.pc += 1
        self.stack[self.sp] = '00000000'
        self.sp -= 1

    def push(self, val):
        if self.sp == -1:
            self.sp = 0
        else:
            self.sp += 1
        self.stack[self.sp] = val
        self.pc += 1
        pass
