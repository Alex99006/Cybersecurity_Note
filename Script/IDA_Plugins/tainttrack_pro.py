# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# TaintTrackPro - IDA Pro 9.0/9.1 compatible plugin (full)
# 功能：
#  - 追踪函数参数（a1/a2/...）的候选定义/来源（启发式）
#  - 生成 DOT、可选 PNG（需要 graphviz dot），以及 HTML 报告
#  - GUI 窗口内展示 HTML（链接 ida:0x... 可跳转到 IDA 地址）
#  - 注册菜单项并支持快捷键 Alt+F8 打开界面
# 使用：
#  - 将此文件放到 IDA plugins 目录，重启 IDA
#  - 或 File->Script file... 直接运行
# -------------------------------------------------------------------------

from __future__ import print_function
import idaapi
import ida_kernwin
import idc
import idautils
import ida_funcs
import os
import time
import re
import subprocess
import traceback

# ---------------- CONFIG ----------------
OUT_DIR = "/tmp"
OUT_DOT = os.path.join(OUT_DIR, "ida_taint_graph.dot")
OUT_PNG = os.path.join(OUT_DIR, "ida_taint_graph.png")
OUT_HTML = os.path.join(OUT_DIR, "ida_taint_report.html")
GRAPHVIZ_BIN = "dot"    # optional external dependency to render PNG

TAINT_SOURCES = [
    "read", "recv", "recvfrom", "recvmsg", "accept",
    "fgets", "gets", "getline", "getenv", "proc_open_buffer",
    "proc_open", "buffer_init_string", "fread", "readline"
]
DANGEROUS_SINKS = [
    "system", "popen", "execl", "execlp", "execv", "execve", "execvp", "execle"
]

# ---------------- utilities ----------------
def dbg(msg):
    idaapi.msg("[TaintTrackPro] %s\n" % str(msg))

def safe_get_inf():
    """
    Return IDA's 'inf' structure in a way compatible across IDA 9.0 variants.
    """
    try:
        return idaapi.get_inf()  # IDA >= 7.0/9.x provides this
    except Exception:
        pass
    try:
        return idaapi.get_inf_structure()
    except Exception:
        pass
    try:
        import ida_idaapi
        return ida_idaapi.get_inf_structure()
    except Exception:
        pass
    return None

def is_64bit():
    inf = safe_get_inf()
    if not inf:
        return False
    try:
        if hasattr(inf, "is_64bit"):
            return inf.is_64bit()
        if hasattr(inf, "is_64bit_app"):
            return inf.is_64bit_app()
    except Exception:
        pass
    return False

def proc_name_lower():
    inf = safe_get_inf()
    if not inf:
        return ""
    try:
        if hasattr(inf, "procName"):
            return inf.procName.lower()
        if hasattr(inf, "procname"):
            return inf.procname.lower()
    except Exception:
        pass
    return ""

# ---------------- architecture helpers ----------------
def get_arg_reg_for_arch(arg_index):
    """
    Return register name for argument index (0-based) for common ABIs.
    If None -> likely stack-based pushes (32-bit x86).
    """
    p = proc_name_lower()
    is64 = is_64bit()
    if "metapc" in p or "x86" in p:
        if is64:
            regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
            return regs[arg_index] if arg_index < len(regs) else None
        else:
            return None
    if "arm" in p:
        regs = ["r0", "r1", "r2", "r3", "r4", "r5"]
        return regs[arg_index] if arg_index < len(regs) else None
    if "mips" in p:
        regs = ["a0", "a1", "a2", "a3"]
        return regs[arg_index] if arg_index < len(regs) else None
    # fallback to x86_64 style if 64-bit
    if is64:
        regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]
        return regs[arg_index] if arg_index < len(regs) else None
    return None

# ---------------- find argument definition at call site ----------------
def find_call_arg_definition(call_ea, arg_index=0, lookback_limit=300):
    """
    Heuristic:
      - For register ABI: scan backwards and find instruction that writes to the argument register
      - For push-based (32-bit): collect 'push' instructions (nearest push is last param)
    Returns list of (ea, mnem, ops_text)
    """
    arch_reg = get_arg_reg_for_arch(arg_index)
    defs = []
    cur = call_ea
    pushes = []
    for i in range(lookback_limit):
        prev = idc.prev_head(cur)
        if prev == idc.BADADDR or prev is None:
            break
        cur = prev
        try:
            mnem = idc.print_insn_mnem(cur).lower()
            ops = " ".join([idc.print_operand(cur, j) or "" for j in range(6)])
        except Exception:
            continue
        if arch_reg is None:
            # collect pushes (32-bit)
            if mnem == "push":
                pushes.append((cur, mnem, ops))
        else:
            # if instruction writes to arch_reg -> definition
            if any(mnem.startswith(x) for x in ("mov", "lea", "xor", "add", "sub", "movabs", "movq", "movl", "movzx", "movsx")):
                op0 = idc.print_operand(cur, 0) or ""
                if arch_reg in op0.lower():
                    defs.append((cur, mnem, ops))
                    return defs
            if mnem == "xor" and arch_reg in ops.lower():
                defs.append((cur, mnem, ops))
                return defs
    # if 32-bit push-based and we collected pushes
    if pushes:
        # pushes scanned backward so pushes[0] is closest to call
        if arg_index < len(pushes):
            return [pushes[arg_index]]
    return defs

# ---------------- classify a candidate instruction (hint) ----------------
def classify_definition_ea(ea, fmt_text):
    txt = fmt_text or ""
    # immediate pointer to string?
    m = re.search(r'0x[0-9a-fA-F]+', txt)
    if m:
        try:
            addr = int(m.group(0), 16)
            s = idc.get_strlit_contents(addr)
            if s:
                try:
                    return "string_literal@0x%x: %s" % (addr, s.decode(errors="ignore")[:120])
                except Exception:
                    return "string_literal@0x%x" % addr
        except Exception:
            pass
    # returned from call?
    if "call" in txt:
        m2 = re.search(r'call\s+([A-Za-z0-9_@]+)', txt)
        if m2:
            callee = m2.group(1)
            if any(src in callee.lower() for src in TAINT_SOURCES):
                return "returned_from_taint_source:%s" % callee
            return "returned_from:%s" % callee
    if "[" in txt or "ptr" in txt or "rbp" in txt or "ebp" in txt:
        return "memory_load"
    for s in TAINT_SOURCES:
        if s in txt:
            return "taint_source_call:%s" % s
    return "reg_or_expr"

# ---------------- intra-function backward scan ----------------
def backward_slice_function(func_ea, param_index=0, max_steps=2000):
    res = {'definitions': [], 'paths': []}
    f = idaapi.get_func(func_ea)
    if not f:
        return res
    start = f.start_ea
    end = f.end_ea
    arg_reg = get_arg_reg_for_arch(param_index)
    ea = end
    steps = 0
    while True:
        ea = idc.prev_head(ea, start)
        if ea == idc.BADADDR or ea is None:
            break
        steps += 1
        if steps > max_steps:
            break
        try:
            mnem = idc.print_insn_mnem(ea).lower()
            ops = " ".join([idc.print_operand(ea, i) or "" for i in range(6)])
        except Exception:
            continue
        if arg_reg and arg_reg in ops.lower():
            cls = classify_definition_ea(ea, "%s %s" % (mnem, ops))
            res['definitions'].append((ea, "%s %s" % (mnem, ops), cls))
        if mnem.startswith("call") and arg_reg and arg_reg in ops.lower():
            res['paths'].append(('param_pass', ea, ops))
    return res

# ---------------- trace callers ----------------
def trace_callers_and_find_sources(func_ea, param_index=0, max_callers=1000):
    results = []
    # NOTE: IDA newer API uses CodeRefsTo (not CodeReferencesTo)
    for xref in idautils.CodeRefsTo(func_ea, 0):
        call_ea = xref
        try:
            caller_func = idaapi.get_func(call_ea)
            caller_start = caller_func.start_ea if caller_func else 0
        except Exception:
            caller_start = 0
        arg_defs = find_call_arg_definition(call_ea, arg_index=param_index)
        hints = []
        for d in arg_defs:
            dea, mnemtxt, ops = d
            cls = classify_definition_ea(dea, mnemtxt + " " + ops)
            hints.append((dea, mnemtxt + " " + ops, cls))
        # fallback: intra-scan of caller
        if not hints and caller_start:
            intra = backward_slice_function(caller_start, param_index=param_index)
            for dd in intra.get('definitions', []):
                hints.append((dd[0], dd[1], dd[2]))
        results.append({'caller': caller_start, 'call_ea': call_ea, 'hints': hints})
        if len(results) >= max_callers:
            break
    return results

# ---------------- build DOT & HTML ----------------
def build_dot(sources, intra_defs, func_ea, param_idx):
    lines = ["digraph taint {", " rankdir=LR; node [shape=box];"]
    root = "func_%x" % func_ea
    fname = idc.get_func_name(func_ea) or hex(func_ea)
    lines.append(' %s [label="%s:a%d"];' % (root, fname, param_idx+1))
    for d in intra_defs.get('definitions', []):
        dea, full, cls = d
        nid = "n%x" % dea
        lab = "%x\\n%s\\n%s" % (dea, full.replace('"', ''), cls)
        lines.append(' %s [label="%s"];' % (nid, lab))
        lines.append(' %s -> %s [label="intra"];' % (nid, root))
    for r in sources:
        call_ea = r['call_ea']
        caller = r['caller']
        callid = "call_%x" % call_ea
        caller_name = idc.get_func_name(caller) if caller else ("caller_%x" % caller)
        lines.append(' %s [label="%s\\ncall@%x"];' % (callid, caller_name, call_ea))
        lines.append(' %s -> %s [label="callsite"];' % (callid, root))
        for h in r.get('hints', []):
            dea, txt, cls = h
            hid = "h_%x_%x" % (call_ea, dea or id(txt))
            lab = "%s\\n%s" % (hex(dea) if dea else "0", txt.replace('"', ''))
            lines.append(' %s [label="%s\\n%s"];' % (hid, lab, cls))
            lines.append(' %s -> %s [label="argdef"];' % (hid, callid))
    lines.append("}")
    dot_text = "\n".join(lines)
    try:
        with open(OUT_DOT, "w") as fh:
            fh.write(dot_text)
    except Exception as e:
        dbg("Failed to write DOT: %s" % e)
    return dot_text

def build_html_report(func_ea, param_idx, trace_results, intra_defs, dot_text, png_generated=False):
    fname = idc.get_func_name(func_ea) or hex(func_ea)
    header = "<h2>TaintTrace Report for %s : a%d</h2>" % (fname, param_idx+1)
    header += "<p>Generated: %s</p>" % time.strftime("%Y-%m-%d %H:%M:%S")
    header += "<h3>Intra-function definitions</h3><ul>"
    for d in intra_defs.get('definitions', []):
        dea, full, cls = d
        header += '<li><a href="ida:0x%x">0x%x</a> : %s <b>%s</b></li>' % (dea, dea, full.replace("<","&lt;").replace(">","&gt;"), cls)
    header += "</ul>"
    header += "<h3>Callers (%d)</h3>" % len(trace_results)
    header += "<table border='1' cellpadding='4' cellspacing='0'><tr><th>caller</th><th>call@</th><th>candidates</th></tr>"
    for r in trace_results:
        caller = r['caller']
        call_ea = r['call_ea']
        caller_name = idc.get_func_name(caller) or ("0x%x" % caller)
        cell = ""
        if r.get('hints'):
            for h in r['hints']:
                dea, txt, cls = h
                cell += '<div><a href="ida:0x%x">0x%x</a> : %s <i>%s</i></div>' % (dea or 0, dea or 0, txt.replace("<","&lt;").replace(">","&gt;"), cls)
        else:
            cell = "<i>no direct hint</i>"
        header += "<tr><td>%s</td><td><a href='ida:0x%x'>0x%x</a></td><td>%s</td></tr>" % (caller_name, call_ea, call_ea, cell)
    header += "</table>"
    header += "<h3>Graph</h3>"
    if png_generated and os.path.exists(OUT_PNG):
        header += "<p><img src='%s' alt='graph' width='100%%'/></p>" % OUT_PNG
    else:
        header += "<pre>%s</pre>" % (dot_text.replace("<","&lt;").replace(">","&gt;"))
    html = "<html><head><meta charset='utf-8'></head><body>%s</body></html>" % header
    try:
        with open(OUT_HTML, "w") as fh:
            fh.write(html)
    except Exception as e:
        dbg("Failed to write HTML: %s" % e)
    return html

# ---------------- GUI form ----------------
class TaintTrackForm(idaapi.PluginForm):
    def OnCreate(self, form):
        self.parent = self.FormToPyQtWidget(form)
        tried = False
        try:
            from PyQt5 import QtWidgets, QtCore
            tried = True
        except Exception:
            try:
                from PySide2 import QtWidgets, QtCore
                tried = True
            except Exception:
                tried = False
        if not tried:
            ida_kernwin.warning("TaintTrackPro requires PyQt5 or PySide2 for GUI - plugin will still work but without GUI.")
            return
        self.QtWidgets = QtWidgets
        self.QtCore = QtCore
        layout = QtWidgets.QVBoxLayout()
        top = QtWidgets.QHBoxLayout()
        self.param_edit = QtWidgets.QLineEdit("1")
        self.analyze_btn = QtWidgets.QPushButton("Analyze (Alt+F8)")
        self.render_btn = QtWidgets.QPushButton("Render Graph (dot->png)")
        self.save_btn = QtWidgets.QPushButton("Save HTML")
        top.addWidget(QtWidgets.QLabel("Param index (1-based):"))
        top.addWidget(self.param_edit)
        top.addWidget(self.analyze_btn)
        top.addWidget(self.render_btn)
        top.addWidget(self.save_btn)
        layout.addLayout(top)
        self.viewer = QtWidgets.QTextBrowser()
        self.viewer.setOpenExternalLinks(False)
        layout.addWidget(self.viewer)
        self.parent.setLayout(layout)
        self.analyze_btn.clicked.connect(self.on_analyze)
        self.render_btn.clicked.connect(self.on_render)
        self.save_btn.clicked.connect(self.on_save)
        self.viewer.anchorClicked.connect(self.on_anchor_clicked)
        self.current_html = None
        self.last_args = None

    def on_anchor_clicked(self, url):
        try:
            s = str(url.toString())
            m = re.search(r'0x[0-9a-fA-F]+', s)
            if m:
                addr = int(m.group(0), 16)
                idc.jumpto(addr)
        except Exception as e:
            dbg("anchor click error: %s" % e)

    def on_render(self):
        if not os.path.exists(OUT_DOT):
            idaapi.msg("[TaintTrackPro] DOT not found: %s\n" % OUT_DOT)
            return
        try:
            subprocess.run([GRAPHVIZ_BIN, "-Tpng", OUT_DOT, "-o", OUT_PNG], check=True)
            idaapi.msg("[TaintTrackPro] Rendered PNG: %s\n" % OUT_PNG)
            if self.current_html and self.last_args:
                func_ea, pidx, trace_results, intra_defs, dot_text = self.last_args
                html = build_html_report(func_ea, pidx, trace_results, intra_defs, dot_text, png_generated=True)
                self.current_html = html
                self.viewer.setHtml(html)
        except Exception as e:
            dbg("Graphviz rendering failed: %s" % e)

    def on_save(self):
        if self.current_html:
            try:
                with open(OUT_HTML, "w") as fh:
                    fh.write(self.current_html)
                idaapi.msg("[TaintTrackPro] HTML saved: %s\n" % OUT_HTML)
            except Exception as e:
                dbg("Failed to save HTML: %s" % e)
        else:
            idaapi.msg("[TaintTrackPro] No report to save\n")

    def on_analyze(self):
        try:
            param_index = int(self.param_edit.text().strip()) - 1
        except Exception:
            ida_kernwin.warning("Invalid param index")
            return
        ea = idc.here()
        f = idaapi.get_func(ea)
        if not f:
            ida_kernwin.warning("No function at current cursor")
            return
        func_ea = f.start_ea
        idaapi.msg("[TaintTrackPro] Analyzing %s param a%d\n" % (idc.get_func_name(func_ea) or hex(func_ea), param_index+1))
        intra_defs = backward_slice_function(func_ea, param_index)
        trace_results = trace_callers_and_find_sources(func_ea, param_index)
        dot_text = build_dot(trace_results, intra_defs, func_ea, param_index)
        png_ok = False
        try:
            subprocess.run([GRAPHVIZ_BIN, "-Tpng", OUT_DOT, "-o", OUT_PNG], check=True)
            png_ok = os.path.exists(OUT_PNG)
        except Exception:
            png_ok = False
        html = build_html_report(func_ea, param_index, trace_results, intra_defs, dot_text, png_generated=png_ok)
        self.current_html = html
        self.last_args = (func_ea, param_index, trace_results, intra_defs, dot_text)
        self.viewer.setHtml(html)
        idaapi.msg("[TaintTrackPro] Report generated (DOT/HTML)\n")

# ---------------- plugin definition ----------------
class TaintTrackPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP
    comment = "TaintTrackPro - argument backward slice and taint analysis"
    help = "Run TaintTrackPro (Alt+F8)"
    wanted_name = "TaintTrackPro"
    wanted_hotkey = "Alt-F8"

    def init(self):
        idaapi.msg("[TaintTrackPro] loaded\n")
        # register action (works on IDA 7.x / 8.x / 9.x)
        self.action_name = "tainttrack:open"
        try:
            act = idaapi.action_desc_t(
                self.action_name,
                "TaintTrackPro Analysis",
                TaintActionHandler(self),
                self.wanted_hotkey,
                "Trace param taint and generate report",
                199
            )
            idaapi.register_action(act)
            try:
                # attach menu - best effort
                idaapi.attach_action_to_menu("Edit/", self.action_name, idaapi.SETMENU_APP)
            except Exception:
                pass
        except Exception as e:
            dbg("action registration failed: %s" % e)
        return idaapi.PLUGIN_OK

    def run(self, arg):
        try:
            form = TaintTrackForm()
            form.Show("TaintTrackPro", options=idaapi.PluginForm.WOPN_PERSIST)
        except Exception as e:
            dbg("run error: %s" % e)
            traceback.print_exc()

    def term(self):
        idaapi.msg("[TaintTrackPro] terminated\n")

class TaintActionHandler(idaapi.action_handler_t):
    def __init__(self, plugin):
        idaapi.action_handler_t.__init__(self)
        self.plugin = plugin

    def activate(self, ctx):
        try:
            form = TaintTrackForm()
            form.Show("TaintTrackPro", options=idaapi.PluginForm.WOPN_PERSIST)
            return 1
        except Exception as e:
            dbg("action activate error: %s" % e)
            return 0

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS

def PLUGIN_ENTRY():
    return TaintTrackPlugin()