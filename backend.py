import pdfplumber
import re
import pandas as pd

def extract_details(narration):
    pattern = r'-\s*To\s*([\w\s]+)$'
    match = re.search(pattern, narration, flags=re.MULTILINE)
    if match:
        result = match.group(1)
        result = result.replace('\n', ' ')
        return result
    else:
        return narration

def extract_data_from_pdf(pdf_path, password):
    tables = []
    with pdfplumber.open(pdf_path, password=password) as pdf:
        tables = [page.extract_tables() for page in pdf.pages]
    cols = tables[0][0][0]
    x_values = [row for row in tables[0][0][2:]]
    z_values = [z for table in tables[1:] for row in table for z in row]
    df = pd.DataFrame(x_values + z_values, columns=cols)
    df.drop(columns=['Cheque No', 'Value Date'], inplace=True)
    c_cols = ['Withdrawal', 'Deposit', 'Balance']
    for i in c_cols:
        df[i] = df[i].str.replace(',', '')
        df[i] = pd.to_numeric(df[i], errors='coerce')
    debit_df = df[(df['Withdrawal'] > 0) & (df['Deposit'] == 0)].copy()
    debit_df.drop(columns=['Deposit'], inplace=True)
    debit_df.reset_index(drop=True, inplace=True)
    for i, row in debit_df.iterrows():
        debit_df.at[i, 'Narration'] = extract_details(row['Narration'])
    total_summary = {
    'Total Credit': df['Deposit'].sum(),
    'Total Debit': df['Withdrawal'].sum(),
    'Total Transactions': len(df),
    'Total Credit Transactions': (df['Deposit'] > 0).sum(),
    'Total Debit Transactions': (df['Withdrawal'] > 0).sum()}
    return debit_df, total_summary