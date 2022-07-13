import json
from lib2to3.pgen2 import literals
from rdflib import Literal,Namespace,BNode, Graph
from rdflib.namespace import RDF, RDFS

with open('Data/extracted_nx_info/2d_cantilever_analysis/2Dmodel_sim2_ABS.json') as jf:
    jobject = json.load(jf)
    jf.close()

graph = Graph()
def jsontordf(graph,jobject,previous_key='root'):
    intial_keys = jobject.keys()
    # iterate over the primary keys
    for i in intial_keys:
        # check whether the primary keys are giving a list or not
        if isinstance(jobject[i],list):
            # check if list is empty
            if len(jobject[i]):
                # level 1 nested dict: check if the values given by the primary keys is a dict or not 
                if isinstance(jobject[i][0],dict):
                    second_keys = jobject[i][0].keys()
                    # print(second_keys)
                    # iterate over second keys to check whether they are dict or not
                    for s in second_keys:
                        if isinstance(jobject[i][0][s],list):
                            # check if list is empty
                            if len(jobject[i][0][s]):
                                # level 2 of nested dicts
                                if isinstance(jobject[i][0][s][0],dict):
                                    # we have 3 levels of nested dict therefore use recursion
                                    # print('Recursion 1-1',jobject[i][0][s][0])
                                    keys = jobject[i][0][s][0].keys()
                                    for rkey in keys:
                                        graph.add((Literal(s),RDF.type,Literal(rkey)))
                                    jsontordf(graph,jobject[i][0][s][0],s)
                                else:
                                    # print(f'I found a list object {jobject[i][0][s][0]}')
                                    for ele2 in jobject[i][0][s]:
                                        graph.add((Literal(i),Literal(s),Literal(ele2)))
                            else:
                                print('list is empty2')
                                graph.add((Literal(i),Literal(s),RDF.nil))
                        else:
                            # level 2 of nested dicts
                            if isinstance(jobject[i][0][s],dict):
                                # we have 3 levels of nested dict therefore use recursion
                                # print('Recursion 1-2',jobject[i][0][s])
                                keys = jobject[i][0][s].keys()
                                for rkey in keys:
                                    graph.add((Literal(s),RDF.type,Literal(rkey)))
                                jsontordf(graph,jobject[i][0][s],s)
                            else:
                                # print(f'I found a non list object {jobject[i][0][s]}')
                                graph.add((Literal(i),Literal(s),Literal(jobject[i][0][s])))
                else:
                    # print(f'object is a list but not a dict: {jobject[i][0]}')
                    for ele2 in jobject[i]:
                        graph.add((Literal(previous_key),Literal(i),Literal(ele2)))
            else:
                print('list is empty1')
                graph.add((Literal(previous_key),Literal(i),RDF.nil))
        else:
            # level 1 nested dict: check if the values given by the primary keys is a dict or not 
            if isinstance(jobject[i],dict):
                second_keys = jobject[i].keys()
                # print(second_keys)
                # iterate over second keys to check whether they are dict or not
                for s in second_keys:
                    if isinstance(jobject[i][s],list):
                        # check if list is empty
                        if len(jobject[i][s]):
                            # level 2 of nested dicts
                            if isinstance(jobject[i][s][0],dict):
                                # we have 3 levels of nested dict therefore use recursion
                                # print('Recursion 2-1',jobject[i][s][0])
                                keys = jobject[i][s][0].keys()
                                for rkey in keys:
                                    graph.add((Literal(s),RDF.type,Literal(rkey)))
                                jsontordf(graph,jobject[i][s][0],s)
                            else:
                                # print(f'I found a 2nd list object {jobject[i][s]}')
                                for ele in jobject[i][s]:
                                    graph.add((Literal(i),Literal(s),Literal(ele)))
                        else:
                            print('list is empty 3')
                            graph.add((Literal(i),Literal(s),RDF.nil))
                    else:
                        # level 2 of nested dicts
                        if isinstance(jobject[i][s],dict):
                            # we have 3 levels of nested dict therefore use recursion
                            # print('Recursion 2-2',jobject[i][s])
                            keys = jobject[i][s].keys()
                            for rkey in keys:
                                graph.add((Literal(s),RDF.type,Literal(rkey)))
                            jsontordf(graph,jobject[i][s],s)
                        else:
                            # print(f'I found a 2nd non list object {jobject[i][s]}')
                            graph.add((Literal(i),Literal(s),Literal(jobject[i][s])))
            else:
                # print(f'object is neither a list nor a dict: {jobject[i]}')
                graph.add((Literal(previous_key),Literal(i),Literal(jobject[i])))

jsontordf(graph,jobject)

print(graph.serialize(format='ttl'))
graph.serialize(destination="tbl3.ttl")