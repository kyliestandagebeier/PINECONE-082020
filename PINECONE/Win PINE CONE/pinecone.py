# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:23:28 2020

@author: Kylie Standage-Beier
"""
import csv #for handling input and output CSVs
import requests #for webpage requests
import json #for loading contents
import time #for timing For-loop API requests
from tkinter import * #For UI
from PIL import ImageTk,Image #For displaying images
from tkinter import filedialog #for file dialog interface
from tkinter import ttk #needed for combo boxes
import os 
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import colors as mcolors
import numpy as np
#########



print("Hello")

root = Tk()
root.title('PINE CONE')
program_logo_path = os.path.join('logos','pineconelogo.ico')
root.iconbitmap(program_logo_path) #logo
root.geometry("500x550") #Size of UI window
#frame = LabelFrame(root, text="Frame", padx=5, pady=5, bg='#f0f0f0')
#frame.grid(row=0, column=0)

"""OPENS CSV INPUT PARAMETERS"""
input_file_path = "aaaaaa"
input_file_path_text = "zzzzz"
parameters = "bbbbbb"
organism = "null"
analysis_button = "null"

"""UI Stuff"""
"""Organism Dropdown menu, selection dictionary defines organism searched"""
def comboclick(event):
    global label2
    global organism
#    myLabel1=Label(root, text=myCombo.get())
#    myLabel1.grid(row=0, column=0)
    
    print(myCombo.get())
    
    label2.grid_forget()
    #dictionary converts text into general term, t be used elsewhere (for more complicated programs)
    selction_dictionary = {'Select Organism':'null',
                           'Manual (.txt)':'text',
                           "Plasmid (.txt)":'plasmid',
                           'Human (hg38)':'hg38', 
                           'Yeast (S288C)':'S288C',
                           'Mouse (mm10)':'mm10',
                           'Rat (rn6)':'rn6',
                           'Zebrafish (danRer11)':'danRer11',
                           'Roundworm (ce11)':'ce11',
                           'Fruitfly (dm6)':'dm6',
                           'Dog (CanFam3)':'CanFam3',
                           'Chimp (panTro6)':'panTro6',
                           'Proboscis monkey':'nasLar1'}
    
    selection_intermediate = selction_dictionary[myCombo.get()] #just an intermediate to translate between dictionaries
    organism = selction_dictionary[myCombo.get()] #organism is name of reference genome as appears in URL
    #dictionary converts selection variable to image name
    organism_icons = {'null':'Query_logo.png', 
                      'hg38':'Human_logo.png', 
                      'S288C':'yeast_logo.png',
                      'mm10':'mouse_logo.png',
                      'text':'manual_text_logo.png',
                      'plasmid':'manual_text_logo.png',
                      'rn6':'rat_logo.png',
                      'danRer11':'zebrafish_logo.png',
                      'ce11':'roundword_logo.png',
                      'dm6':'fruitfly_logo.png',
                      'CanFam3':'dog_logo.png',
                      'panTro6':'chimp_logo.png',
                      'nasLar1':'proboscismonkey_logo.png',}
    
    image_to_display = os.path.join('logos', organism_icons[selection_intermediate])

    if myCombo.get() == "Manual (.txt)":
#        myLabel = Label(root, text = 'select text document').pack()
        my_btn = Button(root, text="Select DNA Sequence (.txt)", command=select_text_file).grid(row=8, column=0) #if manual selected creates file dialog for text input
        #print(myCombo.get())
    elif myCombo.get() == "Plasmid (.txt)":
        my_btn = Button(root, text="Select DNA Sequence (.txt)", command=select_text_file).grid(row=8, column=0)
    else:
        status_label_organism = "Organism: " + myCombo.get()
        #myLabel = Label(root, text = status_label_organism).grid(row=7, column=1, columnspan=3, sticky=W)

    image1 = ImageTk.PhotoImage(Image.open(image_to_display))
    label2 = Label(image=image1)
    label2.image = image1
    label2.grid(row=4, column=0)

"""PE Editing Strategy Radio Buttons Function"""
MODES = [("PE2","PE2_a"),
         ("PE3","PE3_a"),
         ("PE3B","PE3B_a")]

strategy_input = StringVar()
strategy_input.set("PE2_a") #sets default mode


strategy_logo_path = os.path.join('logos','PE2_Logo.png')
image_strategy = ImageTk.PhotoImage(Image.open(strategy_logo_path))
image_label_strategy = Label(image=image_strategy)
image_label_strategy.image = image_strategy
image_label_strategy.grid(row=4, column=1, columnspan=3)



"""Select .CSV file"""
def select_file():
    global input_file_path
    root.filename = filedialog.askopenfilename(initialdir = "/", title="Select File", filetypes = (("csv files", "*.csv"),("all files","*.*")))
    csv_file_name = os.path.basename(root.filename)
    csv_file_display = "Edit File: " + csv_file_name
    my_label = Label(root, text=csv_file_display).grid(row=7, column=0, columnspan=1) #sticky=W
    print (root.filename)
    input_file_path = root.filename

"""If manual input selected, file select for .txt file"""
def select_text_file():
    global input_file_path_text
    root.filename_text = filedialog.askopenfilename(initialdir = "/", title="Select File", filetypes = (("text files", "*.txt"),("all files","*.*")))
    text_file_name = os.path.basename(root.filename_text)
    text_file_display = "DNA Sequence: " + text_file_name
    my_label = Label(root, text=text_file_display).grid(row=9, column=0, columnspan=1)#sticky=W
    input_file_path_text = root.filename_text
    #print(root.filename_text)

"""Main Function, Run button initiates this"""
def run_button():
    global parameters
    global organism
    global output_file_name
    global output_file_name_no_ext
    
    if output_file_entry.get() == "": #Sets default name of output if no output name is entered
        output_file_name_no_ext = "pinecone_output"
        output_file_name = output_file_name_no_ext + ".csv"
    else: #Sets output name to user input
        output_file_name_no_ext = output_file_entry.get()
        output_file_name = output_file_name_no_ext + ".csv"
        
    output_file_status = "'" + output_file_name + "' is complete"
    clicklabel = Label(root, text=output_file_status, fg='green', font=('helvetica', 8, 'bold'))
    clicklabel.grid(row=7, column=1, columnspan=3)
    retrieve_file_path =  input_file_path
    
    with open(retrieve_file_path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        data = [list(row) for row in readCSV]
    print(data)
    parameters = data
        
    """DNA SEQUENCE INPUT (old)"""    
    #DNA = input("Enter DNA Sequence: ").replace(" ", "").upper()
    #Edit_site = int(input("Enter Nucleotide Position of Edit (Bp): "))-1
    #Edit_nucl = input("Enter Desired Nucleotide Edit (A,T,C,G): ").upper()
    #edit_len = int(input("Primer Editing Area Length (def. 10 Bp): "))
    #pbs_len = int(input("Primer Binding Site Length (def. 13 Bp): "))
    cas9_hp = "GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC"
    u6_term = "TTTTTTGTTTT"
    
    """GENERATES DNA REVERSE COMPLEMENT"""
    def dna_rev_comp(DNA):
        dna_a = (DNA.upper().replace(' ',''))  #converts input to uppercase, this is a redundancy
        dna_r = (dna_a[::-1])   #reverse of input DNA
        dna_i = (dna_a.replace("A", "W").replace("T", "X").replace("C", "Y").replace("G", "Z")) #intermediate for making complement
        dna_c = (dna_i.replace("W", "T").replace("X", "A").replace("Y", "G").replace("Z", "C")) #complement
        dna_rc = (dna_c[::-1]) #reverse complement
        return dna_rc, dna_c, dna_r, dna_a #output of function
     
        
    def primer_tm_design(sequence): #enter dna sequence, generates primer with specific Tm, input seq should be 40bp or longer
        tm_set = 63 #Sets goal Tm
        tm = 0 #Starting Tm at begining of For-loop
        #dH is deltaH enthalpy dinucleotide dictionary
        dH = {'AA':-7.9,'TT':-7.9,'AT':-7.2,'TA':-7.2,
              'CA':-8.5,'TG':-8.5,'GT':-8.4,'AC':-8.4,
              'CT':-7.8,'AG':-7.8,'GA':-8.2,'TC':-8.2,
              'CG':-10.6,'GC':-9.8,'GG':-8.0,'CC':-8.0}
        #dS is entropy, -kcal/mol dinucleotide dictionary
        dS = {'AA':-22.6,'TT':-22.6,'AT':-20.4,'TA':-21.3,
              'CA':-22.7,'TG':-22.7,'GT':-22.4,'AC':-22.4,
              'CT':-21.6,'AG':-21.6,'GA':-22.2,'TC':-22.2,
              'CG':-27.2,'GC':-24.4,'GG':-19.9,'CC':-19.9}
                    
        adjust_H = 0.1 
        adjust_S = 2.8
                    
        dH_sum = 0 + adjust_H
        dS_sum = 0 + adjust_S

        for base in range(0,len(sequence)-2):
            dinucleotide = sequence[base:base+2]
            dH_sum += dH[dinucleotide]
            dS_sum += dS[dinucleotide]
            R = 1.987 #universal gas constant 
            M = 500 * 10**-9 #common molarity of primers
            tm_int = ((dH_sum)*1000)/(dS_sum+R*np.log(M))-273.15
            tm = (tm_int +16.6*np.log(1))-15 #15 is adjustment to roughly match values
            if tm >= tm_set: #elongates primer until Tm is reached
                break
        
        primer_seq = sequence[0:base+2] #this is final primer sequence
        #print("Primer legnth: "+ str(len(primer_seq)))
        #print("Primer Seq: " + primer_seq)
        #print("Calculated TM is: " + str(tm))
        
        return primer_seq
    
    """DESIGNS POSITIVE STRAND PEGRNA"""
    def pegrna_top(DNA, Edit_site, Edit_nucl, edit_len_a, pbs_len_a, cas9_hp, u6_term):
        """Determines if user is requesting deletion, defines editing product"""
        if "D" in Edit_nucl: #Determines if user is requesting deletion
            deletion_length = int(Edit_nucl[1:len(Edit_nucl)])
            DNA_l = DNA[0:Edit_site]
            DNA_r = DNA[Edit_site+deletion_length:len(DNA)]  
            DNA_edited = DNA_l + DNA_r
        elif "I" in Edit_nucl:
            integraton = str(Edit_nucl[1:len(Edit_nucl)])
            DNA_l = DNA[0:Edit_site+1]
            DNA_r = DNA[1+Edit_site:len(DNA)]
            DNA_edited = DNA_l + integraton + DNA_r
        else: #if deletion not requested, defines edited DNA below
            DNA_l = DNA[0:Edit_site]
            DNA_r = DNA[1+Edit_site:len(DNA)]
            DNA_edited = DNA_l + Edit_nucl + DNA_r

        length_of_edit = len(Edit_nucl) #computes length of Edit in function, used to modify PAM search and avoid distant PAMs
                
        dna_reverse = DNA[::-1] #reverses DNA for PAM search, PAM search done on reverse to favor guides close to edit
        pam_rev_search = dna_reverse.index("GG", 205, (205+(edit_len-2)-(length_of_edit-1))) #default 203,202+edit_len_a-(length_of_edit-1) #determines PAM site from reverse, to place as close to edit as possible , 203 (reverse) is left most PAM and 200+edit_len_a is edit range with 3bp buffer in RT 
        PAM_site = len(DNA)-pam_rev_search-2
        
        #PAM_site = DNA.index("GG", Edit_site-1, Edit_site+6)
        
        protosp_pe = DNA[PAM_site-21:PAM_site-1]
        guide_1 = "G" + DNA[(PAM_site-21):(PAM_site-1)]
    
        pbs_1 = DNA[(PAM_site-4-pbs_len_a):(PAM_site-4)]
        dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pbs_1)
        pbs_finish = dna_rc
        
        edit_1 = DNA_edited[(PAM_site-4):(PAM_site-4+edit_len_a)] #Generates RT_edit from Edited product
        dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(edit_1) #Reverse complements RT Edit
        edit_finish = dna_rc #Finished RT_template sequence 
        
        ### pegRNA Oligos ###
        peg_guide_top = "CACC" + guide_1
        dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(guide_1)
        peg_guide_bot = "AAC" + dna_rc
        peg_edit_top = "TGC" + edit_finish + pbs_finish + u6_term + "CTGCA"
        peg_e_bot_start = edit_finish + pbs_finish + u6_term
        dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(peg_e_bot_start)
        peg_edit_bot = "G" + dna_rc        
        pegrna_top_finish = str(guide_1 + cas9_hp + edit_finish + pbs_finish + u6_term) #finished pegRNA sequence

        #### Editing strategy function ###
        print("Strategy is: " +str(strategy_selected))
        
        if strategy_selected == 'PE2_a':
            pe3_cut_distance = "" #blank since PE2 selected
            pe3_pe_finish = "" #blank since PE2 selected
            pe3_guide = "" #blank since PE2 selected
            ### Oligos ###
            pe3_guide_top = "" #blank since PE2 selected
            pe3_guide_bot = "" #blank since PE2 selected
            
        elif strategy_selected == 'PE3_a':
            try: #attempts to find PE3 protospacer
                pe3_pam_site = DNA.index("CC", PAM_site+30,PAM_site+100) #default +40,+90#searches for PE3 guide PAM on opposite strand
                pe3_pe_start = DNA[int(pe3_pam_site)+3:int(pe3_pam_site)+23] #double check spacings
                pe3_cut_distance = int(pe3_pam_site)-int(PAM_site)+10 #
                dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pe3_pe_start) 
                pe3_pe_finish = dna_rc #
                pe3_guide = "G" + pe3_pe_finish
                ### Oligos ###
                pe3_guide_top = "CACC" + pe3_guide
                dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pe3_guide)
                pe3_guide_bot = "AAAC" + dna_rc
            except: #if PE3 protospacer not found
                pe3_cut_distance = ""
                pe3_pe_finish = "PE3 Protospacer not found"
                pe3_guide = ""
                pe3_guide_top = ""
                pe3_guide_bot = ""

        elif strategy_selected == 'PE3B_a':
            try: #attempts to find PE3B protospacer
                dna_rc, dna_c, dna_r, dna_a  = dna_rev_comp(DNA_edited)
                DNA_edited_reverse = dna_r
                pe3_pam_site_init = DNA_edited_reverse.index("CC", Edit_site+3,Edit_site+23) #default +40,+90#searches for PE3 guide PAM on opposite strand
                pe3_pam_site = len(DNA)-pe3_pam_site_init-2
                pe3_pe_start = DNA_edited[int(pe3_pam_site)+3:int(pe3_pam_site)+23] #double check spacings
                pe3_cut_distance = int(pe3_pam_site)-int(PAM_site)+10 #
                dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pe3_pe_start) 
                pe3_pe_finish = dna_rc #
                pe3_guide = "G" + pe3_pe_finish
                ### Oligos ###
                pe3_guide_top = "CACC" + pe3_guide
                dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pe3_guide)
                pe3_guide_bot = "AAAC" + dna_rc
            except: #if PE3B protospacer not found
                pe3_cut_distance = "" 
                pe3_pe_finish = "PE3B Protospacer not found"
                pe3_guide = ""
                pe3_guide_top = ""
                pe3_guide_bot = ""
        
        return protosp_pe, PAM_site, guide_1, cas9_hp, edit_finish, pbs_finish, u6_term, pegrna_top_finish, pe3_cut_distance, pe3_pe_finish, pe3_guide, peg_guide_top, peg_guide_bot, peg_edit_top, peg_edit_bot, pe3_guide_top, pe3_guide_bot     
    
    """DESIGNS BOTTOM STRAND pegRNA"""
    def pegrna_bot(DNA, Edit_site, Edit_nucl, edit_len_a, pbs_len_a, cas9_hp, u6_term):
        if "D" in Edit_nucl: #Determines if user is requesting deletion
            deletion_length = int(Edit_nucl[1:len(Edit_nucl)])
            DNA_l = DNA[0:Edit_site]
            DNA_r = DNA[Edit_site+deletion_length:len(DNA)]  
            DNA_edited = DNA_l + DNA_r
        elif "I" in Edit_nucl:
            integraton = str(Edit_nucl[1:len(Edit_nucl)])
            DNA_l = DNA[0:Edit_site+1]
            DNA_r = DNA[1+Edit_site:len(DNA)]
            DNA_edited = DNA_l + integraton + DNA_r
        else: #if deletion not requested, defines edited DNA below
            DNA_l = DNA[0:Edit_site]
            DNA_r = DNA[1+Edit_site:len(DNA)]
            DNA_edited = DNA_l + Edit_nucl + DNA_r
        
        dna_rc, dna_c, dna_r, dna_a  = dna_rev_comp(DNA)
        dna_rcs = str(dna_rc)
        dna_reverse = dna_rcs[::-1]

        length_of_edit = len(Edit_nucl) #computes length of Edit in function, used to modify PAM search and avoid distant PAMs
        pam_rev_search = dna_reverse.index("GG", 204, (204+(edit_len-2)-(length_of_edit-1))) #determines if PAM is within 
        PAM_site_b = len(DNA)-pam_rev_search-2
        protosp_pe_b = dna_rcs[PAM_site_b-21:PAM_site_b-1]
        guide_1_b = "G" + dna_rcs[(PAM_site_b-21):(PAM_site_b-1)]
        pbs_1 = dna_rcs[(PAM_site_b-4-pbs_len_a):(PAM_site_b-4)] #defining PBS
        dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pbs_1)
        pbs_finish_b = dna_rc
        
        dna_rc, dna_c, dna_r, dna_a  = dna_rev_comp(DNA_edited) #defining RT edit
        edit_1 = dna_rc[(PAM_site_b-4):(PAM_site_b-4+edit_len_a)]
        dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(edit_1)
        edit_finish_b = dna_rc        
        pegrna_bot_finish = str(guide_1_b + cas9_hp + edit_finish_b + pbs_finish_b + u6_term) #full pegRNA seq
        
        ### Oligos ###
        peg_guide_top_b = "CACC" + str(guide_1_b) #Guide oligo top
        dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(guide_1_b)
        peg_guide_bot_b = "AAC" + dna_rc #Guide oligo bottom
        peg_edit_top_b = "TGC" + edit_finish_b + pbs_finish_b + u6_term + "CTGCA" #Edit oligo top
        peg_e_bot_start = edit_finish_b + pbs_finish_b + u6_term
        dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(peg_e_bot_start)
        peg_edit_bot_b = "G" + dna_rc #Edit oligo bottom        
             
        if strategy_selected == 'PE2_a':
            pe3_cut_distance_b = "" #blank since PE2 selected
            pe3_pe_finish_b = "" #blank since PE2 selected
            pe3_guide_b = "" #blank since PE2 selected
            ### Oligos ###
            pe3_guide_top_b = "" #blank since PE2 selected
            pe3_guide_bot_b = "" #blank since PE2 selected
            
        elif strategy_selected == 'PE3_a':
            try: #attempts to find PE3 protospacer
                pe3_pam_site_b = dna_rcs.index("CC", PAM_site_b+30,PAM_site_b+100) #default +40,+90#searches for PE3 guide PAM on opposite strand
                pe3_pe_start_b = dna_rcs[int(pe3_pam_site_b)+3:int(pe3_pam_site_b)+23] #double check spacings
                pe3_cut_distance_b = int(pe3_pam_site_b)-int(PAM_site_b)+10 #
                dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pe3_pe_start_b) 
                pe3_pe_finish_b = dna_rc #
                pe3_guide_b = "G" + pe3_pe_finish_b
                ### Oligos ###
                pe3_guide_top_b = "CACC" + pe3_guide_b
                dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pe3_guide)
                pe3_guide_bot_b = "AAAC" + dna_rc
            except: #if PE3 protospacer not found
                pe3_cut_distance_b = ""
                pe3_pe_finish_b = "PE3 Protospacer not found"
                pe3_guide_b = ""
                pe3_guide_top_b = ""
                pe3_guide_bot_b = ""

        elif strategy_selected == 'PE3B_a':
            try: #attempts to find PE3B protospacer
                dna_rc, dna_c, dna_r, dna_a  = dna_rev_comp(DNA_edited)
                DNA_edited_reverse = dna_r
                
                pe3_pam_site_init = DNA_edited_reverse.index("CC", Edit_site+3,Edit_site+23) #PE3B defined based off of edit
                
                pe3_pam_site_b = len(DNA)-pe3_pam_site_init-2
                pe3_pe_start = DNA_edited[int(pe3_pam_site_b)+3:int(pe3_pam_site_b)+23] #double check spacings
                pe3_cut_distance_b = int(pe3_pam_site_b)-int(PAM_site_b)+10 #
                dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pe3_pe_start) 
                pe3_pe_finish_b = dna_rc #
                pe3_guide_b = "G" + pe3_pe_finish
                ### Oligos ###
                pe3_guide_top_b = "CACC" + pe3_guide_b
                dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(pe3_guide_b)
                pe3_guide_bot_b = "AAAC" + dna_rc
            except: #if PE3B protospacer not found
                pe3_cut_distance_b = "" 
                pe3_pe_finish_b = "PE3B Protospacer not found"
                pe3_guide_b = ""
                pe3_guide_top_b = ""
                pe3_guide_bot_b = ""        
    
        return protosp_pe_b, PAM_site_b, guide_1_b, cas9_hp, edit_finish_b, pbs_finish_b, u6_term, pegrna_bot_finish, pe3_cut_distance_b, pe3_pe_finish_b, pe3_guide_b, peg_guide_top_b, peg_guide_bot_b, peg_edit_top_b, peg_edit_bot_b, pe3_guide_top_b, pe3_guide_bot_b  
    
    """LOOP FOR GENERATING PEGRNA CSV FILE"""
    with open(output_file_name,'w') as f1: #Creates CSV file
        writer=csv.writer(f1, delimiter=',',lineterminator='\n',) #assigns writer parameters, \t
        header = ['Name','Chromosome','Position', 'Edit', 'Strand', 'pegRNA','Protospacer' ,'RT Template','RT Length','Primer Sequence','PBS Length', 'PE3 or 3B Protospacer', 'PE3 or 3B Distance', 'peg_Guide_top', 'peg_Guide_bot', 'peg_Edit_top', 'peg_Edit_bot', 'PE3_Guide_top', 'PE3_Guide_bot', 'Seq_F', 'Seq_R', 'Notes'] #header of CSV file output
        writer.writerow(header) #creates header in file
        for index in range(1,len(parameters)):
            ###Input_CSV###
            pegRNA_name = str(parameters[index][0]) #Name of guide in input file
            chrom_num = str(parameters[index][1]) #chromosome of target locus
            input_position = int(parameters[index][2]) #specific Bp address of locus
            Edit_nucl = str(parameters[index][3]).upper() #Edit Specified in RT edit
            length_of_edit = len(parameters[index][3]) #used for modifying PAM site search calculation, avoid spurious ID of distant PAMs
            #Edit_site = int(209) #this is hard coded position of edit in seq returned from API
            edit_len = int(parameters[index][4]) #RT template length, also specifies editing range for PAM search
            edit_len_a = edit_len #explicitly keeps edit length as an integer
            pbs_len = int(parameters[index][5]) #Specified Primer length
            pbs_len_a = pbs_len #explicitly kepps PBS length as an integer
            notes = str(parameters[index][6]) #This is retained between input and output for note keeping
            #https://genome.ucsc.edu/goldenPath/help/api.html > get DNA seq from speficied chromosomes
#            position_start = str(input_position-210) #downstream of edit
#            position_end = str(input_position+210) #upstream of edit
#            url_req = str("https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=chr" + chrom_num + ";start=" + position_start +";end=" + position_end) #URL of UCSC Genome browaer Hg38 API
            try:
                ##################### Organism selection #####################
                if organism == "null":
                    print("no organism selected")
                    DNA = "No Organim, No DNA"
                    print(DNA)
                elif organism == "text": #manual 
                    file_name = open(input_file_path_text, "r")
                    print(file_name.read)
                    print(file_name.readable()) #TRUE OR FALSE output
                    DNA_in = str(file_name.readline()).upper().replace(' ','').replace('\n','') #converts all to upper and removes spaces
                    position_start = int(input_position-210) #downstream of edit
                    position_end = int(input_position+210) #upstream of edit
                    Edit_site = int(209)
                    DNA = DNA_in[position_start:position_end]
                    #print(DNA)
                    
                elif organism == "plasmid": #need to add text wrap around
                    file_name = open(input_file_path_text, "r")
                    print(file_name.read)
                    print(file_name.readable()) #TRUE OR FALSE output
                    DNA_in = str(file_name.readline()).upper().replace(' ','').replace('\n','') #converts all to upper and removes spaces and new lines
                    Edit_site = int(209)
                    
                    #determines position in plasmid, rotates plasmid to accomodate edits
                    if 210 <= input_position <= len(DNA_in)-210:
                        position_start = int(input_position-210) #downstream of edit
                        position_end = int(input_position+210) #upstream of edit
                        DNA = DNA_in[position_start:position_end]
                    elif input_position < 210:
                        plasmid_shift = str(DNA_in[len(DNA_in)-500:len(DNA_in)] + DNA_in[0:len(DNA_in)-500])
                        position_start = int(input_position-210+500) #downstream of edit
                        position_end = int(input_position+210+500) #upstream of edit
                        DNA = plasmid_shift[position_start:position_end]
                    elif len(DNA_in)-input_position < 210:
                        plasmid_shift = str(DNA_in[500:len(DNA_in)] + DNA_in[0:500])
                        position_start = int(input_position-210-500) #downstream of edit
                        position_end = int(input_position+210-500) #upstream of edit
                        DNA = plasmid_shift[position_start:position_end]
                    #print(DNA)
                
                elif organism == "S288C": #Yeast Saccharomyces cerevisae S288C, YGD
                    position_start = str(input_position-209) #downstream of edit
                    position_end = str(input_position+210) #upstream of edit
                    url_req = str("https://www.yeastgenome.org/run_seqtools?&chr=" + chrom_num + "&start=" + position_start +"&end=" + position_end + "&rev=0")
                    api_request = requests.get(url_req) #Begins API request
                    api = json.loads(api_request.content)
                    DNA_in = api['residue']
                    DNA = DNA_in.upper().replace(' ','') #converts all to upper and removes spaces
                    Edit_site = int(209) #this is hard coded position of edit in seq returned from API
                    print(DNA) 
                else: #Human Homo sapiens Hg38 and other
                    position_start = str(input_position-210) #downstream of edit
                    position_end = str(input_position+210) #upstream of edit
                    url_req = str("https://api.genome.ucsc.edu/getData/sequence?genome=" + organism + ";chrom=chr" + chrom_num + ";start=" + position_start +";end=" + position_end) #URL of UCSC Genome browaer Hg38 API
                    api_request = requests.get(url_req) #Begins API request
                    api = json.loads(api_request.content)
                    DNA_in = api['dna']
                    DNA = DNA_in.upper().replace(' ','') #converts all to upper and removes spaces
                    Edit_site = int(209) #this is hard coded position of edit in seq returned from API
                    print(DNA)

                ##################### Test if pegRNA can be designed, Positive Strand #####################
                dna_reverse = DNA[::-1] #reverses DNA for PAM search, PAM search done on reverse to favor guides close to edit
                pam_rev_search = dna_reverse.index("GG", 205, 205+((edit_len-2)-(length_of_edit-1))) #determines PAM site from reverse, to place as close to edit as possible 
                PAM_site = len(DNA)-pam_rev_search-2
    
                #PAM_site = DNA.index("GG", Edit_site-1, Edit_site+6) #OLD PAM SITE DEFINITION
                protosp_pe, PAM_site, guide_1, cas9_hp, edit_finish, pbs_finish, u6_term, pegrna_top_finish, pe3_cut_distance, pe3_pe_finish, pe3_guide, peg_guide_top, peg_guide_bot, peg_edit_top, peg_edit_bot, pe3_guide_top, pe3_guide_bot = pegrna_top(DNA, Edit_site, Edit_nucl, edit_len, pbs_len, cas9_hp, u6_term)
                print("Top strand protospacer " + str(index) + ":" + protosp_pe)
                print("Top pEGRNA for " + str(index) + ":")
                print("pegRNA for "  + str(index) + ":")
                #pegrna_top = str(guide_1 + cas9_hp + edit_finish + pbs_finish + u6_term)        
                print(guide_1 + cas9_hp + edit_finish + pbs_finish + u6_term) #print pegRNA for troubleshooting
                pegrna_top_finish = str(guide_1 + cas9_hp + edit_finish + pbs_finish + u6_term) #explicitly places parts together to make pegRNA
                
                ### Primers ###
                sequence = str(DNA[0:60])
                primer_seq = primer_tm_design(sequence) #forward primer, tm set
                seq_f_finish = primer_seq
                
                dna_rc , dna_c, dna_r, dna_a  = dna_rev_comp(DNA[len(DNA)-60:len(DNA)]) #reverse primer, tm set
                sequence = str(dna_rc)
                primer_seq = primer_tm_design(sequence)
                seq_r_finish = primer_seq
                
                ### Edit Defined ###
                if "D" in Edit_nucl: #Determines if user is requesting deletion
                    editing_product = str(Edit_nucl)
                elif "I" in Edit_nucl:
                    editing_product = str(Edit_nucl)
                else:
                    editing_product = str(DNA[209]) + "-to-" + str(Edit_nucl) #generates X-to-Y format for edit annotation
                
                print("PE3 Cut Distance: " + str(pe3_cut_distance))
                print("PE3 Protospacer: " + pe3_pe_finish)
                print("Forward Sequencing: " + seq_f_finish)
                print("Reverse Sequencing: " + seq_r_finish)
                print("Length of Edit " + str(index) + ": " + str(length_of_edit))
                strand_t = "Positive"
                #validation_top = "valid"
            except ValueError:
                pegrna_top_finish = "No Valid pegRNA"
                strand_t = "Positive"
                seq_f_finish = " "
                seq_r_finish = " "
                editing_product = " "
                protosp_pe = " "
                edit_finish = " "
                pbs_finish = " "
                pe3_pe_finish = " "
                pe3_cut_distance = " "
                peg_guide_top = " "
                peg_guide_bot = " "
                peg_edit_top = " "
                peg_edit_bot = " "
                pe3_guide_top = " "
                pe3_guide_bot = " "
                #validation_top = "error"
                print("No Valid positive strand pEGRNAs for " + str(index))
            row_t = [pegRNA_name, chrom_num, input_position, editing_product, strand_t, pegrna_top_finish, protosp_pe, edit_finish, edit_len, pbs_finish, pbs_len, pe3_pe_finish, pe3_cut_distance, peg_guide_top, peg_guide_bot, peg_edit_top, peg_edit_bot, pe3_guide_top, pe3_guide_bot, seq_f_finish, seq_r_finish, notes] #determines what values are writen to CSV file 
            writer.writerow(row_t) #writes new row eachtime
            #Negative strand pegRNAs below
            try:
                dna_rc, dna_c, dna_r, dna_a  = dna_rev_comp(DNA)
                dna_rcs = str(dna_rc)
                
                dna_reverse = dna_rcs[::-1] #reverses DNA for PAM search, PAM search done on reverse to favor guides close to edit
                pam_rev_search = dna_reverse.index("GG", 204, (204+(edit_len-2)-(length_of_edit-1))) #determines if PAM is within 
                PAM_site_b = len(DNA)-pam_rev_search-2
                protosp_pe_b, PAM_site_b, guide_1_b, cas9_hp, edit_finish_b, pbs_finish_b, u6_term, pegrna_bot_finish, pe3_cut_distance_b, pe3_pe_finish_b, pe3_guide_b, peg_guide_top_b, peg_guide_bot_b, peg_edit_top_b, peg_edit_bot_b, pe3_guide_top_b, pe3_guide_bot_b = pegrna_bot(DNA, Edit_site, Edit_nucl, edit_len, pbs_len, cas9_hp, u6_term)
                print("Bottom strand protospacer " + str(index) + ":" + protosp_pe_b)
                print("Bottom pEGRNA for " + str(index) + ":")
                print("pegRNA for "  + str(index) + ":")
                #pegrna_bot_finish = str(guide_1_b + cas9_hp + edit_finish_b + pbs_finish_b + u6_term)
                print(guide_1_b + cas9_hp + edit_finish_b + pbs_finish_b + u6_term)
                pegrna_bot_finish = str(guide_1_b + cas9_hp + edit_finish_b + pbs_finish_b + u6_term)
                
                ### Primers ###
                sequence = str(DNA[0:60])
                primer_seq = primer_tm_design(sequence) #forward primer, tm set
                seq_f_finish = primer_seq
                
                dna_rc , dna_c, dna_r, dna_a  = dna_rev_comp(DNA[len(DNA)-60:len(DNA)]) #reverse primer, tm set
                sequence = str(dna_rc)
                print(sequence)
                primer_seq = primer_tm_design(sequence)
                seq_r_finish = primer_seq
                
                #seq_f_finish = DNA[0:20] #Forward sequencing primer
                #dna_rc, dna_c, dna_r, dna_a = dna_rev_comp(DNA[len(DNA)-20:len(DNA)]) #Reverse sequencing primer
                #seq_r_finish = dna_rc #Reverse sequencing primer
                
                if "D" in Edit_nucl: #Determines if user is requesting deletion
                    editing_product = str(Edit_nucl)
                elif "I" in Edit_nucl:
                    editing_product = str(Edit_nucl)
                else:
                    editing_product = str(DNA[209]) + "-to-" + str(Edit_nucl) #generates X-to-Y format for edit annotation
                
                print("PE3 Cut Distance: " + str(pe3_cut_distance_b))
                print("PE3 Protospacer: " + pe3_pe_finish_b)
                print("Forward Sequencing: " + seq_f_finish)
                print("Reverse Sequencing: " + seq_r_finish)
                #validation_bot = "valid"
                strand_b = "Negative"
            except ValueError:
                pegrna_bot_finish = "No Valid pegRNA"
                editing_product = " "
                strand_b = "Negative"
                seq_f_finish = " "
                seq_r_finish = " "
                seq_r_finish = " "
                protosp_pe_b = " "
                edit_finish_b = " "
                pbs_finish_b = " "
                pe3_pe_finish_b = " "
                pe3_cut_distance_b = " "
                peg_guide_top_b = " "
                peg_guide_bot_b = " "
                peg_edit_top_b = " "
                peg_edit_bot_b = " "
                pe3_guide_top_b = " "
                pe3_guide_bot_b = " "
                #validation_bot = "error"
                print("No Valid negative strand  pEGRNAs " + str(index))
            row_b = [pegRNA_name, chrom_num, input_position, editing_product, strand_b, pegrna_bot_finish, protosp_pe_b, edit_finish_b, edit_len, pbs_finish_b, pbs_len, pe3_pe_finish_b, pe3_cut_distance_b, peg_guide_top_b, peg_guide_bot_b, peg_edit_top_b, peg_edit_bot_b, pe3_guide_top_b, pe3_guide_bot_b, seq_f_finish, seq_r_finish, notes]
            writer.writerow(row_b) #writes new row eachtime
            time.sleep(0.5) #limits API request to 1 per half second, prevents request spamming
    
    if organism == "hg38":
        analysis_button = Button(root, text='Analyze', command=analyze_file).grid(row=9, column=3, columnspan=1)
    elif organism == "S288C":
        analysis_button = Button(root, text='Analyze', command=analyze_file).grid(row=9, column=3, columnspan=1)
        
    csvfile.close()
    return output_file_name

"""Circos Image Generation"""
#def open_circos():
#    global output_file_name
#    global circos_image #dont seem to need to declare image before global
#    top = Toplevel()
#    top.title('Analysis of ' +str(output_file_name))
#    lbl = Label(top, text='Hello?').pack()
#    circos_image = ImageTk.PhotoImage(Image.open("Low_quality_example.png"))
#    circos_label = Label(top, image=circos_image).pack()
#    close_button = Button(top, text='close', command=top.destroy).pack()


"""This is the Circos Analyze Functions"""
def analyze_file():
    global circos_image #dont seem to need to declare image before global
    
    def polar2xy(r, theta):
        return np.array([r*np.cos(theta), r*np.sin(theta)])
    
    def IdeogramArc(start=0, end=60, radius=1.0, width=0.2, ax=None, color=1):#color=(1,0,0) changing color here doesnt seem to affect
        # start, end should be in [0, 360)
        if start > end:
            start, end = end, start
        start *= np.pi/180.
        end *= np.pi/180.
        # optimal distance to the control points
        # https://stackoverflow.com/questions/1734745/how-to-create-circle-with-b%C3%A9zier-curves
        opt = 4./3. * np.tan((end-start)/ 4.) * radius
        inner = radius*(1-width)
        verts = [
            polar2xy(radius, start),
            polar2xy(radius, start) + polar2xy(opt, start+0.5*np.pi),
            polar2xy(radius, end) + polar2xy(opt, end-0.5*np.pi),
            polar2xy(radius, end),
            polar2xy(inner, end),
            polar2xy(inner, end) + polar2xy(opt*(1-width), end-0.5*np.pi),
            polar2xy(inner, start) + polar2xy(opt*(1-width), start+0.5*np.pi),
            polar2xy(inner, start),
            polar2xy(radius, start),
            ]
    
        codes = [Path.MOVETO,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.LINETO,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CLOSEPOLY,
                 ]
    
        if ax == None:
            return verts, codes
        else: #color infor for circle
            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor=color, edgecolor='white', lw=2)
            ax.add_patch(patch) #remove "+(value)" to remove color distortion, +(0.5,), +(0.4,)
    
    """This is for chords between seperate sections""" # should not need to modify to much, just determines chord draw.
    def ChordArc(start1=0, end1=60, start2=180, end2=240, radius=1.0, chordwidth=0.7, ax=None, color=1):#color=(1,0,0)
        # start, end should be in [0, 360)
        if start1 > end1:
            start1, end1 = end1, start1
        if start2 > end2:
            start2, end2 = end2, start2
        start1 *= np.pi/180.
        end1 *= np.pi/180.
        start2 *= np.pi/180.
        end2 *= np.pi/180.
        opt1 = 4./3. * np.tan((end1-start1)/ 4.) * radius
        opt2 = 4./3. * np.tan((end2-start2)/ 4.) * radius
        rchord = radius * (1-chordwidth)
        verts = [
            polar2xy(radius, start1),
            polar2xy(radius, start1) + polar2xy(opt1, start1+0.5*np.pi),
            polar2xy(radius, end1) + polar2xy(opt1, end1-0.5*np.pi),
            polar2xy(radius, end1),
            polar2xy(rchord, end1),
            polar2xy(rchord, start2),
            polar2xy(radius, start2),
            polar2xy(radius, start2) + polar2xy(opt2, start2+0.5*np.pi),
            polar2xy(radius, end2) + polar2xy(opt2, end2-0.5*np.pi),
            polar2xy(radius, end2),
            polar2xy(rchord, end2),
            polar2xy(rchord, start1),
            polar2xy(radius, start1),
            ]
    
        codes = [Path.MOVETO,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 Path.CURVE4,
                 ]
    
        if ax == None:
            return verts, codes
        else: #color info for chords
            path = Path(verts, codes)
            patch = patches.PathPatch(path, facecolor=color+(0.5,), edgecolor=color+(0.5,), lw=0.3)
            ax.add_patch(patch) #modify  "+(value)" to manipulate color, +(0.5,), +(0.4,)
    
    """Plots chord diagram"""
    def chordDiagram(ax, colors=None, width=0.125, pad=0.0, chordwidth=0.7): #width is thickness of outer arc, pad is spacing between arcs, chordwith determines curvature of chords
        global valid_pegrna_sum
        
        if organism == 'S288C': #yeast genome dictionary
            chr_dict = {'chr1':230218,'chr2':813184,'chr3':316620,'chr4':1531933,
                              'chr5':576874,'chr6':270161,'chr7':1090940,'chr8':562643,
                              'chr9':439888,'chr10':745751,'chr11':666816,'chr12':1078177,
                              'chr13':924431,'chr14':784333,'chr15':1091291,'chr16':948066,'pegRNAs':600000}
        
        elif organism == 'hg38': #human genome dictionary
            chr_dict = {'chr1':248956422,'chr2':242193529,'chr3':198295559,'chr4':190214555,'chr5':181538259,
                          'chr6':170805979,'chr7':159345973,'chr8':145138636,'chr9':138394717,'chr10':133797422,
                          'chr11':135086622,'chr12':133275309,'chr13':114364328,'chr14':107043718,'chr15':101991189,
                          'chr16':90338345,'chr17':83257441,'chr18':80373285,'chr19':58617616,'chr20':64444167,
                          'chr21':46709983,'chr22':50818468,'chrx':156040895,'chry':57227415,'pegRNAs':145138636}
        
        chrom_names_list = list(chr_dict.keys())
        chrom_sizes_list = list(chr_dict.values())
        dictionary_sum = np.sum(chrom_sizes_list, dtype=np.int64).astype(float)
        pegRNA_degrees_start =  ((dictionary_sum-chr_dict['pegRNAs'])/dictionary_sum)*360
        pegRNA_degree_range = 360 - pegRNA_degrees_start
        #print(pegRNA_degree_range)
    
        ax.set_xlim(-1.1, 1.1) #sets axes scale, X
        ax.set_ylim(-1.1, 1.1) #sets axes scale, Y
    
        if colors is None: #color library 
            colors = [(0.40234375,0,0.05078125), (0.5977,0,0.0507), (0.79296875,0.09375,0.11328125), (0.93359375,0.23046875,0.171875),(0.98046875,0.4140625,0.2890625), (0.49609375,0.15234375,0.015625),
                      (0.6484375,0.2109375,0.01171875), (0.84765625,0.28125,0.00390625), (0.94140625,0.41015625,0.07421875),(0.98828125,0.55078125,0.234375), (0,0.265625,0.10546875), (0,0.42578125,0.171875),
                      (0.13671875,0.54296875,0.26953125), (0.25390625,0.66796875,0.36328125),(0.453125,0.765625,0.4609375), (0.03125,0.1875,0.41796875),(0.03125,0.31640625,0.609375), (0.12890625,0.44140625,0.70703125),
                      (0.2578125,0.5703125,0.7734375),(0.41796875,0.6796875,0.8359375), (0.24609375,0,0.48828125), (0.328125,0.15234375,0.55859375), (0.4140625,0.31640625,0.63671875), (0.5,0.48828125,0.7265625),
                      (0.03125,0.31640625,0.609375)]
            if len(chrom_sizes_list) > 25: #limit number of rows
                print('x is too large! Use x smaller than 10')
    
        #y determines proportion of arcs based off of chromosome sizes 
        y = chrom_sizes_list/np.sum(chrom_sizes_list, dtype=np.int64).astype(float) * (360 - pad*len(chrom_sizes_list)) #determines the proportion of the circle this takes up, 360 degrees- pad*number of arcs (rows)
        
        pos = {}
        arc = []
        nodePos = []    
        start = 0 #initial start position
    
        for i in range(len(chrom_sizes_list)): #x is sum of rows in data set, for loop runs and appends ARCS together
            end = start + y[i] #this determines arc size, use y[i]*0.5 to set to half circle
            arc.append((start, end)) #this looks like it adds new arcs to plot
            angle = 0.5*(start+end) #rotation of text
            
            if -30 <= angle <= 210:
                angle -= 90 #determines angle of text labels, 90 is tangent to circle, for top left half of circle
            else:
                angle -= 270 #determines angle of text labels, 90 is tangent to circle, for bottom right half of circle
            
            #######
            nodePos.append(tuple(polar2xy(0.93, 0.5*(start+end)*np.pi/180.)) + (angle,)) #controls distance out labels are places label for each arc
            #######
            
            start = end + pad #pad is distance between seperate arcs, start of new arc is defined here it appears
    
        for i in range(len(chrom_sizes_list)): #x is sum of rows in data set
            start, end = arc[i] #this detmines the arc position, essential
            #######
            IdeogramArc(start=start, end=end, radius=1.0, ax=ax, color=colors[i], width=width) #controls arc position, modifier can be added to end seq for chr. length
            #######
        """Analysis of excell output"""
        with open(output_file_name) as csvfile: #opens pinecone output
            readCSV = csv.reader(csvfile, delimiter=',')
            data1 = [list(row) for row in readCSV]
            #print(data)
            parameters1 = data1
            start2 = 340
            end2 = start2+0.5
            valid_pegrna_sum = 0
            
            for csv_add_value in range(1,len(parameters1)):
                pegRNA_status = str(parameters1[csv_add_value][5])
                if pegRNA_status == '':
                    none=0
                elif pegRNA_status == 'No Valid pegRNA':
                    none=0
                else:
                    valid_pegrna_sum += 1
            plotted_pegrna_count = 0
            print("Plotting " + str(valid_pegrna_sum) + " pegRNAs")
            for csv_index in range(1,len(parameters1)):
                pegRNA_name = str(parameters1[csv_index][0])
                pegRNA_chr = str(parameters1[csv_index][1]).lower()
                pegRNA_position = int(parameters1[csv_index][2])
                edit_result = str(parameters1[csv_index][3]).upper()
                pegRNA_status = str(parameters1[csv_index][5])
                
                if pegRNA_status == '':
                    none=0
                elif pegRNA_status == 'No Valid pegRNA':
                    none=0
                else:
                    input_key = "chr" + str(pegRNA_chr)
                    selection = chrom_names_list.index(input_key)
                    sum_total_chr = 0
                    sizes = 0
                    key_selection = chrom_names_list[0]
                    plotted_pegrna_count += 1
    
                    for q in range(0,selection): #this is noninclusive of selection
                        key_selection = chrom_names_list[q]
                        sizes = chr_dict[key_selection]
                        sum_total_chr += sizes
                       
                    sum_total_chr_edit = sum_total_chr + pegRNA_position #i think this calc should happen outside this loop
                    edit_degrees = (sum_total_chr_edit/dictionary_sum)*(360-pad*(q)) #need modify pad term
                
                    width1 = 0.5 #width of chords connecting to chromosome
                    start1 = edit_degrees-width1*0.5
                    end1 = edit_degrees+width1*0.5
        
                    if pegRNA_degree_range/valid_pegrna_sum > 0.5: #this controls sizes of chords into 'pegRNA' node for small data sets              
                        width2 = 0.5
                        centering_term = pegRNA_degrees_start + (pegRNA_degree_range-(valid_pegrna_sum*0.5))*0.5
                        start2 = centering_term+plotted_pegrna_count*width2 #makes steps proportion to width
                        end2 = start2+width2
                        #print('A')
                    else: #this controls sizes of chords into 'pegRNA' node 
                        width2 = (pegRNA_degree_range/valid_pegrna_sum) #width will get smaller with large data sets
                        #print('B')
                        start2 = pegRNA_degrees_start+plotted_pegrna_count*width2 #makes steps proportion to width
                        end2 = start2+width2
                    
                    label_radius = 1.01
                    if 0 <= edit_degrees <= 90:
                        ax.annotate(pegRNA_name, polar2xy(label_radius, (edit_degrees)*np.pi/180.),horizontalalignment='left', verticalalignment='bottom', rotation=edit_degrees) #pegRNA name, radius, position, angle i think
                    elif 90 < edit_degrees <=180:
                        ax.annotate(pegRNA_name, polar2xy(label_radius, (edit_degrees)*np.pi/180.),horizontalalignment='right', verticalalignment='bottom', rotation=edit_degrees-180)
                    elif 180 < edit_degrees <=270:
                        ax.annotate(pegRNA_name, polar2xy(label_radius, (edit_degrees)*np.pi/180.),horizontalalignment='right', verticalalignment='top', rotation=edit_degrees-180)
                    elif 270 < edit_degrees <=315:
                        ax.annotate(pegRNA_name, polar2xy(label_radius, (edit_degrees)*np.pi/180.),horizontalalignment='left', verticalalignment='top', rotation=edit_degrees)
                    else:
                        ax.annotate(pegRNA_name, polar2xy(label_radius, (edit_degrees)*np.pi/180.),horizontalalignment='right', verticalalignment='center', rotation=edit_degrees-180) #pegRNA name, radius, position, angle i think
                    
                    if "D" in edit_result:
                        chord_color = (0.79296875,0.09375,0.11328125) #Red
                    elif "I" in edit_result:
                        chord_color = (0,0.42578125,0.171875) #Green
                    else:
                        chord_color = (0.03125,0.31640625,0.609375) #Blue,  (0.03125,0.31640625,0.609375)   
                    
                    #############
                    ChordArc(start1, end1, start2, end2, radius=1.-width, color=chord_color, chordwidth=chordwidth, ax=ax)
                    #############
                    
        #print(nodePos)
        return nodePos 
    
    """Circos Figure Plotting"""
    fig = plt.figure(figsize=(8,8)) #plotsize 10x10 works well
    ax = plt.axes([0,0,1,1])
    nodePos = chordDiagram(ax)
    ax.axis('off') #axes around plot
    prop = dict(fontsize=16*0.8, ha='center', va='center')
    if organism == "S288C":
        nodes_chr = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X','XI','XII','XIII','XIV','XV','XVI','pegRNAs']
    elif organism == "hg38":
        nodes_chr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11','12','13','14','15','16','17','18','19','20','21','22','X','Y','pegRNAs'] # Names of labels
    
    for i in range(len(nodes_chr)): # number here is number of labels, 
        ax.text(nodePos[i][0], nodePos[i][1], nodes_chr[i], rotation=nodePos[i][2], **prop, color='white')
    high_res_display = "High_res_" + output_file_name_no_ext + ".svg"
    low_res_display = "Low_res_" + output_file_name_no_ext + ".png"
    plt.savefig(high_res_display, format="svg",transparent=True, bbox_inches='tight', pad_inches=0.02) #1000dpi looks good
    plt.savefig(low_res_display, dpi=75, transparent=True, bbox_inches='tight', pad_inches=0.02) #1000dpi looks good
    """tkinter function to display plot"""
    top = Toplevel()
    top.title('Analysis of ' +str(output_file_name_no_ext))
    lbl = Label(top, text=str(output_file_name_no_ext)+" has "+str(valid_pegrna_sum)+" valid pegRNAs").pack()
    circos_image = ImageTk.PhotoImage(Image.open(low_res_display))
    circos_label = Label(top, image=circos_image).pack()
    close_button = Button(top, text='close', command=top.destroy).pack()

"""UI Startup Buttons and Images"""

ui_title = Label(root, text="PINE CONE: Creator Of New Edits", font=('helvetica', 18, 'bold')).grid(row=0, column=0, columnspan=4, pady=2)
ui_1 = Label(root, text="1: Select Organism", font=('helvetica', 12, 'bold')).grid(row=2, column=0, columnspan=1, pady=2)
ui_2 = Label(root, text="2: Select Strategy", font=('helvetica', 12, 'bold')).grid(row=2, column=1, columnspan=2, pady=2)
ui_3 = Label(root, text="3: Select Input Files", font=('helvetica', 12, 'bold')).grid(row=5, column=0, columnspan=1, pady=2)
ui_4 = Label(root, text="4: Output File", font=('helvetica', 12, 'bold')).grid(row=5, column=1, columnspan=2, stick=W, pady=2)
ui_5 = Label(root, text="Output Name:").grid(row=6, column=1, columnspan=2, stick=W, pady=2)

place_holder_csv_selected = Label(root, text=" ", font=('helvetica', 12, 'bold')).grid(row=7, column=0, columnspan=3, sticky=W)
place_holder_dna_input = Label(root, text=" ", font=('helvetica', 12, 'bold')).grid(row=8, column=0)
place_holder_dna_selected = Label(root, text=" ", font=('helvetica', 12, 'bold')).grid(row=9, column=1, columnspan=3)
place_holder_output_status = Label(root, text=" ", font=('helvetica', 12, 'bold')).grid(row=7, column=1, columnspan=3)

"""Organism Dropdown menu list of organisms, if oganis list updated, also update comboclick function"""

organism_options = ["Select Organism",
                    "Manual (.txt)",
                    "Plasmid (.txt)",
                    "Human (hg38)", 
                    "Yeast (S288C)",
                    "Mouse (mm10)",
                    "Rat (rn6)",
                    "Zebrafish (danRer11)",
                    "Roundworm (ce11)",
                    "Fruitfly (dm6)",
                    "Dog (CanFam3)",
                    "Chimp (panTro6)",
                    "Proboscis monkey"]


"""User Interface"""
organism_clicked = StringVar()
organism_clicked.set(organism_options[0])
#starting image for organism logo
starting_query_logo_path = os.path.join('logos','Query_logo.png')
image1 = ImageTk.PhotoImage(Image.open(starting_query_logo_path))
label2 = Label(image=image1)
label2.image = image1
label2.grid(row=4, column=0)

"""PE Editing Strategy Radio Buttons"""


"""Dropdown Box for Organism Selection"""
myCombo = ttk.Combobox(root, value=organism_options)
myCombo.current(0)
myCombo.bind("<<ComboboxSelected>>", comboclick)#binds combo, (thing, action)
myCombo.grid(row=3, column=0)


"""Select File Button"""
my_btn = Button(root, text="Select Edit File (.csv)", command=select_file).grid(row=6, column=0, pady=2)

"""Banner Image"""
center_logo_path = os.path.join('logos',"Center_logo.png")
centerimage = ImageTk.PhotoImage(Image.open(center_logo_path))
centerlabel = Label(image=centerimage)
centerlabel.grid(row=1,column=0,columnspan=5, pady=5)

"""Labeling of buttons fg = foregroun and bg = background, can use Hex color code"""    
label_instruction = Label(root, text="Once file(s) are selected click 'Run PINE CONE'").grid(row=8, column=1, columnspan=3, sticky=W)
mybutton = Button(root, text="Run PINE CONE", command=run_button, fg='white', bg='red', font=('helvetica', 9, 'bold')).grid(row=9, column=1, columnspan=3)

"""Prime Editing Strategy Editing Buttons"""
for index, (text, mode) in enumerate(MODES):
    editing_strategy_radiobutton = Radiobutton(root, text=text,variable=strategy_input, value=mode, command=lambda: clicked(strategy_input.get()))
    editing_strategy_radiobutton.grid(row=3,column=(1+index))

"""Output File Entry"""
output_file_entry = Entry(root)
output_file_entry.grid(row=6, column=2, columnspan=2, stick=W, pady=2)

"""Editing Strategy Image"""
def clicked(value):
    global image_label_strategy
    global strategy_selected
    image_label_strategy.grid_forget()
    strategy_selected = value
    strategy_icons = {'PE2_a':'PE2_Logo.png', 'PE3_a':'PE3_Logo.png', 'PE3B_a':'PE3B_Logo.png'}    
    strategy_logo_path = os.path.join('logos',strategy_icons[value])
    image_strategy = ImageTk.PhotoImage(Image.open(strategy_logo_path))
    image_label_strategy = Label(image=image_strategy)
    image_label_strategy.image = image_strategy
    image_label_strategy.grid(row=4, column=1, columnspan=3)

root.mainloop()
print("Bye")