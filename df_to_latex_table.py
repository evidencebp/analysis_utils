import numbers
import pandas as pd

def df_to_latex_table(df: pd.DataFrame
                      , caption : str = ''
                      , columns_to_name : dict = None
                      , hline=True
                      , rounding_digits=2
                      , star_table=False
                      , bold_title=True):
    numbers_format = '{:,.' + str(rounding_digits) + 'f}'

    if star_table:
        print(r"\begin {table*}[h!]\centering")
    else:
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
            if bold_title:
                print(r"\textbf{" + columns_to_name.get(c, c) + "}", end='')
            else:
                print(columns_to_name.get(c, c), end='')
            first = False

        print(r"\\")


    else:
        print(" & ".join(df.columns), r"\\")

    if hline:
        print(r"\hline")

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
    if star_table:
        print(r"\end{table*}")
    else:
        print(r"\end{table}")

