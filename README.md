# Portfolio-Optimization-Using-NSGA2-with-Python
See more information about specific algorithm and problem, you can click
<br>
<br>
## Notification
Because of the research issues, `mutation.py`, `crossover`,`repair.py` will not be upload to the Github for the moment, you can design its by yourself and there enormous documents which can instrust you.
<br>
<br>
## Row Data
the `rowData` file save all the row data. Specifically, those data include all the daily transaction data for 12 chinese stock bwteen 2014 to 2016. the data are derived from the Straight Flush software.
<br>
<br>
## Code
`dataProcessing.py`: Process row data set and output result.<br>
`NSGA2Selection.py`: Describe and realize NSGA-Ⅱ algorithm using for portfolio optimization problem.<br>
`multiObjectiveGA.py`:Main module to realize GA loop.<br>
`tools.py`:Save some tool functions.<br>
<br>
## Usage
After adding `mutation.py`,`crossover.py` and `repair.py` appropriately, you can run `multiObjcetive.py` module to excute GA loop. Of course, you can change the parameters to the see whether there has any difference.
