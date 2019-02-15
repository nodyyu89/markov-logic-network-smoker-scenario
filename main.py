# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 16:30:30 2019

@author: Nody
"""

import os
import sys
from pracmln.utils.project import PRACMLNConfig
from pracmln.utils import config, locs
from pracmln.utils.config import global_config_filename
import os
from pracmln.mlnlearn import MLNLearn
from pracmln import MLN, Database, query

class social_modelling():

    def read_data(paths, predicate):
        content = []
        base_path = os.getcwd()
        file = open(base_path + '\\' + paths,'r',encoding = 'utf8')
        pre_content = file.read()
        pre_content = pre_content.split('###')
        pre_content = [x for x in pre_content if x !='']
        for i in pre_content:
            element = i.split('\n')
            element = [x.replace(':','_') for x in element if x !='']
            for j in element[1::]:
                splited = j.split('(')
                content.append((element[0],splited[0]+'('+splited[1].upper()))
        
            #content.append((element[0],element[1::]))
        
        return content
    
    def read_formula(paths,predicate):
        predicate_list = [x.split('(')[0] for x in predicate]
        predicate_list = predicate_list + ['!'+x for x in predicate_list]
        predicate_list = [' '+x for x in predicate_list]
        predicate_list = [(x.lower(),x) for x in predicate_list]
        exist_list = []
        exist_list2 = []
        formula = []
        base_path = os.getcwd()
        file = open(base_path + '\\' + paths,'r',encoding = 'utf8')
        formula = file.read()
        formula = formula.split('\n')
        formula = [x for x in formula if x !='']
        formula = [' ' +x.replace(' or ',' v ').replace(' and ',' ^ ').replace(':','') for x in formula]
        exist_list = [x for x in formula if 'Exists ' in x]
        formula = ['0 '+x for x in formula if 'Exists ' not in x]
# =============================================================================
#         exist_list = [x.lower() for x in exist_list]
#         for i in exist_list:
#             string = i
#             for j in predicate_list:
#                 string = string.replace(j[0],j[1])
#             string = string.replace(':',' (').replace('exists ','EXIST ')
#             exist_list2.append(string+').')
#         #exist_list = [x.replace('Exists ','EXIST ').replace(':',' (') + ').' for x in exist_list]
#         #print(exist_list)
# =============================================================================
        #print(exist_list2)
        formula = exist_list2 + formula
        #formula = [x.replace('Exists ','EXIST ') + ]
# =============================================================================
#         predicate_list = [x.split('(')[0] for x in predicate]
#         for i in predicate_list:
#             formula = [x.replace(i.lower(),i) for x in formula]
# =============================================================================
        return formula 
    
    def read_predicate(paths):
        predicate = []
        base_path = os.getcwd()
        file = open(base_path + '\\' + paths,'r',encoding = 'utf8')
        predicate = file.read()
        predicate = predicate.split('\n')
        predicate_list = [x.split('(')[0] for x in predicate]
        predicate_list2 = [x.split('(')[1].replace(' ','').lower() for x in predicate]
        predicate = []
        for i in zip(predicate_list,predicate_list2):
            predicate.append(i[0] + '(' + i[1])
        return predicate
        
    
    def model_config(predicate,formula,database):
        mln = MLN(grammar='StandardGrammar',logic='FirstOrderLogic')
        for i in predicate:
            mln << i
            print('input predicate successful:'+i)
        for i in formula:
            mln << i
            print('input formula successful :'+i)
        mln.write()
        db = Database(mln)
        try:
            for i in enumerate(database):
                db << i[1][1]
                print('input database successful : ' + i[1][0] + ' : ' +i[1][1])
        except :
            for j in database[i[0]::]:
                db << j[1]
            
        db.write()
        return (db,mln)
        
    def activate_model(database, mln):
        
        DEFAULT_CONFIG = os.path.join(locs.user_data, global_config_filename)
        conf = PRACMLNConfig(DEFAULT_CONFIG)
        
        config = {}
        config['verbose'] = True
        config['discr_preds'] = 0
        config['db'] = database
        config['mln'] = mln
        config['ignore_zero_weight_formulas'] = 0
        config['ignore_unknown_preds'] = 0
        config['incremental'] = 0
        config['grammar'] = 'StandardGrammar'
        config['logic'] = 'FirstOrderLogic'
        #Other Methods: EnumerationAsk, MC-SAT, WCSPInference, GibbsSampler
        config['method'] = 'BPLL'
        config['multicore'] = 1
        config['profile'] = 0
        config['shuffle'] = 0
        config['prior_mean'] = 0
        config['prior_stdev'] = 5
        config['save'] = 1
        config['use_initial_weights'] = 0
        config['use_prior'] = 0
        conf.update(config)
        
        print('training...')
        learn = MLNLearn(conf, mln=mln, db=database)
        result = learn.run()
        print('finished...')
        return result
    
    def inference(path, result, data, mln):
        query_list = []
        base_path = os.getcwd()
        file = open(base_path + '\\' + path,'r',encoding = 'utf8')
        query_list = file.read()
        query_list = query_list.split('\n')
        query_list = [x for x in query_list if x !='']
        for i in query_list:
            print(query(queries=i, method='MC-SAT', mln=mln, db=data, verbose=False, multicore=True).run().results)




if __name__ == '__main__':

    predicate = social_modelling.read_predicate('predicate.txt')
    formula = social_modelling.read_formula('formula.txt',predicate)
    database = social_modelling.read_data('data.txt', predicate)
    data,mln = social_modelling.model_config(predicate,formula,database)
    output = social_modelling.activate_model(data,mln)
    inference = social_modelling.inference('inference.txt', output, data, mln)
# missing arguement
            
#query(queries='Cancer(x)', method='MC-SAT', mln=mln, db=data, verbose=False, multicore=True).run().results





# =============================================================================
#         predicate_list = [(x,x.lower()) for x in predicate_list]
#         predicate = [x.replace(' ','').lower() for x in predicate if x !='']
#         predicate2 = []
#         for i in predicate_list:
#             for j in predicate:
#                 if i[1] in j:
#                    predicate2.append(j.replace(i[1],i[0]))
#         #predicate = [x[0] + x[1:].replace(' ','').lower() for x in predicate if x !='']
#         #predicate = ['0 '+x for x in predicate if x !='']
#  
# =============================================================================
