from tools.imports import *

def find_most_common(col: pd.Series, name_col: str) -> Optional[list]: 
    """
    Finds the most common value(s) in a given pandas Series and prints the result(s).

    Args:
        (pd.Series) col - pandas Series representing the column for which the most common value(s) is to be found
        (str) name_col - a descriptive name of the column being analyzed, used in the printed output
     
    Returns:
        ([list]) - A list of the most common values.
    """
    if col.empty:
        raise ValueError(f"The pandas Series should not be empty")
    # Create a list of most commun value(s) in col
    most_common = col.mode().tolist()
    # Print and return the list of most common value(s)
    if len(most_common) > 1:
        print(f"Most commons {name_col} are: {most_common[0]}", end='')
        for ite in most_common[1:]: 
            print(f", {ite}")
        most_common = sorted(most_common)
    else:
        print(f"The most common {name_col} is {most_common[0]}")
    return most_common