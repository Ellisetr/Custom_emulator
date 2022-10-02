import re
import tkinter as tk
import tkinter.ttk as ttk
import emulator
import compiler
import lang


class GUI:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=600, width=800)
        frame3 = ttk.Frame(toplevel1)
        frame3.configure(height=600, width=200)
        self.codeTxt = tk.Text(frame3)
        self.codeTxt.configure(height=28, width=50)
        self.codeTxt.grid(column=0, columnspan=3, row=1)
        self.cmpBtn = ttk.Button(frame3)
        self.cmpBtn.configure(text='Compile')
        self.cmpBtn.grid(column=0, row=0)
        self.cmpBtn.bind("<ButtonPress>", self.compile, add="")
        self.runBtn = ttk.Button(frame3)
        self.runBtn.configure(text='Run all')
        self.runBtn.grid(column=1, row=0)
        self.runBtn.bind("<ButtonPress>", self.full_run, add="")
        self.stepBtn = ttk.Button(frame3)
        self.stepBtn.configure(text='Run one step')
        self.stepBtn.grid(column=2, row=0)
        self.stepBtn.bind("<ButtonPress>", self.one_tick, add="")
        frame3.grid(column=1, row=0)
        frame5 = ttk.Frame(toplevel1)
        frame5.configure(height=600, width=200)
        frame7 = ttk.Frame(frame5)
        frame7.configure(height=200, width=200)
        self.COM_MEM_frame = ttk.Labelframe(frame7)
        self.COM_MEM_frame.configure(height=200, text='COM MEM', width=400)
        self.COM_MEM = ttk.Treeview(self.COM_MEM_frame)
        self.COM_MEM = ttk.Treeview(self.COM_MEM_frame, columns=('mem_adr', 'op_code'), show='headings')
        self.COM_MEM.heading('mem_adr', text="Memory address")
        self.COM_MEM.heading('op_code', text="Operation code")
        self.COM_MEM.pack()
        self.COM_MEM_frame.grid(column=0, row=0)
        self.DATA_MEM_frame = ttk.Labelframe(frame7)
        self.DATA_MEM_frame.configure(height=200, text='DATA MEM', width=200)
        self.DATA_MEM = ttk.Treeview(self.DATA_MEM_frame, columns=('mem_adr', 'data'), show='headings')
        self.DATA_MEM.heading('mem_adr', text="Memory address")
        self.DATA_MEM.heading('data', text="Data")
        self.DATA_MEM.configure(selectmode="extended")
        self.DATA_MEM.grid(column=0, columnspan=1, row=0)
        self.DATA_MEM_frame.grid(column=1, row=0)
        frame7.grid(column=0, columnspan=2, row=0)
        self.stack_frame = ttk.Labelframe(frame5)
        self.stack_frame.configure(height=200, text='STACK MEM', width=200)
        self.STACK_MEM = ttk.Treeview(self.stack_frame, columns=('mem_adr', 'data'), show='headings')
        self.STACK_MEM.pack(side="top")
        self.STACK_MEM.heading('mem_adr', text="Memory address")
        self.STACK_MEM.heading('data', text="Data")
        self.stack_frame.grid(column=1, row=1, sticky="e")
        frame1 = ttk.Frame(frame5)
        frame1.configure(height=200, width=200)
        self.PC_frame = ttk.Labelframe(frame1)
        self.PC_frame.configure(height=200, text='PC', width=200)
        self.PC_data = tk.Text(self.PC_frame)
        self.PC_data.configure(height=1, width=2)
        self.PC_data.grid(column=0, row=0)
        self.PC_frame.grid(column=0, row=0)
        self.REGC_frame = ttk.Labelframe(frame1)
        self.REGC_frame.configure(height=200, text='REGC', width=200)
        self.REGC = tk.Text(self.REGC_frame)
        self.REGC.configure(height=1, width=16)
        self.REGC.pack(side="top")
        self.REGC_frame.grid(column=1, row=0)
        self.DECC_frame = ttk.Labelframe(frame1)
        self.DECC_frame.configure(height=200, text='DECC', width=16)
        self.DECC = tk.Text(self.DECC_frame)
        self.DECC.configure(height=1, width=16)
        self.DECC.pack(side="top")
        self.DECC_frame.grid(column=1, row=1)
        self.SP_frame = ttk.Labelframe(frame1)
        self.SP_frame.configure(height=1, text='SP\n', width=200)
        self.SP_data = tk.Text(self.SP_frame)
        self.SP_data.configure(height=1, state="normal", width=2)
        self.SP_data.grid(column=0, row=0)
        self.SP_frame.grid(column=0, row=1)
        self.Flag_frame = ttk.Labelframe(frame1)
        self.Flag_frame.configure(height=200, text='Flags', width=200)
        self.C_label = ttk.Label(self.Flag_frame)
        self.C_label.configure(padding=5, text='C')
        self.C_label.grid(column=0, row=0)
        self.ZF_label = ttk.Label(self.Flag_frame)
        self.ZF_label.configure(text='ZF')
        self.ZF_label.grid(column=1, row=0)
        self.C = tk.Text(self.Flag_frame)
        self.C.configure(height=1, width=1)
        self.C.grid(column=0, row=1)
        self.ZF = tk.Text(self.Flag_frame)
        self.ZF.configure(height=1, width=1)
        self.ZF.grid(column=1, ipadx=0, row=1)
        self.Flag_frame.grid(column=1, columnspan=1, row=3)
        self.CNT_frame = ttk.Labelframe(frame1)
        self.CNT_frame.configure(height=200, text='CNT', width=200)
        self.CNT = tk.Text(self.CNT_frame)
        self.CNT.configure(height=1, width=2)
        self.CNT.pack(side="top")
        self.CNT_frame.grid(column=0, row=3, rowspan=1)
        frame1.grid(column=0, row=1)
        frame5.grid(column=0, row=0)
        frame5.grid_anchor("center")
        frame1.grid(column=0, row=1)
        frame5.grid(column=0, row=0)
        frame5.grid_anchor("center")

        # Main widget
        self.mainwindow = toplevel1

        # Emulator init
        self.emulator = emulator.emulator()

    def run(self):
        self.mainwindow.mainloop()

    def compile(self, event=None):
        self.emulator.start_emul()
        print(self.codeTxt.get(1.0, "end-1c"))
        self.emulator.set_ram(compiler.compile(self.codeTxt.get(1.0, "end-1c")))
        self.update_ui()
        pass

    def full_run(self, event=None):
        while self.decode_op(self.emulator.ram[self.emulator.pc]) != 'END':
            self.one_tick()
        self.update_ui()

    def one_tick(self, event=None):
        self.update_ui()
        self.emulator.new_execute()

    def update_ui(self):
        self.update_com_mem()
        self.update_stack_mem()
        self.update_mem()
        self.SP_data.delete(1.0, tk.END)
        if self.emulator.sp == -1:
            self.SP_data.insert(tk.END, 0)
        else:
            self.SP_data.insert(tk.END, self.emulator.sp)
        self.PC_data.delete(1.0, tk.END)
        self.PC_data.insert(tk.END, self.emulator.pc)
        self.REGC.delete(1.0, tk.END)
        self.REGC.insert(tk.END, self.emulator.ram[self.emulator.pc])
        self.DECC.delete(1.0, tk.END)
        self.DECC.insert(tk.END, self.decode_op(self.emulator.ram[self.emulator.pc]))
        self.CNT.delete(1.0, tk.END)
        self.CNT.insert(tk.END, int(self.emulator.counter,2))
        self.C.delete(1.0, tk.END)
        self.C.insert(tk.END, self.emulator.get_flag('C'))
        self.ZF.delete(1.0, tk.END)
        self.ZF.insert(tk.END, self.emulator.get_flag('ZF'))

    def update_com_mem(self):
        self.COM_MEM.delete(*self.COM_MEM.get_children())
        cnt = 0
        for ops in self.emulator.ram:
            self.COM_MEM.insert('', tk.END, values=[f'{cnt:x}', ops])
            cnt += 1

    def update_mem(self):
        self.DATA_MEM.delete(*self.DATA_MEM.get_children())
        cnt = 0
        for data in self.emulator.mem:
            self.DATA_MEM.insert('', tk.END, values=[f'{cnt:x}', data])
            cnt += 1

    def update_stack_mem(self):
        self.STACK_MEM.delete(*self.STACK_MEM.get_children())
        cnt = 0
        for data in self.emulator.stack:
            self.STACK_MEM.insert('', tk.END, values=[f'{cnt:x}', data])
            cnt += 1

    def decode_op(self, op):
        if lang.code_com_list[op[:8]] == 'PUSH':
            return 'PUSH ' + str(int(op[8:], 2))
        else:
            return lang.code_com_list[op[:8]]


if __name__ == '__main__':
    app = GUI()
    app.run()
