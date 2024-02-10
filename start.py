import xml.etree.ElementTree as Xet 
import pyarrow as pa
import pandas as pd 
import csv
from IPython.display import display


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
rewizje_igraf = list(igraf.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))
rewizje_pdef = list(pdef.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))
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
    #if ("visible" in i.attrib) or not("name" in i.attrib): # żeby nie sypało błędami jakby z jakiegoś powodu nie było ustawione
        #if not("visible" in i.attrib) or i.attrib["visible"] != "false"    : #jest widoczny (jak nie to olewam go)
    id = i.attrib["id"] # id rozpatrywanego elementu
    ################# ANALIZA ZŁOŻENIA #######################
    if ("occurrenceRefs" in i.attrib): # jest zlożeniem                
        refs_list = list(i.attrib["occurrenceRefs"].split(" ")) #tymczasowa lista childrenów                
        if ("name" in i.attrib): #przypisanie nazwy zlozenia jeżeli ma name
            asm_name = i.attrib["name"].rsplit('.',1)[0] #czyszczenie rozszerzenia pliku i nr wystąpienia - .asm: 4
        else: #przypisanie nazwy zlozenia (id maszyny) dla root-a
            asm_name = maszyna
        # iteracja po liście składowych 
        # id to nr składowej                
        for p in refs_list: #asm_cols =  ["par_id", "mach_id", "asm_id", "asm_name", "par_name" ]
            asm_rows.append({"par_id": p , "mach_id": mach_id, "asm_id": id, "asm_name": asm_name, "ile": 1})

    ################# ANALIZA ELEMENTÓW #######################
    else: # nie jest zlozeniem
        par_rows.append({"id": id ,"name": i.attrib["name"].rsplit('.',1)[0]})

    ile = ile + 1
print("Przebadano: " + str(ile) + " rekordów.")
print("Zapisano: " + str(len(asm_rows)) + " części zadeklarowanych w złożeniach.")
print("Zapisano: " + str(len(par_rows)) + " części.")

######## PO INSTANCJACH ######################
"""<ProductDef> - maszyna 
-<InstanceGraph> - zbiorczy  
--<Instance/> - powołanie (par i asm)  
--<ProductRevisionView/> - wywołanie assembly z listą składowych w instanceRefs (lista)
-</InstanceGraph>
-<ProductRevisionView/> - solidy definicje
instancje = list(igraf.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}Instance'))
rewizje_igraf = list(igraf.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))
rewizje_pdef = list(pdef.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))
"""
rew_col = ["machine", "name", "is_asm"]
rew_rows = []
for p in rewizje_pdef:
    is_asm = 0 if p.attrib["type"] == "solid" else 1
    name = p.attrib["name"]
    rew_rows.append({"machine": mach_id, "name": name, "is_asm": is_asm})
for rg in rewizje_igraf:
    is_asm = 0 if rg.attrib["type"] == "solid" else 1
    name = rg.attrib["name"]
    rew_rows.append({"machine": mach_id, "name": name, "is_asm": is_asm})



# biblioteka -  pojedyncze wystąpienia asm i par
# index, machine, name, is_asm
biblioteka_df = pd.DataFrame(rew_rows, columns=rew_col, index=None).drop_duplicates()

# assemblies - lista z powtórzeniami
# asm_id to id nadtrzędnego zlożenia
# par_id to id rekordu
# index, mach_id, asm_id, asm_name, par_id, ile
asm_df = pd.DataFrame(asm_rows, columns=asm_cols, index=None) 

# parts - lista części z powtórzeniami
# index, id, name
par_df = pd.DataFrame(par_rows, columns=par_cols, index=None) 

# asm2par_df to przeróbka asm_df do zgodności z par_df
# następnie łącze je razem w jedną tabelę par_asm_df
asm2par_df = asm_df[['asm_id', 'asm_name']].rename(columns={'asm_id': 'id', 'asm_name': 'name'}).drop_duplicates(subset=['id'])
par_asm_df = pd.concat([asm2par_df, par_df])

#paruję asm_df z par_df  
join_df = asm_df.join(par_asm_df.set_index('id'), on='par_id').rename(columns={'mach_id': 'maszyna', 'asm_name': 'zespol', 'par_name': 'name', 'ile': 'ilosc'})
join_df['zespol'] = join_df['zespol'] + '_' + join_df['asm_id']
join_df['biblioteka'] = join_df['name']
#asm_f_uq = asm_df.drop_duplicates(subset=['asm_id'])

#tutaj co robię strasznie na około ale nie chciał mi się join robić
#asm_f_uqu = asm_f_uq[["par_id", "asm_name"]].
display(join_df)


biblioteka_df.to_csv(mach_id + "_biblioteka.csv")
#asm_df.to_csv(mach_id + '_asm_df.csv')
#par_df.to_csv(mach_id + '_par_df.csv')
#asm2par_df.to_csv(mach_id + '_asm2par_df.csv')
#par_asm_df.to_csv(mach_id + '_par_asm_df.csv')
join_df.to_csv(mach_id + '_BOM.csv', index=False, quotechar='"',
                       quoting=csv.QUOTE_NONNUMERIC)

#mrg_f_full.to_csv(mach_id + '_asm+par_mrg_asm.csv')



