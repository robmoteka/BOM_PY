import xml.etree.ElementTree as Xet 
import pandas as pd 


#asm_ to tabela złorzeń asm.par brana z ProductRevisionView 
# mach_name - nazwa maszyny brana z id= thisAsm
asm_cols = ["is_asm", "maszyna", "asm_name", "name", "biblioteka", "par_per_asm"]
# zerujemy wiersze na starcie
asm_rows = []

#parsing xml
# <ProductDef> - maszyna 
# -<InstanceGraph> - zbiorczy  
# --<Instance/> - powołanie (par i asm)  
# --<ProductRevisionView/> - wywołanie assembly z listą składowych w instanceRefs (lista)
# -</InstanceGraph>
# --<ProductRevisionView/> - solidy definicje
# --<ProductView> - id i primaryOccurenceRef=jakiesid nie znalazłem powiązania 
# ---<Occurence/> - id, nazwa (z par/psm/asm i :1 wystąpieniem), instanceRef (ścieżka?)
# --<ProductView/>
# <ProductDef/>

#fname - trzeba to sparametryzować
fname = "032P_00.00.00.000_Przenosnik_rolkowo_lancuchowy.plmxml"
# xmlparse - cała struktura s
xmlparse = Xet.parse(fname)
# po diabła ten root?
root = xmlparse.getroot()

# mapujemy strukturę InstanceGraph do obiektu maszyna 
maszyna = xmlparse.find('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductDef/{http://www.plmxml.org/Schemas/PLMXMLSchema}InstanceGraph')

# przyporządkowanie struktur do list obiektów 
skladowe = list(maszyna.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}Instance'))
referencje = list(maszyna.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))

struktura = []

for i in maszyna:
    print(i[0])