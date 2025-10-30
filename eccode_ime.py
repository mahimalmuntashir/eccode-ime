# F1225040103
# MAHIM AL MUNTASHIR BILLAH
# Masters of Computer Technology
# NJUPT - Nanjing University of Posts and Telecommunications

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from collections import defaultdict

APP_TITLE = "ECCode IME (Easy Chinese Code)"
DEFAULT_XLSX = os.path.join(os.path.dirname(__file__), "eccode_dataset.xlsx")

def normalize_code(*parts):
    """Join non-null code parts into a single lowercase string (e.g., 'y','h',None -> 'yh')."""
    s = "".join([str(p) for p in parts if pd.notna(p)]).strip()
    return s.lower()

def load_eccode_excel(path: str):
    """Load and parse the ECCode dataset from an Excel file."""
    df = pd.read_excel(path, sheet_name=0)
    char_col = None
    code_cols = []
    for c in df.columns:
        if str(c).strip() in ["汉字", "字", "字符", "Character"]:
            char_col = c
    if char_col is None and len(df.columns) >= 2:
        char_col = df.columns[1]
    preferred = [c for c in df.columns if str(c).startswith('Unnamed:')]
    code_cols = preferred[:4]
    if not code_cols:
        for c in df.columns:
            vals = df[c].astype(str).str.fullmatch(r"[A-Za-z]{1,4}").sum()
            if vals > 10:
                code_cols.append(c)
        code_cols = code_cols[:4]
    
    codes = []
    for _, row in df.iterrows():
        ch = str(row.get(char_col, "")).strip()
        if ch and ch != "nan":
            code = normalize_code(*(row.get(c, "") for c in code_cols))
            if code:
                codes.append((ch, code))

    seen = set()
    unique_codes = []
    for ch, cd in codes:
        key = (ch, cd)
        if key not in seen:
            seen.add(key)
            unique_codes.append((ch, cd))

    code_to_chars = defaultdict(list)
    for ch, cd in unique_codes:
        if ch not in code_to_chars[cd]:
            code_to_chars[cd].append(ch)

    return unique_codes, code_to_chars

class ECCodeIME(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("780x520")
        self.minsize(900, 700)

        self.codes = []
        self.code_to_chars = {}
        self.current_code = tk.StringVar()
        self.composed_text = tk.StringVar()
        self.status_text = tk.StringVar(value="Load dataset or start typing…")

        self.create_widgets()
        self.try_autoload()

        for i in range(1, 10):
            self.bind(str(i), self._make_pick_handler(i-1))
        self.bind("<space>", self.commit_first)
        self.bind("<Return>", self.commit_first)
        self.bind("<Escape>", self.clear_code)

    def try_autoload(self):
        if os.path.exists(DEFAULT_XLSX):
            try:
                self.load_dataset(DEFAULT_XLSX)
                self.status_text.set(f"Loaded dataset: {os.path.basename(DEFAULT_XLSX)} — {len(self.codes)} mappings")
            except Exception as e:
                self.status_text.set(f"Autoload failed: {e}")
        else:
            self.status_text.set("No default dataset found, please click ‘Load Excel…’")

    def create_widgets(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        ttk.Button(toolbar, text="Load Excel…", command=self.browse_dataset).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Save Text…", command=self.save_text).pack(side=tk.LEFT, padx=6)
        ttk.Button(toolbar, text="Copy", command=self.copy_text).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=6)
        ttk.Button(toolbar, text="Help", command=self.show_help).pack(side=tk.LEFT)

        # Composed text (set it to be readonly)
        out_frame = ttk.LabelFrame(self, text="Composed Text")
        out_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=10, pady=6)

        self.output = tk.Text(out_frame, height=4, font=("Noto Sans CJK SC", 18), state=tk.DISABLED)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.statusbar = ttk.Label(self, textvariable=self.status_text, anchor="w")
        self.statusbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0,8))

        # Input frame
        inframe = ttk.LabelFrame(self, text="Code Input")
        inframe.pack(side=tk.TOP, fill=tk.X, padx=10, pady=6)
        ttk.Label(inframe, text="Code:").pack(side=tk.LEFT, padx=(8,4), pady=6)
        entry = ttk.Entry(inframe, textvariable=self.current_code, width=40, font=("Consolas", 14))
        entry.pack(side=tk.LEFT, padx=4, pady=6, fill=tk.X, expand=True)
        entry.bind("<KeyRelease>", self.on_code_changed)

        ttk.Button(inframe, text="Commit ①", command=self.commit_first).pack(side=tk.LEFT, padx=4)

        # Candidates
        cand_frame = ttk.LabelFrame(self, text="Candidates (1–9 to select; Space/Enter=first)")
        cand_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=6)

        self.cand_list = tk.Listbox(cand_frame, height=10, font=("Noto Sans CJK SC", 16))
        self.cand_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.cand_list.bind("<Double-Button-1>", self.commit_selected)

        self.cand_scroll = ttk.Scrollbar(cand_frame, orient=tk.VERTICAL, command=self.cand_list.yview)
        self.cand_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Reverse lookup (character → codes)
        rev_frame = ttk.LabelFrame(self, text="Reverse Lookup (enter a character to see ECCode)")
        rev_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=6)

        self.rev_char = tk.StringVar()
        ttk.Label(rev_frame, text="字:").pack(side=tk.LEFT, padx=(8,4), pady=6)
        rev_entry = ttk.Entry(rev_frame, textvariable=self.rev_char, width=10, font=("Noto Sans CJK SC", 16))
        rev_entry.pack(side=tk.LEFT, padx=4, pady=6)
        ttk.Button(rev_frame, text="Lookup", command=self.reverse_lookup).pack(side=tk.LEFT, padx=4)
        self.rev_result = ttk.Label(rev_frame, text="", font=("Consolas", 12))
        self.rev_result.pack(side=tk.LEFT, padx=10)

        self.cand_list.config(yscrollcommand=self.cand_scroll.set)

    def browse_dataset(self):
        path = filedialog.askopenfilename(
            title="Choose ECCode Excel file",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if path:
            try:
                self.load_dataset(path)
                self.status_text.set(f"Loaded dataset: {os.path.basename(path)} — {len(self.codes)} mappings")
            except Exception as e:
                messagebox.showerror("Load failed", str(e))

    def load_dataset(self, path):
        self.codes, self.code_to_chars = load_eccode_excel(path)
        self.refresh_candidates()

    def on_code_changed(self, event=None):
        self.refresh_candidates()

    def _search_prefix(self, prefix: str):
        prefix = prefix.lower().strip()
        if not prefix:
            return []
        out = []
        for ch, cd in self.codes:
            if cd.startswith(prefix):
                out.append((ch, cd))
        seen = set()
        uniq = []
        for ch, cd in out:
            if ch not in seen:
                uniq.append((ch, cd))
                seen.add(ch)
        return uniq

    def refresh_candidates(self):
        prefix = self.current_code.get().lower().strip()
        self.cand_list.delete(0, tk.END)
        if not prefix:
            self.status_text.set("Type a code (e.g., 'yh' → 一).")
            return
        result = self._search_prefix(prefix)
        if result:
            for idx, (ch, cd) in enumerate(result[:200]):
                pre = f"{(idx+1)%10}." if idx < 9 else "   "
                self.cand_list.insert(tk.END, f"{pre} {ch}    [{cd}]")
            self.status_text.set(f"{len(result)} candidates for '{prefix}'. 1–9 to pick, Space/Enter commit first.")
        else:
            self.cand_list.insert(tk.END, "（无匹配 / No matches）")
            self.status_text.set(f"No matches for '{prefix}'.")

    def _make_pick_handler(self, index):
        def handler(event=None):
            try:
                text = self.cand_list.get(index)
            except Exception:
                return
            if "[" in text and "]" in text:
                ch = text.split(" ", 2)[1]
                self._commit_char(ch)
        return handler

    def commit_first(self, event=None):
        if self.cand_list.size() > 0:
            text = self.cand_list.get(0)
            if "[" in text and "]" in text and "No matches" not in text:
                ch = text.split(" ", 2)[1]
                self._commit_char(ch)
        return "break"

    def commit_selected(self, event=None):
        sel = self.cand_list.curselection()
        if not sel:
            return
        idx = sel[0]
        text = self.cand_list.get(idx)
        if "[" in text and "]" in text and "No matches" not in text:
            ch = text.split(" ", 2)[1]
            self._commit_char(ch)

    def _commit_char(self, ch: str):
        self.output.config(state=tk.NORMAL)  # Temporarily enable editing
        self.output.insert(tk.END, ch)
        self.output.config(state=tk.DISABLED)  # Disable editing again
        self.clear_code()

    def clear_code(self, event=None):
        self.current_code.set("")
        self.refresh_candidates()
        return "break"

    def copy_text(self):
        text = self.output.get("1.0", tk.END).rstrip("\n")
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_text.set("Copied to clipboard.")

    def save_text(self):
        text = self.output.get("1.0", tk.END)
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save composed text"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            self.status_text.set(f"Saved: {os.path.basename(path)}")

    def clear_all(self):
        # Clear the code input field
        self.current_code.set("")  
        # Clear the Composed Text area (make it read-only again)
        self.output.config(state=tk.NORMAL)  # Temporarily enable editing
        self.output.delete("1.0", tk.END)    # Clear text
        self.output.config(state=tk.DISABLED)  # Disable editing again
        self.clear_code()  # Ensure the candidate list is refreshed

    def reverse_lookup(self):
        ch = self.rev_char.get().strip()
        if not ch:
            self.rev_result.config(text="")
            return
        codes = [cd for (c, cd) in self.codes if c == ch]
        codes = sorted(set(codes), key=len)
        if codes:
            self.rev_result.config(text=f"Codes: {', '.join(codes)}")
        else:
            self.rev_result.config(text="No code found.")

    def show_help(self):
        msg = (
            "ECCode IME usage:\n"
            "• Type ECCode codes into the Code box. Examples: yh → 一, zkii → 中.\n"
            "• Candidate list updates as you type (prefix search).\n"
            "• Press 1–9 to pick a candidate; Space/Enter commits the first.\n"
            "• Use ‘Load Excel…’ to switch to another ECCode dataset.\n"
            "• ‘Copy’ copies the composed text to the clipboard; ‘Save Text…’ saves as .txt.\n"
            "\nDataset columns expected:\n"
            "• ‘汉字’ (Chinese character)\n"
            "• One or more code columns containing small Latin-letter codes. This app concatenates them.\n\n"
            "© 2025 - Mahim Al Muntashir Billah\n"
            "NJUPT - Nanjing University of Posts and Telecommunications\n"
            "Website: https://www.mahimalmuntashir.com/\n"
            "Email: contact@mahimalmuntashir.com"
        )
        messagebox.showinfo("Help", msg)

def main():
    app = ECCodeIME()
    app.mainloop()

if __name__ == "__main__":
    main()
