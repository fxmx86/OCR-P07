# Data manipulation libraries
import pandas as pd
import numpy as np

# Data visualization libraries
import matplotlib.pyplot as plt
import plotly.express as pex

# Custom functions
import functionsPlot as fx_functions_plot
import functionsPCA as fx_functions_pca


# Defining a function to save/restore dataframes in/from the zip file FileZip. Dataframes contains the dataframes list.
import os.path, zipfile, tarfile

def zip_save_restore(FileZip: str, Dataframes: list[str]=[], Format: str="pickle", *args, **kwargs) -> list:
    """ Depending on the zip file existence, this function will :
        - save all listed dataframes in a small zip file, if not already done.
        - restore inexistent dataframes from pickle/CSV files in zip file, with *args, **kwargs if available.
        ** More work to be done to get rid of globals(), with dataframes in a dataframe ? **
    """
    
    if not os.path.isfile(FileZip):
        with zipfile.ZipFile(FileZip, mode="w", compression=zipfile.ZIP_BZIP2) as zip:
            for df in Dataframes:
                if Format == "pickle" : df2 = df; globals()[df].to_pickle(df2)
                if Format != "pickle" : Format = "CSV"; df2 = df + ".csv"; globals()[df].to_csv(df2)
                zip.write(df2); os.remove(df2); print (df + " : df saved (" + Format + ")")
        return Dataframes

    else:
        dfs = []
        with zipfile.ZipFile(FileZip, mode="r") as zip:
            for file in zip.infolist():
                file = file.filename; fileok = file.replace(".csv", "").replace(".", "")
                msg = "df already exist or not in listed Dataframes"

                if fileok not in globals() and (Dataframes == [] or fileok in Dataframes):
                    if file.find(".csv") >= 0 or Format != "pickle" :
                        msg = "(CSV W global params, if existent)"
                        try:
                            args1 = fileok + "_args"; kwargs1 = fileok + "_kwargs"
                            if args1 in globals() and kwargs1 in globals():
                                msg = "(CSV W unique params)"
                                globals()[fileok] = pd.read_csv(zip.open(file), *globals()[args1], **globals()[kwargs1])
                            else:
                                globals()[fileok] = pd.read_csv(zip.open(file), *args, **kwargs)
                        except Exception as ex:
                            print('ERROR : ', ex); msg = "or not (ERROR above !)"

                    else :
                        msg = "(pickle)"; globals()[fileok] = pd.read_pickle(zip.open(file), *args, **kwargs).sort_index()
                    msg = "df restored " + msg
                dfs.append(fileok); print (fileok + " : " + msg)
        return dfs

# Modif