import xml.etree.ElementTree as Xet 
import pyarrow as pa
import pandas as pd 


""" asm_ to tabela złorzeń brana z Occurence
"""
asm_cols = ["mach_id", "asm_id", "asm_name", "par_id", "ile"]
asm_rows = []

# biblioteka chyba ciurkiem z Instance
par_cols = ["id", "name"]
par_rows = []

"""parsing xml
<ProductDef> - maszyna 
-<InstanceGraph> - zbiorczy  
--<Instance/> - powołanie (par i asm)  
--<ProductRevisionView/> - wywołanie assembly z listą składowych w instanceRefs (lista)
-</InstanceGraph>
-<ProductRevisionView/> - solidy definicje
-<ProductView> - id i primaryOccurenceRef=jakiesid nie znalazłem powiązania 
--<Occurence/> - id, nazwa (z par/psm/asm i :1 wystąpieniem), instanceRef (ścieżka?)
-<ProductView/>
<ProductDef/>
"""
#fname - trzeba to sparametryzować
fname = "032P_00.00.00.000_Przenosnik_rolkowo_lancuchowy.plmxml"
# xmlparse - cała struktura
xmlparse = Xet.parse(fname)
# po diabła ten root?
root = xmlparse.getroot()

# mapujemy strukturę InstanceGraph do obiektu maszyna 
pdef = xmlparse.find('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductDef')
igraf = xmlparse.find('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductDef/{http://www.plmxml.org/Schemas/PLMXMLSchema}InstanceGraph')
pview = xmlparse.find('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductDef/{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductView')

# przyporządkowanie struktur do list obiektów 
instancje = list(igraf.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}Instance'))
assemblies = list(igraf.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))
solidy = list(pdef.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))
occurence = list(pview.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}Occurrence'))
struktura = []

""" testowana logika
biorę jako bazę occurrence
pomijam te z visible = false 
jeżeli ma occurrenceRefs to jest złożeniem 
occ..R zawiera wszystkie składowe
"""

maszyna = pdef.attrib["name"]
mach_id = maszyna.split("_")[0]

################# PO OCCURENSACH ###########################
ile = 0
for i in occurence:
    if ("visible" in i.attrib) or not("name" in i.attrib): # żeby nie sypało błędami jakby z jakiegoś powodu nie było ustawione
        if not("visible" in i.attrib) or i.attrib["visible"] != "false"    : #jest widoczny (jak nie to olewam go)
            id = i.attrib["id"] # id rozpatrywanego elementu
            ################# ANALIZA ZŁOŻENIA #######################
            if ("occurrenceRefs" in i.attrib): # jest zlożeniem                
                refs_list = list(i.attrib["occurrenceRefs"].split(" ")) #tymczasowa lista childrenów                
                if ("name" in i.attrib): #przypisanie nazwy zlozenia jeżeli ma name
                   asm_name = i.attrib["name"].rsplit('.',1)[0] #czyszczenie rozszerzenia pliku i nr wystąpienia - .asm: 4
                   print(asm_name)
                else: #przypisanie nazwy zlozenia (id maszyny) dla root-a
                   asm_name = maszyna
                   print(asm_name)
                # iteracja po liście składowych 
                # id to nr składowej                
                for p in refs_list: #asm_cols =  ["par_id", "mach_id", "asm_id", "asm_name", "par_name" ]
                    asm_rows.append({"par_id": p , "mach_id": mach_id, "asm_id": id, "asm_name": asm_name})

            ################# ANALIZA ELEMENTÓW #######################
            else: # nie jest zlozeniem
                par_rows.append({"id": id ,"name": i.attrib["name"].rsplit('.',1)[0]})

    ile = ile + 1
print("Przebadano: " + str(ile) + " rekordów.")
print("Zapisano: " + str(len(asm_rows)) + " części zadeklarowanych w złożeniach.")
print("Zapisano: " + str(len(par_rows)) + " części.")

######## PO INSTANCJACH I PRV ######################
"""<ProductDef> - maszyna 
-<InstanceGraph> - zbiorczy  
--<Instance/> - powołanie (par i asm)  
--<ProductRevisionView/> - wywołanie assembly z listą składowych w instanceRefs (lista)
-</InstanceGraph>
-<ProductRevisionView/> - solidy definicje
instancje = list(igraf.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}Instance'))
assemblies = list(igraf.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))
solidy 
"""
inst_col = []
inst_rows = []
for p in instancje:
    is_asm = 0 if i.attrib["type"] == "solid" else 1
    


asm_f = pd.DataFrame(asm_rows, columns=asm_cols, index=None)
#asmg_f = asm_f.groupby(['asm_id'])
asm_f.to_csv("occur_asm_" + fname + '_asm.csv')
par_f = pd.DataFrame(par_rows, columns=par_cols, index=None)
par_f.to_csv("occur_par_" + fname + '_par.csv')

df1 = asm_f.merge(par_f, left_on="par_id", right_on="id")
df1.to_csv(fname + '_mrg.csv')