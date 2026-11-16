
# GENERAL LEDGER ERROR DETECTOR SYSTEM

A Python-based desktop application designed to assist in reviewing General Ledger records and identifying potential errors and inconsistencies.

## FEATURES

- Missing and invalid date detection
- Missing account title detection
- Invalid debit and credit values
- Negative amount detection
- Possible duplicate transaction detection
- Account title validation against a registered Chart of Accounts
- Overall debit and credit balance checking
- Excel audit report export

## TECHNOLOGIES USED

- Python
- Pandas
- OpenPyXL
- CustomTkinter
- Tkinter

## INSTALLATION

Install the required packages:

```bash
pip install -r requirements.txt
```

## HOW TO RUN

```bash
python gl_error_detector.py
```

## PROJECT FILES

- gl_error_detector.py – Main application
- sample_gl.xlsx – Sample General Ledger data
- Chart of Accounts.xlsx – Sample Chart of Accounts
- requirements.txt – Required Python packages

## DISCLAIMER

This project is intended as an accounting review assistance tool. Its findings require proper accounting review and professional judgment.
