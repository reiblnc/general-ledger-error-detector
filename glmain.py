
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

import customtkinter as ctk
import pandas as pd


# =========================================================
# APPLICATION SETTINGS
# =========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

FONT = "Calibri"

FONT_TITLE = (FONT, 29, "bold")
FONT_SUBTITLE = (FONT, 15, "bold")
FONT_HEADING = (FONT, 19, "bold")
FONT_BODY = (FONT, 15)
FONT_BUTTON = (FONT, 15, "bold")
FONT_TABLE = (FONT, 14)
FONT_TABLE_HEADER = (FONT, 14, "bold")

# COLOR PALETTE
BACKGROUND = "#F4F7FB"
WHITE = "#FFFFFF"
SOFT_BLUE = "#EAF3FA"
MINT = "#DDF2EE"
TEAL = "#278C83"
DARK_TEAL = "#20766F"
BLUE = "#3976A8"
DARK_BLUE = "#263F59"
TEXT = "#263445"
MUTED = "#718096"
VERTICAL_LINE = "#B8C9D8"
ALT_ROW = "#F1F6FA"
SUCCESS = "#278052"
DANGER = "#B54747"


# =========================================================
# GENERAL LEDGER ERROR DETECTOR
# =========================================================

class LedgerErrorDetector(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("GENERAL LEDGER ERROR DETECTOR SYSTEM")
        self.geometry("1250x780")
        self.minsize(950, 620)
        self.configure(fg_color=BACKGROUND)

        self.ledger_file = None
        self.coa_file = None
        self.coa_accounts = set()
        self.issues = []
        self.ledger_data = None

        self.column_titles = [
            "NO.", "ISSUE", "GL ROW", "ACCOUNT", "DETAILS"
        ]

        self.column_widths = [70, 210, 100, 240, 550]

        self.create_interface()

    # =====================================================
    # MAIN INTERFACE
    # =====================================================

    def create_interface(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND,
            corner_radius=0
        )
        main_frame.grid(
            row=0, column=0,
            sticky="nsew",
            padx=24, pady=20
        )

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = ctk.CTkFrame(
            main_frame,
            fg_color=SOFT_BLUE,
            corner_radius=14,
            border_width=1,
            border_color="#D6E5F0"
        )
        header.grid(
            row=0, column=0,
            sticky="ew",
            pady=(0, 16)
        )

        header.grid_columnconfigure(1, weight=1)

        # LEDGER LOGO
        logo = tk.Canvas(
            header,
            width=68,
            height=68,
            bg=SOFT_BLUE,
            highlightthickness=0
        )
        logo.grid(
            row=0, column=0,
            padx=(20, 14), pady=15
        )

        logo.create_rectangle(
            10, 8, 57, 60,
            fill=TEAL,
            outline=TEAL
        )

        logo.create_rectangle(
            16, 13, 51, 55,
            fill=WHITE,
            outline=WHITE
        )

        logo.create_line(
            33, 14, 33, 54,
            fill=TEAL,
            width=2
        )

        for y in [23, 32, 41]:
            logo.create_line(
                21, y, 29, y,
                fill=BLUE,
                width=2
            )
            logo.create_line(
                37, y, 46, y,
                fill=BLUE,
                width=2
            )

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        title_frame.grid(
            row=0, column=1,
            sticky="w",
            pady=15
        )

        ctk.CTkLabel(
            title_frame,
            text="GENERAL LEDGER",
            font=FONT_TITLE,
            text_color=DARK_BLUE
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="ERROR DETECTOR SYSTEM",
            font=FONT_SUBTITLE,
            text_color=TEAL
        ).pack(anchor="w", pady=(1, 0))

        ctk.CTkLabel(
            title_frame,
            text="ACCOUNTING REVIEW & VALIDATION",
            font=(FONT, 12, "bold"),
            text_color=MUTED
        ).pack(anchor="w", pady=(4, 0))

        # -------------------------------------------------
        # GENERAL LEDGER FILE
        # -------------------------------------------------

        file_frame = ctk.CTkFrame(
            main_frame,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color="#E0E8F0"
        )
        file_frame.grid(
            row=1, column=0,
            sticky="ew",
            pady=(0, 14)
        )

        file_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            file_frame,
            text="GENERAL LEDGER FILE",
            font=FONT_BODY,
            text_color=DARK_BLUE
        ).grid(
            row=0, column=0,
            sticky="w",
            padx=18, pady=(14, 5)
        )

        self.file_label = ctk.CTkLabel(
            file_frame,
            text="NO GENERAL LEDGER FILE SELECTED",
            font=FONT_BODY,
            text_color=MUTED,
            anchor="w"
        )
        self.file_label.grid(
            row=1, column=0,
            sticky="ew",
            padx=18, pady=(0, 10)
        )

        ctk.CTkButton(
            file_frame,
            text="BROWSE GENERAL LEDGER",
            font=FONT_BUTTON,
            height=46,
            corner_radius=8,
            fg_color=BLUE,
            hover_color=DARK_BLUE,
            command=self.browse_ledger
        ).grid(
            row=2, column=0,
            sticky="ew",
            padx=18, pady=(0, 16)
        )

        # -------------------------------------------------
        # ACTION BUTTONS
        # -------------------------------------------------

        button_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        button_frame.grid(
            row=2, column=0,
            sticky="ew",
            pady=(0, 14)
        )

        for col in range(3):
            button_frame.grid_columnconfigure(
                col, weight=1
            )

        ctk.CTkButton(
            button_frame,
            text="CHECK LEDGER",
            font=FONT_BUTTON,
            height=46,
            corner_radius=8,
            fg_color=TEAL,
            hover_color=DARK_TEAL,
            command=self.check_ledger
        ).grid(
            row=0, column=0,
            sticky="ew",
            padx=(0, 7)
        )

        ctk.CTkButton(
            button_frame,
            text="CHART OF ACCOUNTS",
            font=FONT_BUTTON,
            height=46,
            corner_radius=8,
            fg_color=BLUE,
            hover_color=DARK_BLUE,
            command=self.register_coa
        ).grid(
            row=0, column=1,
            sticky="ew",
            padx=7
        )

        ctk.CTkButton(
            button_frame,
            text="EXPORT REPORT",
            font=FONT_BUTTON,
            height=46,
            corner_radius=8,
            fg_color=DARK_BLUE,
            hover_color="#172D43",
            command=self.export_report
        ).grid(
            row=0, column=2,
            sticky="ew",
            padx=(7, 0)
        )

        # -------------------------------------------------
        # AUDIT RESULTS
        # -------------------------------------------------

        results_frame = ctk.CTkFrame(
            main_frame,
            fg_color=WHITE,
            corner_radius=12,
            border_width=1,
            border_color="#E0E8F0"
        )
        results_frame.grid(
            row=3, column=0,
            sticky="nsew"
        )

        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)

        results_header = ctk.CTkFrame(
            results_frame,
            fg_color="transparent"
        )
        results_header.grid(
            row=0, column=0,
            sticky="ew",
            padx=18, pady=15
        )

        results_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            results_header,
            text="AUDIT RESULTS",
            font=FONT_HEADING,
            text_color=DARK_BLUE
        ).grid(
            row=0, column=0,
            sticky="w"
        )

        self.status_label = ctk.CTkLabel(
            results_header,
            text="READY TO CHECK YOUR GENERAL LEDGER",
            font=(FONT, 13, "bold"),
            text_color=MUTED
        )
        self.status_label.grid(
            row=0, column=1,
            sticky="e"
        )

        # TABLE CONTAINER
        table_container = tk.Frame(
            results_frame,
            bg=WHITE
        )
        table_container.grid(
            row=1, column=0,
            sticky="nsew",
            padx=14, pady=(0, 14)
        )

        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)

        self.table_canvas = tk.Canvas(
            table_container,
            bg=WHITE,
            highlightthickness=0
        )
        self.table_canvas.grid(
            row=0, column=0,
            sticky="nsew"
        )

        scrollbar_y = ctk.CTkScrollbar(
            table_container,
            orientation="vertical",
            command=self.table_canvas.yview
        )
        scrollbar_y.grid(
            row=0, column=1,
            sticky="ns"
        )

        scrollbar_x = ctk.CTkScrollbar(
            table_container,
            orientation="horizontal",
            command=self.table_canvas.xview
        )
        scrollbar_x.grid(
            row=1, column=0,
            sticky="ew"
        )

        self.table_canvas.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.table_inner = tk.Frame(
            self.table_canvas,
            bg=WHITE
        )

        self.table_window = self.table_canvas.create_window(
            (0, 0),
            window=self.table_inner,
            anchor="nw"
        )

        self.table_inner.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.table_canvas.bind(
            "<Configure>",
            self.resize_table
        )

        self.create_table_header()

    # =====================================================
    # TABLE - VERTICAL SEPARATORS ONLY
    # =====================================================

    def create_table_header(self):

        for col, title in enumerate(self.column_titles):

            actual_col = col * 2

            self.table_inner.grid_columnconfigure(
                actual_col,
                minsize=self.column_widths[col],
                weight=1 if col in [1, 3, 4] else 0
            )

            header = tk.Label(
                self.table_inner,
                text=title,
                font=FONT_TABLE_HEADER,
                bg=MINT,
                fg=DARK_BLUE,
                padx=10,
                pady=13,
                anchor="w"
            )

            header.grid(
                row=0,
                column=actual_col,
                sticky="nsew"
            )

            self.table_inner.grid_columnconfigure(
                actual_col + 1,
                minsize=1,
                weight=0
            )

            separator = tk.Frame(
                self.table_inner,
                bg=VERTICAL_LINE,
                width=1
            )

            separator.grid(
                row=0,
                column=actual_col + 1,
                sticky="ns"
            )

    def update_scroll_region(self, event=None):

        self.table_canvas.configure(
            scrollregion=self.table_canvas.bbox("all")
        )

    def resize_table(self, event):

        total_width = sum(self.column_widths) + 5

        self.table_canvas.itemconfigure(
            self.table_window,
            width=max(event.width, total_width)
        )

    def display_results(self):

        # REMOVE PREVIOUS RESULT ROWS
        for widget in self.table_inner.winfo_children():

            info = widget.grid_info()

            if info and int(info["row"]) > 0:
                widget.destroy()

        if not self.issues:

            success_label = tk.Label(
                self.table_inner,
                text="NO ISSUES FOUND. YOUR GENERAL LEDGER PASSED THE AVAILABLE CHECKS.",
                font=(FONT, 14, "bold"),
                bg=WHITE,
                fg=SUCCESS,
                padx=12,
                pady=18,
                anchor="w"
            )

            success_label.grid(
                row=1,
                column=0,
                columnspan=10,
                sticky="nsew"
            )

            self.update_scroll_region()
            return

        for index, issue in enumerate(self.issues, start=1):

            values = [
                index,
                issue["issue"].upper(),
                issue["row"],
                issue["account"],
                issue["details"].upper()
            ]

            row_bg = WHITE if index % 2 == 1 else ALT_ROW

            for col, value in enumerate(values):

                actual_col = col * 2

                cell = tk.Label(
                    self.table_inner,
                    text=str(value),
                    font=FONT_TABLE,
                    bg=row_bg,
                    fg=TEXT,
                    padx=10,
                    pady=12,
                    anchor="w",
                    justify="left",
                    wraplength=self.column_widths[col] - 20
                )

                cell.grid(
                    row=index,
                    column=actual_col,
                    sticky="nsew"
                )

                separator = tk.Frame(
                    self.table_inner,
                    bg=VERTICAL_LINE,
                    width=1
                )

                separator.grid(
                    row=index,
                    column=actual_col + 1,
                    sticky="ns"
                )

        self.update_scroll_region()

    # =====================================================
    # CHART OF ACCOUNTS
    # =====================================================

    def register_coa(self):

        file_path = filedialog.askopenfilename(
            title="SELECT CHART OF ACCOUNTS",
            filetypes=[
                ("EXCEL FILES", "*.xlsx *.xls"),
                ("ALL FILES", "*.*")
            ]
        )

        if not file_path:
            return

        try:

            coa_df = pd.read_excel(file_path)

            account_column = None

            for column in coa_df.columns:

                if str(column).strip().casefold() == "account title":
                    account_column = column
                    break

            if account_column is None:

                messagebox.showerror(
                    "INVALID CHART OF ACCOUNTS",
                    "THE EXCEL FILE MUST CONTAIN AN ACCOUNT TITLE COLUMN."
                )
                return

            self.coa_accounts = {
                str(account).strip().casefold()
                for account in coa_df[account_column].dropna()
                if str(account).strip()
            }

            self.coa_file = file_path

            messagebox.showinfo(
                "CHART OF ACCOUNTS REGISTERED",
                f"SUCCESSFULLY REGISTERED {len(self.coa_accounts)} ACCOUNT TITLES."
            )

        except Exception as e:

            messagebox.showerror(
                "ERROR",
                f"UNABLE TO REGISTER CHART OF ACCOUNTS:\n{e}"
            )

    # =====================================================
    # BROWSE GENERAL LEDGER
    # =====================================================

    def browse_ledger(self):

        file_path = filedialog.askopenfilename(
            title="SELECT GENERAL LEDGER",
            filetypes=[
                ("EXCEL FILES", "*.xlsx *.xls"),
                ("ALL FILES", "*.*")
            ]
        )

        if file_path:

            self.ledger_file = file_path

            self.file_label.configure(
                text=Path(file_path).name.upper(),
                text_color=TEXT
            )

            self.status_label.configure(
                text="GENERAL LEDGER FILE SELECTED",
                text_color=BLUE
            )

    # =====================================================
    # ISSUE HANDLER
    # =====================================================

    def add_issue(self, issue, row, account, details):

        self.issues.append({
            "issue": issue,
            "row": row,
            "account": account,
            "details": details
        })

    # =====================================================
    # CHECK GENERAL LEDGER
    # =====================================================

    def check_ledger(self):

        if not self.ledger_file:

            messagebox.showwarning(
                "NO FILE SELECTED",
                "PLEASE SELECT A GENERAL LEDGER FILE FIRST."
            )
            return

        try:

            df = pd.read_excel(self.ledger_file)

            df.columns = [
                str(column).strip().upper()
                for column in df.columns
            ]

            required_columns = ["DATE", "ACCOUNT"]

            missing_columns = [
                col for col in required_columns
                if col not in df.columns
            ]

            if missing_columns:

                messagebox.showerror(
                    "MISSING COLUMNS",
                    "THE GENERAL LEDGER MUST CONTAIN DATE AND ACCOUNT COLUMNS."
                )
                return

            if "DEBIT" not in df.columns:
                df["DEBIT"] = 0

            if "CREDIT" not in df.columns:
                df["CREDIT"] = 0

            self.ledger_data = df.copy()
            self.issues = []

            # CHECK EACH ROW
            for index, row in df.iterrows():

                excel_row = index + 2

                account = (
                    str(row["ACCOUNT"]).strip()
                    if pd.notna(row["ACCOUNT"])
                    else ""
                )

                # MISSING ACCOUNT
                if not account:

                    self.add_issue(
                        "Missing Account",
                        excel_row,
                        "-",
                        "Account title is missing."
                    )

                # MISSING OR INVALID DATE
                if pd.isna(row["DATE"]):

                    self.add_issue(
                        "Missing Date",
                        excel_row,
                        account or "-",
                        "Transaction date is missing."
                    )

                else:

                    try:
                        pd.to_datetime(row["DATE"], errors="raise")

                    except Exception:

                        self.add_issue(
                            "Invalid Date",
                            excel_row,
                            account or "-",
                            f"Invalid date value: {row['DATE']}"
                        )

                # NUMERIC VALIDATION
                debit_raw = row["DEBIT"]
                credit_raw = row["CREDIT"]

                debit_value = pd.to_numeric(
                    pd.Series([debit_raw]),
                    errors="coerce"
                ).iloc[0]

                credit_value = pd.to_numeric(
                    pd.Series([credit_raw]),
                    errors="coerce"
                ).iloc[0]

                debit_has_value = (
                    pd.notna(debit_raw) and str(debit_raw).strip() != ""
                )

                credit_has_value = (
                    pd.notna(credit_raw) and str(credit_raw).strip() != ""
                )

                if pd.isna(debit_value) and debit_has_value:

                    self.add_issue(
                        "Invalid Debit",
                        excel_row,
                        account or "-",
                        "Debit amount is not numeric."
                    )

                if pd.isna(credit_value) and credit_has_value:

                    self.add_issue(
                        "Invalid Credit",
                        excel_row,
                        account or "-",
                        "Credit amount is not numeric."
                    )

                debit = 0 if pd.isna(debit_value) else float(debit_value)
                credit = 0 if pd.isna(credit_value) else float(credit_value)

                # NEGATIVE AMOUNTS
                if debit < 0:

                    self.add_issue(
                        "Negative Debit",
                        excel_row,
                        account or "-",
                        "Debit amount should not be negative."
                    )

                if credit < 0:

                    self.add_issue(
                        "Negative Credit",
                        excel_row,
                        account or "-",
                        "Credit amount should not be negative."
                    )

                # BOTH DEBIT AND CREDIT ON ONE ROW
                if debit > 0 and credit > 0:

                    self.add_issue(
                        "Review Entry",
                        excel_row,
                        account or "-",
                        "Both debit and credit amounts are entered on the same row. Review the entry."
                    )

                # CHECK ACCOUNT AGAINST COA
                if account and self.coa_accounts:

                    if account.casefold() not in self.coa_accounts:

                        self.add_issue(
                            "Account Not in COA",
                            excel_row,
                            account,
                            "Account title was not found in the registered Chart of Accounts."
                        )

            # DUPLICATE ROW CHECK
            duplicates = df.duplicated(
                subset=list(df.columns),
                keep=False
            )

            for index in df[duplicates].index:

                row = df.loc[index]

                account = (
                    str(row["ACCOUNT"]).strip()
                    if pd.notna(row["ACCOUNT"])
                    else "-"
                )

                self.add_issue(
                    "Possible Duplicate",
                    index + 2,
                    account,
                    "This General Ledger row appears to be duplicated. Review before treating it as an error."
                )

            # TOTAL DEBIT AND CREDIT CHECK
            debit_total = pd.to_numeric(
                df["DEBIT"],
                errors="coerce"
            ).fillna(0).sum()

            credit_total = pd.to_numeric(
                df["CREDIT"],
                errors="coerce"
            ).fillna(0).sum()

            if abs(debit_total - credit_total) > 0.01:

                self.add_issue(
                    "Unbalanced GL",
                    "-",
                    "-",
                    f"Total Debit: {debit_total:,.2f} | "
                    f"Total Credit: {credit_total:,.2f} | "
                    f"Difference: {debit_total - credit_total:,.2f}"
                )

            # DISPLAY RESULTS
            self.display_results()

            if self.issues:

                self.status_label.configure(
                    text=f"{len(self.issues)} ISSUE(S) FOUND",
                    text_color=DANGER
                )

                messagebox.showwarning(
                    "LEDGER CHECK COMPLETED",
                    f"CHECKING COMPLETED.\n\n"
                    f"{len(self.issues)} ISSUE(S) FOUND.\n"
                    f"PLEASE REVIEW THE AUDIT RESULTS."
                )

            else:

                self.status_label.configure(
                    text="NO ISSUES FOUND",
                    text_color=SUCCESS
                )

                messagebox.showinfo(
                    "LEDGER CHECK COMPLETED",
                    "NO ISSUES WERE FOUND BASED ON THE AVAILABLE CHECKS."
                )

        except Exception as e:

            messagebox.showerror(
                "ERROR",
                f"UNABLE TO CHECK GENERAL LEDGER:\n{e}"
            )

    # =====================================================
    # EXPORT REPORT
    # =====================================================

    def export_report(self):

        if not self.issues:

            messagebox.showwarning(
                "NO REPORT AVAILABLE",
                "THERE ARE NO AUDIT ISSUES TO EXPORT."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="SAVE AUDIT REPORT",
            defaultextension=".xlsx",
            filetypes=[
                ("EXCEL FILES", "*.xlsx")
            ],
            initialfile="General_Ledger_Audit_Report.xlsx"
        )

        if not file_path:
            return

        try:

            report_df = pd.DataFrame(self.issues)

            report_df.insert(
                0,
                "NO.",
                range(1, len(report_df) + 1)
            )

            report_df.columns = [
                "NO.",
                "ISSUE",
                "GL ROW",
                "ACCOUNT",
                "DETAILS"
            ]

            report_df.to_excel(
                file_path,
                index=False
            )

            messagebox.showinfo(
                "REPORT EXPORTED",
                f"AUDIT REPORT SUCCESSFULLY SAVED:\n{file_path}"
            )

        except Exception as e:

            messagebox.showerror(
                "EXPORT ERROR",
                f"UNABLE TO EXPORT REPORT:\n{e}"
            )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app = LedgerErrorDetector()
    app.mainloop()
