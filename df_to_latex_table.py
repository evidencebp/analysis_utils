import numbers
import pandas as pd

def df_to_latex_table(df: pd.DataFrame
                      , caption : str = ''
                      , columns_to_name : dict = None
                      , hline=True
                      , rounding_digits=2):
    numbers_format = '{:,.' + str(rounding_digits) + 'f}'

    print(r"\begin {table}[h!]\centering")
    print(r"\caption{", caption, "}")
    if hline:
        print(r"\begin{tabular}{", "| l"*len(df.columns), " | }")
        print(r"\hline")
    else:
        print(r"\begin{tabular}{", "l"*len(df.columns), "}")
    if columns_to_name:
        first = True
        for c in df.columns:
            if not first:
                print(" & ", end='')
            print(columns_to_name.get(c, c), end='')
            first = False

        if hline:
            print(r"\\ \hline")
        else:
            print(r"\\")

    else:
        print(" & ".join(df.columns), r"\\")

    for _, i in df.iterrows():
        first = True
        for c in df.columns:
            if not first:
                print(" & ", end='')
            if isinstance(i[c], numbers.Number):
                print(numbers_format.format(i[c]), end='')
            else:
                print(i[c], end='')
            first = False
        if hline:
            print(r"\\ \hline")
        else:
            print(r"\\")

    print(r"\end{tabular}")
    print(r"\end{table}")

