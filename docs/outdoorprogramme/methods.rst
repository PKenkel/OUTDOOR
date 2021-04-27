Method types
=====

The different classes have different methods. These are divided into:
- Public methods
- Private methods

Public methods are written as normal function and are used in different classes and modules or can be used as parameter-setting function. Private methods are written as __ - private functions in python. These methods are either used internally to calculate specific data from raw data or they display detailed parameter setters which are called by public bundle setters.

Methods are ofter labeled with one of the following prescripts:

set_function : A function to set a a parameter necessary for the optimization problem. Detailed setter functions are often declared as private and called from so-called bundle setters

set_xyData : A bundle setter function which takes a bundle of information regarding one aspect of modeling (e.g. economics data of one unit operation) and hands it to the private detailed setters for formatting the data into the right format.

add_function: A function which adds entries to a list, which is later used as Set in the optimization problem (e.g. unit operations)

fill_function : Most often these functions are private, they collect data from unit-operation objects and fill them into a list which is used for formatting.

calc_function: Functions which calculate advanced variables which are derived from the initial data (e.g. annualized capital cost factors for different unit operations)

prepare_function: A higher function which calls lesser functions (calc, fill etc.) in the right order to process all the input data to the final file format (Private)