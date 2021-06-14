import numpy as np


def capex_calculator(UnitProcess, CECPI, Detail=None):
    """

    Parameters
    ----------
    UnitProcess : Process - Class
        An Object of Type Process i handed to the function
        
    CECPI : Float / Int
        The CECPI for the Process_Unit of the depicted year of the simulation
    
    Detail : String, optional
        Can either be "average", "rough" or "fine", if nothing i selected "average"
        is the default.
        This String decides on how many linearization points for th piece-wise lin.
        of the Unit Capex are defined.
        
        
    Description
    ------------
    
    This function takes a Process Unit and the CECPI of the regarded year, 
    and calculates a piece-wise linear function of the Equipment Costs of the Process
    based on the non-linear function saved in the process itself.
    It returns the piece-wise lin. Function pieces.
        
    


    Returns
    -------
    x_vals : Dictionary
        Returns the x_vals (Reference Flows) of the piece-wise linearization of the
        non-linear CAPEX function:
            
        Example: x_vals = {'lin_CAPEX_x': {(ProcessUnit,points) : Value}}

    y_vals : Dictionary
        Returns the y_vals (Equiptment Costs) of the piece-wise linearization of the
        non-linear CAPEX function:
            
        Example:     Same as x_vals.

    """
    
    
    ProcessNumber = UnitProcess.Number
    M_REF = UnitProcess.CAPEX_factors['m_Ref'][ProcessNumber]
    C_REF =  UnitProcess.CAPEX_factors['C_Ref'][ProcessNumber]
    F_REF = UnitProcess.CAPEX_factors['f'][ProcessNumber]
    CECPI_REF = UnitProcess.CAPEX_factors['CECPI_ref'][ProcessNumber]
    CECPI = CECPI['CECPI']
    
    
    x_vals = {'lin_CAPEX_x' : {}}
    y_vals = {'lin_CAPEX_y': {}}
    
 
    if Detail == "rough":
        intervals = 9
    elif Detail == "fine":
        intervals = 300
    else:
        intervals = 19
    
    points = intervals +1
    real_points = (points - 3) / 2
    M= np.zeros([points,4])
    j = 0
    j2 = 2
    
    M[0,0] = 1
    M[0,1] = 0
    M[0,2] = 0
    M[0,3] = 0
    
    x_vals['lin_CAPEX_x'][ProcessNumber ,1] = 0
    y_vals['lin_CAPEX_y'][ProcessNumber ,1] = 0
    

    
    M[points-1,0] = points 
    M[points-1,1] = 1000000
    M[points-1,2] = 1000000
    M[points-1,3] = C_REF * (M[intervals,2]/M_REF)**F_REF * (CECPI/CECPI_REF)
    
    

    
    for i in range(1,points-1):
        M[i,0] = i+1
        if j < real_points:      
            M[i,1] = 1/(real_points + 1-j) 
            M[i,2] = 1/(real_points + 1-j) * M_REF    
        elif j == real_points:
            M[i,1] = 1 
            M[i,2] = M_REF
        else:
            M[i,1] = 1 * j2  
            M[i,2] = 1 * j2 *M_REF  
            j2 += 1
        j += 1
        M[i,3] = C_REF * (M[i,2]/M_REF)**F_REF * (CECPI/CECPI_REF)
        x_vals['lin_CAPEX_x'][ProcessNumber ,i+1] = M[i,2]
        y_vals['lin_CAPEX_y'][ProcessNumber ,i+1] = M[i,3] 


    x_vals['lin_CAPEX_x'][ProcessNumber ,points] = 1000000
    y_vals['lin_CAPEX_y'][ProcessNumber ,points] = M[points-1,3]   



    return (x_vals, y_vals)

    




