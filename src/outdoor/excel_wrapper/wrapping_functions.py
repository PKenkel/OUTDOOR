# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:15:15 2020

@author: Celina
"""

import pandas as pd


#Funktionen:


def read_type1(df, Col1, Col2):
    
    """
    Description 
    -----------
    There is an Dataframe with different coloumns 
    function read TWO specific columns and add the value in an dict 
    
    Context 
    ----------
    is called in wrapp_ReactionData1, wrapp_EconomicData
    
    Parameters
    ----------
    df : Dataframe
    Col1 : Integer
        Column number 1
    Col2 : Integer
        Column number 2

    Returns
    -------
    dict1 : Python dictionary
    Returns Python dictionary with one time indexed value

    """

    dict1 = {}

    for x in range(len(df)):
       if  pd.isna(df.iloc[x,Col2]) == False :
           dict1[df.iloc[x,Col1]] = df.iloc[x,Col2]
           

    return dict1


def read_type2(df, Col1, Col2, Col3) :
    
    """
    Description 
    -----------
    There is an Dataframe with different coloumns 
    function read THREE specific columns and add the values in an (Twice-indexed)-dict
    
    Context 
    ----------
    ist called in wrapp_ReactionData2, wrapp_BalanceData
    
    Parameters
    ----------
    df : Dataframe

    Col1 : Integer
        Column number 1
    Col2 : Integer
        Column number 2
    Col3 : Integer
        Column number 3

    
    Returns
    -------
    dt : Python dictionary
        Dictionary with value of two times indexed variable

    """

    dict1 = {}

    for x in range(len(df)):
        if  pd.isna(df.iloc[x,Col3]) == False :
            dict1[df.iloc[x,Col1], df.iloc[x,Col2]] = df.iloc[x,Col3]

    return dict1



def read_list(df, Col1, *args):
    """
    Description 
    -----------
    There is an Dataframe with different coloumns 
    function read ONE specific column and add the values in a list  
    
    Context 
    ----------
    ist called in wrapp_EnergyData
    
    Parameters
    ----------
    df : Dataframe

    Col1 : Integer
        Column number 1

    Context 
    ----------
    
    Returns
    -------
    liste: Python List with entries of components or sth else

    """

    pylist = []

    for x in range(*args, len(df)):
        if  pd.isna(df.iloc[x,Col1]) == False :
            pylist.append(df.iloc[x,Col1])


    return pylist


def read_list_new(df, Col, Start=0, End=None):
    
    if End == None:
        End = len(df)
    else:
        End = End
        
        
    pylist = list()
    
    for i in range(Start, End):
        if not pd.isnull(df.iloc[i,Col]):
            pylist.append(df.iloc[i,Col])
            
    return pylist
            
            
            
            





def convert_letters(Letter): 
    """
    Description 
    -----------
    Input_Letters are convert to their ord-Number minus  64 
    
    Parameters
    ----------
    Letter : String "A", "B" etc. 

    Context 
    ----------
    is called in wrapp_ProcessUnits and wrapp_SystemData   
    
    Returns
    -------
    Number : Integer   

    """
    Number = ord(Letter) - 64
    return Number

def convert_letters2(Letter): 
    Number = ord(Letter) - 64 + 26
    return Number

def convert_numbers (number):
    """
    Description 
    -----------    
    Input_Integer-2 = Output_Integer 
    
    Parameters
    ----------
    number : Integer
       
    Context 
    ---------- 
    is called in wrapp_ProcessUnits and wrapp_SystemData 
    
    
    Returns
    -------
    number : Integer
        
    """
    number = number-2
    return number


def convert_total (letter1,number1, letter2, number2):
    """
    Description 
    -----------    
    Converting the letter of a column and the number of a line from an exceldata to a range

    Context 
    ----------
    is called in wrapp_ProcessUnits and wrapp_SystemData 
    
    Parameters
    ----------
    letter1 : String,  "A", "B" etc. 
    number1 : Integer
    letter2 : String,  "A", "B" etc.
    number2 : Integer
        
    
    Returns
    -------
    None.

    """
    Range = range (convert_numbers(number1), convert_numbers(number2)+1), range(convert_letters(letter1)-1, convert_letters(letter2))
    return(Range)


def convert_total2 (letter1,number1, letter2, number2):
        Range = range (convert_numbers(number1), convert_numbers(number2)+1), range(convert_letters2(letter1)-1, convert_letters2(letter2))
        return(Range)





