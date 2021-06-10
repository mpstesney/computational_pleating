"""
Save input string as .FOLD file in local directory...

filePath parsing from:
https://www.grasshopper3d.com/forum/topics/
suggestion-improve-text?xg_source=activity&id=2985220%3ATopic%3A152075&
page=2#comments
"""

__author__ = "mpste"
__version__ = "2020.04.03"

# write data to .FOLD file
if write:
    # get filepath to current folder
    docPath = ghenv.LocalScope.ghdoc.Path
    docName = ghenv.LocalScope.ghdoc.Name
    path = docPath.replace(".gh","*")
    path = path.replace(docName,"")
    
    # add new file name to filepath
    path += filename + ".fold"

    with open(path, "wt") as f:
        f.write(data)