
def calculate_sensitiveParameters(Superstructure):
    
    value_dic = {}
    
    def calc_points(tuple_):
        start = tuple_[1] 
        end = tuple_[2] 
        points = tuple_[3] 
        dx = (end-start)/(points-1)
        list_ = []

        for i in range(points):
            xx = dx*i + start  
            list_.append(xx)
        
        return list_

    for i in Superstructure.sensitive_parameters:
        if len(i) == 4:
            value_dic[i[0]] = calc_points(i)
        elif len(i) == 5:
            try: 
                value_dic[i[0]][i[4]] = calc_points(i)
            except:      
                value_dic[i[0]] = {}
                value_dic[i[0]][i[4]] = calc_points(i)
            

    return value_dic







def prepare_mutableParameters(ModelInstance, Superstructure):

    
    def set_mutable(instance, parameter):
        if parameter == 'electricity_price' or parameter == 'chilling_price':
            instance.delta_ut._mutable = True
        elif parameter == 'working_hours':
            instance.flh._mutable = True
        elif parameter == 'capital_costs' or parameter == 'simple_capex':
            instance.lin_CAPEX_x._mutable = True
            instance.lin_CAPEX_y._mutable = True
        elif parameter == 'component_concentration':
            instance.conc._mutable = True
        elif parameter == 'heating_demand':
            instance.tau_h._mutable = True
            instance.tau_c._mutable = True
        elif parameter == 'source_costs':
            instance.materialcosts._mutable = True
        elif parameter == 'opex':
            instance.K_OM._mutable = True
        elif parameter == 'product_price':
            instance.ProductPrice._mutable = True
        else:
            raise ValueError('Parameter to set mutable not existing')
        
        
    for i in Superstructure.sensitive_parameters:
        name = i[0]
        set_mutable(ModelInstance,name)