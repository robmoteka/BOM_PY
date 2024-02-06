import xml.etree.ElementTree as Xet 
import pandas as pd 


#asm_ to tabela złorzeń asm.par brana z ProductRevisionView 
# mach_name - nazwa maszyny brana z id= thisAsm
asm_cols = ["is_asm", "maszyna", "asm_name", "name", "biblioteka", "par_per_asm"]
# zerujemy wiersze na starcie
asm_rows = []

#parsing xml
# - ProductDef - maszyna 
# -- InstanceGraph - zbiorczy 
# --- Instance - powołanie wystąpień z definicji (jn) 
# --- ProductRevisionView - definicje w 2 wersjach solid i assembly
# -- ProductView - 
# --- Occurence - wystąpienia definicji

# xmlparse - cała struktura
fname = "036P_00.00.00.000_Przenosnik_lancuchowy.plmxml"
xmlparse = Xet.parse(fname)
# po diabła ten root?
root = xmlparse.getroot()

# mapujemy strukturę InstanceGraph do obiektu maszyna 
maszyna = xmlparse.find('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductDef/{http://www.plmxml.org/Schemas/PLMXMLSchema}InstanceGraph')

# przyporządkowanie struktur do list obiektów 
skladowe = list(maszyna.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}Instance'))
referencje = list(maszyna.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))

struktura = []

def znajdzAsm(nrId):
    for i in referencje:
        if i.attrib['id'] == nrId:
            r_name = i.attrib['name']
            is_asm = 0 if i.attrib["type"] == "solid" else 1
            if is_asm == 0:
                return(r_name, is_asm)
            else:
                 r_list = list(i.attrib["instanceRefs"].split(" ")) #lista składowych
                 for m in r_list


mach_name = 

for i in skladowe:
    if i.attrib["id"] == "thisAsm":
        mach_name = i.attrib["name"]
        split_mach_name = mach_name.split("_")
        el_list = list(i.attrib["instanceRefs"].split(" ")) #tą listę
    for t in el_list:
            
        
        
        #is_asm = 0 if i.attrib["type"] == "solid" else 
       
       
        # asm_rows.append({
        #     "maszyna": split_mach_name[0], 
        #     "asm_name": mach_name,
        #     "name": par_name[0],
        #     "biblioteka": par_name[0],
        #     "par_per_asm": par_per_asm,
        #     "is_asm": is_asm
        # })


# # jadziem z iteracją po listach iiihaaa, patataj, patataj
# for i in referencje: 
#     # "i" złorzenie z nazwą i listą skladowych
#     ref_id = i.attrib["id"] 
#     ref_name = i.attrib["name"]
#     ref_type = i.attrib["type"]
#     # tutaj sobie kradnę nazwę maszyny
#     if ref_id == "thisAsm":
#         mach_name = ref_name.split("_")
    
 

#     #childrens to lista elementów w danym (1) złorzeniu
#     # childrens = [12,123,124] 
#     childrens = list(i.attrib["instanceRefs"].split(" "))
#     for m in childrens:  
#         # m to kolejny element w złorzeniu 
#         for t in skladowe: # szukamy w skladowych odpowiadających m numerów id
#             # t to tablica de facto z nazwą i id do powiązania z m
#             if m == t.attrib["id"]: # znaleziono parkę 
#                par_per_asm = 1
#                par_name = t.attrib["name"].rsplit('.',1) #czyszczenie rozszerzenia pliku i nr wystąpienia - .asm: 4
#                if par_name[1].find('asm') == -1: #sprawdź czy to złorzenie czy nie i wystaw flagę - po co nie wiem jeszcze ale czuję, że się przyda
#                     is_asm = 0
#                else:
#                     is_asm = 1
#         # dokładamy wiersz do tablicy
#         asm_rows.append({"maszyna": mach_name[0]  ,"asm_name": asm_name, "name": par_name[0], "biblioteka": par_name[0], "par_per_asm": par_per_asm, "is_asm": is_asm})


#print(asm_rows)
# for i in skladowe: 
#     name=i.attrib["name"] # to trzeba wyczyścić z .par:12
#     id=i.attrib["id"]
#     ref=i.attrib["partRef"] #ta wartość tylko w tablicy tymczasowej
#     for x in referencje:
#         if x.attrib["id"] == ref[1:]:
#             #print(x.attrib["type"])
#             ref_name = x.attrib["name"]
#             ref_type = x.attrib["type"]
#             if ref_type == "assembly":  
#                 asm = x.attrib["instanceRefs"]
          
#     part_rows.append({"id": id, "name": name,})
    
asm_f = pd.DataFrame(asm_rows, columns=asm_cols, index=None)
asm_f.to_csv(fname + '.csv')