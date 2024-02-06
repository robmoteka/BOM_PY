import xml.etree.ElementTree as Xet 
import pyarrow as pa
import pandas as pd 


""" asm_ to tabela złorzeń i części brana z Occurence
asm_name to nazwa nadrzędnego zlożenia (jak główne to null)
name to nazwa zlozenia lub czesci bez suffixu
is_asm to dodatkowe info że to zlozenie
"""
asm_cols = ["maszyna", "parent_name", "name", "biblioteka",  ]
asm_rows = []

# biblioteka chyba ciurkiem z Instance
lib_cols = []
lib_rows = []

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


count = 0
for i in occurence:
    if ("visible" in i.attrib):
        # czy jest widoczny jeżeli nie to nie ma go
        if i.attrib["visible"] != "false" :
            # jest zlożeniem
            if ("occurrenceRefs" in i.attrib):
               print("do nothing")


    count = count + 1
print(count)