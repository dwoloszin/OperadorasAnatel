import os
import sys
import glob
import numpy as np
from itertools import chain
import pandas as pd
from simplekml import Kml, ListItemType, Color, Types, Snippet
import unique
import SectorGoogle
import simplekml
import timeit
import ImportDF











def process():
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    zip_directory = os.path.join(script_dir, 'export')

    csv_path = os.path.join(script_dir, 'export/'+'GOOGLE_ALL')
    frameSI = ImportDF.ImportDFFromZip(zip_directory)
    frameSI_copy = frameSI.copy()
    frameSI_Null = frameSI_copy[~frameSI_copy['Azimute_(Median)'].astype(bool)]
    UpdateDate = frameSI['UpdateDate'][0]
    kml = Kml(name="GOOGLE_ALL_"+UpdateDate, open=1)
    screen = kml.newscreenoverlay(name='Legends')
    legend_path = os.path.join(script_dir, 'import/legend/'+'legend5'+'.png')
    screen.icon.href = legend_path
    screen.overlayxy = simplekml.OverlayXY(x=0,y=1,xunits=simplekml.Units.fraction,yunits=simplekml.Units.fraction)
    screen.screenxy = simplekml.ScreenXY(x=1,y=1,xunits= simplekml.Units.pixels,yunits=simplekml.Units.insetpixels)
    screen.size.x = -1
    screen.size.y = -1
    screen.size.xunits = simplekml.Units.fraction
    screen.size.yunits = simplekml.Units.fraction

    endIDlist = []
    operator = []
    for index, row in frameSI.iterrows():
        if row['NomeEntidade'] not in operator:
            fol0 = kml.newfolder(name=row['NomeEntidade'])
            operator.append(row['NomeEntidade'])

        if row['NumEstacao'] not in endIDlist:
            fol = fol0.newfolder(name=row['NumEstacao'])
            endIDlist.append(row['NumEstacao'])
        

        pol = fol.newpolygon(name=row['physicalSector'])

        lat = float(row['Latitude'].split('|')[0])
        lon = float(row['Longitude'].split('|')[0])
        az = row['Azimute_(Median)']
        distt = float(row['distance'])
        vectors = SectorGoogle.CalcPointsSector(lat,lon,az,distt)
        pol.outerboundaryis = vectors

        pol.style.linestyle.color = colorretured(row['NomeEntidade'])
        pol.style.linestyle.width = 5
        pol.style.polystyle.color = simplekml.Color.changealphaint(180, colorretured(row['NomeEntidade']))


        for i in frameSI.columns:
            pol.extendeddata.newdata(name= i, value=str(row[i]), displayname=None)
    
    kml.savekmz(csv_path + ".kmz",format=False)      
    





#Corrigir SPENE_001*
def processArchiveSector():
    pathImport = '\export\GOOGLE_ALL'
    #fields = ['CELL_Fisico','LOCATION','CELLName','ref','MOBILE_SITE_NAME','LATITUDE','LONGITUDE','REGIONAL','IBGE_ID','ANF','MUNICIPIO','CS_STATUS','ALTURA','MECHANICAL_TILT','AMD_TILT_E','MS_TYPE','SI_PORT_BAND','CST_NAME','AZIMUTH','Dia ID','Data Primeiro Tráfego ID','Data Último Tráfego ID','Último Volume Dados Registrado','Semana do Ano','Hora','Classificação','Classificação2','Fator_Plan_LT','Vol_Total_Dl_Allop_LT','Throu_Pdcp_Cell_Dl_LT','Throu_User _Pdcp_Dl_LT','TPUT','Act_Ue_Data_Dl_LT','Users_Rrc_Conn_Mean_LT','Cqi_Mean_LT','Prb_Util_Mean_Dl_LT','Tti_Util_LT','Util_LT','dataArchive_x','LastClassif','LastClassif2','ADM STATE','OP STATE','EARFCNDL','BW DL','TAC','ENODEB ID','CELL ID','PCI','[S]','MIMO','dataArchive_y','ORDEM COMPLEXA','ELEMENTO ID','PROJETO','SPRINT','SETORES 4G MMIMO','FREQ 4G','REAL ATIVAÇÃO NETFLOW','PLO + OC','STATUS ATIVAÇÃO','STATUS ATIVAÇÃO2','dataArchive','FREQUÊNCIA ROLLOUT']
    fields = ['CELL_Fisico_Portal_PMO','Station ID ID_Portal_PMO', 'AZIMUTH_LOCATION_Azi_ALL','Dia ID_Portal_PMO','Municipio Nome_Portal_PMO','Municipio ID_Portal_PMO', 'ANF ID_Portal_PMO', 'BTS/NodeB/ENodeB DESC_Portal_PMO', 'Celula DESC_Portal_PMO', 'Banda DESC_Portal_PMO','CST_NAME_Portal_PMO', 'Latitude Celula ID_Portal_PMO', 'Longitude Celula ID_Portal_PMO', 'Tecnologia Sigla_Portal_PMO', 'Data Primeiro Trafego ID2_Portal_PMO','Ultimo Trafego Voz Registrado2_Portal_PMO','Ultimo Volume Dados Registrado2_Portal_PMO','ActiveCellTime(days)_Portal_PMO', 'ActiveCellTime(days)2_Portal_PMO', 'CS_STATUS_SI', 'ALTURA_SI', 'MS_TYPE_SI', 'SI_PORT_BAND_SI', 'CST_NAME_SI', 'NGNIS_DUMP', 'ADM STATE2_DUMP', 'OP STATE2_DUMP', 'FREQ CELL_DUMP', 'FREQ SITE_DUMP','CST_NAME_DUMP', 'EARFCNDL2_DUMP', 'BW DL_DUMP', 'TAC_DUMP', 'ENODEB ID_DUMP', 'PCI_DUMP', '[S]2_DUMP', 'MIMO2_DUMP', 'dataArchive_DUMP', 'Banda_CELULAS_CRITICAS','CST_NAME_CELULAS_CRITICAS','Flag Mocn_CELULAS_CRITICAS', 'Semana do Ano_CELULAS_CRITICAS', 'Classificacao_CELULAS_CRITICAS', 'TPUT_CELULAS_CRITICAS', 'Tti_Util_LT_CELULAS_CRITICAS', 'Classificacao2_CELULAS_CRITICAS','LastClassif_CELULAS_CRITICAS', 'LastClassif2_CELULAS_CRITICAS','ClassificacaoGeralW_CELULAS_CRITICAS','GeralCritico_CELULAS_CRITICAS','GeralAlerta_CELULAS_CRITICAS','GeralBom_CELULAS_CRITICAS','GeralExcelente_CELULAS_CRITICAS', 'ORDEM COMPLEXA_PMO_CellFisico', 'PROJETO_PMO_CellFisico', 'SPRINT_PMO_CellFisico', 'SETORES 4G MMIMO_PMO_CellFisico', 'FREQ 4G_PMO_CellFisico', 'REAL ATIVACAO NETFLOW_PMO_CellFisico', 'PLO + OC_PMO_CellFisico', 'STATUS ATIVACAO_PMO_CellFisico','STATUS ATIVACAO2_PMO_CellFisico', 'dataArchive_PMO_CellFisico', 'TECNOLOGIA_PMO_CellFisico', 'FREQUENCIA ROLLOUT_PMO_CellFisico','CST_NAME_PMO_CellFisico','Periodo_SmartService_EVE','count(TOTAL)_SmartService_EVE','Numero_Open_SmartService_EVE','Status_Open_SmartService_EVE','Data de Criacao_Open_SmartService_EVE','count_Open_SmartService_EVE','Periodo_SmartService_ACESSO','Numero_SmartService_ACESSO','DataInicio_SmartService_ACESSO','Status_SmartService_ACESSO','NE ID_SmartService_ACESSO','dataArchive_SmartService_ACESSO','count(TOTAL)_SmartService_ACESSO','Numero_Open_SmartService_ACESSO','DataInicio_Open_SmartService_ACESSO','NE ID_Open_SmartService_ACESSO','count_Open_SmartService_ACESSO','Periodo_TWAMP','PacketLatJitClassifLastClass_TWAMP','PacketLatJitClassifLastClassTxt_TWAMP','PacketLatJitClassifLastClassTxt2_TWAMP','DEGRADOU_TWAMP']
    pathImportSI = os.getcwd() + pathImport
    archiveName = pathImport[8:len(pathImport)]
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    csv_path = os.path.join(script_dir, 'export/'+'GOOGLE_ALL')
    legend_path = os.path.join(script_dir, 'import/legend/'+'legend3'+'.png')
    #print ('loalding files...\n')
    all_filesSI = glob.glob(pathImportSI + "/*.csv")
    all_filesSI.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    li = []
    
    for filename in all_filesSI:
        iter_csv = pd.read_csv(filename, index_col=None, encoding="UTF-8", header=0, error_bad_lines=False,dtype=str, sep = ';',iterator=True, chunksize=10000, usecols = fields )
        df = pd.concat([chunk for chunk in iter_csv])

        df2 = df[fields] # ordering labels
        li.append(df2)
    frameSI = pd.concat(li, axis=0, ignore_index=True)
    frameSI.fillna(0,inplace=True)
    
    # end_ID vazios
    frameSI_copy = frameSI.copy()
    frameSI_Null = frameSI_copy[~frameSI_copy['Latitude Celula ID_Portal_PMO'].astype(bool)]
    
    KeepList_frameSI_Null = ['Station ID ID_Portal_PMO','Municipio Nome_Portal_PMO','ANF ID_Portal_PMO','BTS/NodeB/ENodeB DESC_Portal_PMO','Latitude Celula ID_Portal_PMO','Longitude Celula ID_Portal_PMO','ORDEM COMPLEXA_PMO_CellFisico','PROJETO_PMO_CellFisico','SPRINT_PMO_CellFisico','STATUS ATIVACAO_PMO_CellFisico','STATUS ATIVACAO2_PMO_CellFisico','TECNOLOGIA_PMO_CellFisico']
    renameList_frameSI_Null = ['End_ID','Municipio','ANF','SITE','Lat','Long','ORDEM','PROJETO','SPRINT','STATUS','STATUS2','TECNOLOGIA']

    locationBase_frameSI_Null = list(frameSI_Null.columns)
    DellList = list(set(locationBase_frameSI_Null)^set(KeepList_frameSI_Null))
    frameSI_Null = frameSI_Null.drop(DellList,1)
    frameSI_Null = frameSI_Null.drop_duplicates()
    frameSI_Null = frameSI_Null.reset_index(drop=True)
    frameSI_Null.columns = renameList_frameSI_Null
    
    csv_path_frameSI_Null = os.path.join(script_dir, 'export/'+'End_ID_Null_Spazio.csv')
    frameSI_Null.to_csv(csv_path_frameSI_Null,index=True,header=True,sep=';',encoding='UTF-8')

    
    
    #exclui linhas com latitude vazia antes de rodar o loop
    frameSI = frameSI[frameSI['Latitude Celula ID_Portal_PMO'].astype(bool)]
    kml = Kml(name="GOOGLE_ALL", open=1)
    screen = kml.newscreenoverlay(name='Legends')
    screen.icon.href = legend_path
    #screen.icon.href = r'C:\Users\f8059678\OneDrive - TIM\Dario\@_PYTHON\GOOGLE_ALL\import\legend\legend.png'
    screen.overlayxy = simplekml.OverlayXY(x=0,y=1,xunits=simplekml.Units.fraction,yunits=simplekml.Units.fraction)
    screen.screenxy = simplekml.ScreenXY(x=1,y=1,xunits= simplekml.Units.pixels,yunits=simplekml.Units.insetpixels)
    screen.size.x = -1
    screen.size.y = -1
    screen.size.xunits = simplekml.Units.fraction
    screen.size.yunits = simplekml.Units.fraction


    endIDlist = []
    frameSI.insert(len(frameSI.columns),'Balanceamento','')
    frameSI.insert(len(frameSI.columns),'Criticas_Prio','')
    frameSI.insert(len(frameSI.columns),'Rollout_Prio','')
    frameSI.insert(len(frameSI.columns),'TWAMP_Prio','')
    frameSI.insert(len(frameSI.columns),'ClassificacaoGeralLastW_CELULAS_CRITICAS','Bom')

    
    for index, row in frameSI.iterrows():
        if row['BTS/NodeB/ENodeB DESC_Portal_PMO'] not in endIDlist:
            fol = kml.newfolder(name=row['BTS/NodeB/ENodeB DESC_Portal_PMO'])
            endIDlist.append(row['BTS/NodeB/ENodeB DESC_Portal_PMO'])

        #fol = kml.newfolder(name=row['CELL_Fisico'])
        #pnt = fol.newpoint(name=row['CELL_Fisico'], coords =[(row['LONGITUDE'].replace(',','.'),row['LATITUDE'].replace(',','.'))])
        pol = fol.newpolygon(name=row['CELL_Fisico_Portal_PMO'])

        lat = row['Latitude Celula ID_Portal_PMO'].replace(',','.')
        lon = row['Longitude Celula ID_Portal_PMO'].replace(',','.')
        az = row['AZIMUTH_LOCATION_Azi_ALL']
        vectors = SectorGoogle.CalcPointsSector(lat,lon,az)
        pol.outerboundaryis = vectors

        pol.style.linestyle.color = simplekml.Color.green
        pol.style.linestyle.width = 5
        pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.green)
        xf = str(row['LastClassif_CELULAS_CRITICAS']).split('|')
        st = str(row['STATUS ATIVACAO_PMO_CellFisico']).split('|')
        MS_TYPE2 = str(row['Tecnologia Sigla_Portal_PMO']).split('|')
        critico = 0
        alerta = 0
        bom = 0
        excelente = 0
        count = 0
        count4g = 0

        for gh in xf:
            if len(gh) > 2:
                if gh == 'Critico':
                    critico +=1
                    count +=1
                if gh == 'Alerta':
                    alerta +=1
                    count +=1
                if gh == 'Bom':
                    bom +=1
                    count +=1
                if gh == 'Excelente':
                    excelente +=1
                    count +=1
        
        for ms in MS_TYPE2:
            if ms == '4G':
                count4g +=1

        # NO PLO
        if row['PLO + OC_PMO_CellFisico'] == '0' or row['PLO + OC_PMO_CellFisico'] == 0 or row['STATUS ATIVACAO_PMO_CellFisico'] == 'ATIVO' :
            if critico + alerta <= excelente and critico + alerta != 0:
                pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                pol.style.linestyle.width = 5
                pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.dodgerblue)# 0 - 255
                frameSI.at[index,'Balanceamento'] = 'Balanceamento'
                frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Balanceamento'
            else:
                if critico > (count/2) and critico != 0:
                    pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                    pol.style.linestyle.width = 5
                    pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.black)
                    frameSI.at[index,'Criticas_Prio'] = 'Prio_0'
                    frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                    frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'SuperCritico'
                else:
                    if 'Critico' in xf:
                        pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                        pol.style.linestyle.width = 5
                        pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.deeppink)
                        frameSI.at[index,'Criticas_Prio'] = 'Prio_1'
                        frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                        frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Critico'
                    else:
                        if 'Alerta' in xf:
                            pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                            pol.style.linestyle.width = 5
                            pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.gold)
                            frameSI.at[index,'Criticas_Prio'] = 'Prio_2'
                            frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                            frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Alerta'
                        else:
                            if count4g > 0:
                                pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                pol.style.linestyle.width = 5
                                pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.green)
                                frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))    
                            else:
                                pol.style.linestyle.color = simplekml.Color.blue
                                pol.style.linestyle.width = 5
                                pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.green)
                                frameSI.at[index,'Rollout_Prio'] = 'Prio_4'
        # com PMO
        else:
            if row['ActiveCellTime(days)_Portal_PMO'] == '0':
                pol.style.linestyle.color = simplekml.Color.whitesmoke
                pol.style.linestyle.width = 5
                pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.white)

            else:


                if critico + alerta <= excelente and critico + alerta != 0:
                    pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                    pol.style.linestyle.width = 2
                    pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.dodgerblue)
                    frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                    frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Balanceamento'

                else:
                    if critico > (count/2) and critico != 0:
                        pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                        pol.style.linestyle.width = 2
                        pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.black)
                        frameSI.at[index,'Rollout_Prio'] = 'Prio_0'
                        frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                        frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'SuperCritico'
                    else:
                        if 'Critico' in xf:
                            pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                            pol.style.linestyle.width = 2
                            pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.deeppink)
                            frameSI.at[index,'Rollout_Prio'] = 'Prio_1'
                            frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                            frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Critico'

                        else:
                            if 'Alerta' in xf:
                                pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                pol.style.linestyle.width = 2
                                pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.gold)
                                frameSI.at[index,'Rollout_Prio'] = 'Prio_2'
                                frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Alerta'
                            else:
                                if count4g > 0:
                                    pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                    pol.style.linestyle.width = 2
                                    pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.green)
                                    frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                    

                                else:
                                    pol.style.linestyle.color = simplekml.Color.blue
                                    pol.style.linestyle.width = 2
                                    pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.green)
                                    frameSI.at[index,'Rollout_Prio'] = 'Prio_3'

                                

        
        #removefromloop0 = ['Banda DESC_Portal_PMO','CST_NAME_Portal_PMO', 'Tecnologia Sigla', 'SI_PORT_BAND_SI', 'MS_TYPE_SI','FREQ CELL_DUMP', 'FREQ SITE_DUMP','CST_NAME_DUMP', 'BW DL_DUMP','Banda_CELULAS_CRITICAS','ClassificacaoGeralW_CELULAS_CRITICAS','GeralCritico_CELULAS_CRITICAS','GeralAlerta_CELULAS_CRITICAS','GeralBom_CELULAS_CRITICAS','GeralExcelente_CELULAS_CRITICAS','FREQUENCIA ROLLOUT_PMO_CellFisico']
        removefromloop0 = ['Banda DESC_Portal_PMO','CST_NAME_Portal_PMO', 'Tecnologia Sigla', 'SI_PORT_BAND_SI', 'MS_TYPE_SI','FREQ CELL_DUMP', 'FREQ SITE_DUMP','CST_NAME_DUMP', 'BW DL_DUMP','Banda_CELULAS_CRITICAS','GeralCritico_CELULAS_CRITICAS','GeralAlerta_CELULAS_CRITICAS','GeralBom_CELULAS_CRITICAS','GeralExcelente_CELULAS_CRITICAS','FREQUENCIA ROLLOUT_PMO_CellFisico']
        legend = []
        for t in fields:
            if t not in legend and t not in removefromloop0:
                legend.append(t)



        for i in legend:
            pol.extendeddata.newdata(name= i, value=str(row[i]), displayname=None)
        
    removefromloop = ['Station ID ID_Portal_PMO','CELL_Fisico_Portal_PMO','Classificacao2_CELULAS_CRITICAS','LastClassif2_CELULAS_CRITICAS','STATUS ATIVACAO2_PMO_CellFisico','Balanceamento','Criticas_Prio','Rollout_Prio','ANF ID_Portal_PMO','Municipio Nome_Portal_PMO','Periodo_TWAMP','PacketLatJitClassifLastClass_TWAMP','PacketLatJitClassifLastClassTxt_TWAMP','PacketLatJitClassifLastClassTxt2_TWAMP','DEGRADOU_TWAMP','TWAMP_Prio']
    locationBase_top = list(frameSI.columns)
    res = list(set(locationBase_top)^set(removefromloop))
    
    frameSI = frameSI.drop(res,axis=1)
    CriticasPrio = frameSI.copy()
    CriticasPrio = CriticasPrio.drop(['TWAMP_Prio','Balanceamento','Rollout_Prio','Periodo_TWAMP','PacketLatJitClassifLastClass_TWAMP','PacketLatJitClassifLastClassTxt_TWAMP','PacketLatJitClassifLastClassTxt2_TWAMP','DEGRADOU_TWAMP'],axis=1)
    #CriticasPrio = CriticasPrio.drop(CriticasPrio.loc[CriticasPrio['Criticas_Prio'] != 'Criticas_Prio'].index)
    CriticasPrio = CriticasPrio.loc[CriticasPrio['Criticas_Prio'].isin(['Prio_0','Prio_1','Prio_2'])]
    CriticasPrio = CriticasPrio.sort_values(["Criticas_Prio"], ascending = [True])
    CriticasPrio = CriticasPrio.reset_index(drop=True)

    csv_path10 = os.path.join(script_dir, 'export/'+'Criticas_Prio'+'.csv')
    CriticasPrio.to_csv(csv_path10,index=False,header=True,sep=';')


    Rollout_Prio = frameSI.copy()
    Rollout_Prio = Rollout_Prio.drop(['Balanceamento','Criticas_Prio','Periodo_TWAMP','PacketLatJitClassifLastClass_TWAMP','PacketLatJitClassifLastClassTxt_TWAMP','PacketLatJitClassifLastClassTxt2_TWAMP','DEGRADOU_TWAMP','TWAMP_Prio'],axis=1)
    #CriticasPrio = CriticasPrio.drop(CriticasPrio.loc[CriticasPrio['Criticas_Prio'] != 'Criticas_Prio'].index)
    Rollout_Prio = Rollout_Prio.loc[Rollout_Prio['Rollout_Prio'].isin(['Prio_0','Prio_1','Prio_2','Prio_3','Prio_4'])]
    Rollout_Prio = Rollout_Prio.sort_values(["Rollout_Prio"], ascending = [True])
    Rollout_Prio = Rollout_Prio.reset_index(drop=True)

    csv_path11 = os.path.join(script_dir, 'export/'+'Rollout_Prio'+'.csv')
    Rollout_Prio.to_csv(csv_path11,index=False,header=True,sep=';')



    Balanceamento = frameSI.copy()
    Balanceamento = Balanceamento.drop(['TWAMP_Prio','Periodo_TWAMP','PacketLatJitClassifLastClass_TWAMP','PacketLatJitClassifLastClassTxt_TWAMP','PacketLatJitClassifLastClassTxt2_TWAMP','DEGRADOU_TWAMP'],axis=1)
    Balanceamento = Balanceamento.drop(Balanceamento.loc[Balanceamento['Balanceamento'] != 'Balanceamento'].index)
    Balanceamento = Balanceamento.drop(['Criticas_Prio','Rollout_Prio'],axis=1)
    csv_path2 = os.path.join(script_dir, 'export/'+'Balanceamento'+'.csv')
    Balanceamento.to_csv(csv_path2,index=False,header=True,sep=';')




    TWAMP = frameSI.copy()
    print(TWAMP.head())
    
    TWAMP = TWAMP.drop(['Classificacao2_CELULAS_CRITICAS','LastClassif2_CELULAS_CRITICAS','STATUS ATIVACAO2_PMO_CellFisico','Balanceamento','Criticas_Prio', 'Rollout_Prio'],axis=1)
    TWAMP = TWAMP.loc[TWAMP['TWAMP_Prio'].isin(['Prio_0','Prio_1','Prio_2','Prio_3'])]
    TWAMP = TWAMP.sort_values(["TWAMP_Prio"], ascending = [True])
    TWAMP = TWAMP.reset_index(drop=True)
    csv_path21 = os.path.join(script_dir, 'export/'+'TWAMP'+'.csv')
    TWAMP.to_csv(csv_path21,index=False,header=True,sep=';')
    



    #kml.save(os.path.splitext(__file__)[0] + ".kml",format=False)
    #kml.save(csv_path + ".kml",format=False)
    kml.savekmz(csv_path + ".kmz",format=False)

def processArchiveSector2():
    pathImport = '\export\GOOGLE_ALL2'
    #fields = ['CELL_Fisico','LOCATION','CELLName','ref','MOBILE_SITE_NAME','LATITUDE','LONGITUDE','REGIONAL','IBGE_ID','ANF','MUNICIPIO','CS_STATUS','ALTURA','MECHANICAL_TILT','AMD_TILT_E','MS_TYPE','SI_PORT_BAND','CST_NAME','AZIMUTH','Dia ID','Data Primeiro Tráfego ID','Data Último Tráfego ID','Último Volume Dados Registrado','Semana do Ano','Hora','Classificação','Classificação2','Fator_Plan_LT','Vol_Total_Dl_Allop_LT','Throu_Pdcp_Cell_Dl_LT','Throu_User _Pdcp_Dl_LT','TPUT','Act_Ue_Data_Dl_LT','Users_Rrc_Conn_Mean_LT','Cqi_Mean_LT','Prb_Util_Mean_Dl_LT','Tti_Util_LT','Util_LT','dataArchive_x','LastClassif','LastClassif2','ADM STATE','OP STATE','EARFCNDL','BW DL','TAC','ENODEB ID','CELL ID','PCI','[S]','MIMO','dataArchive_y','ORDEM COMPLEXA','ELEMENTO ID','PROJETO','SPRINT','SETORES 4G MMIMO','FREQ 4G','REAL ATIVAÇÃO NETFLOW','PLO + OC','STATUS ATIVAÇÃO','STATUS ATIVAÇÃO2','dataArchive','FREQUÊNCIA ROLLOUT']
    #fields = ['CELL_Fisico_Portal_PMO','Station ID ID_Portal_PMO', 'AZIMUTH_LOCATION_Azi_ALL','Dia ID_Portal_PMO','Municipio Nome_Portal_PMO','Municipio ID_Portal_PMO', 'ANF ID_Portal_PMO', 'BTS/NodeB/ENodeB DESC_Portal_PMO', 'Celula DESC_Portal_PMO', 'Banda DESC_Portal_PMO','CST_NAME_Portal_PMO', 'Latitude Celula ID_Portal_PMO', 'Longitude Celula ID_Portal_PMO', 'Tecnologia Sigla_Portal_PMO', 'Data Primeiro Trafego ID2_Portal_PMO','Ultimo Trafego Voz Registrado2_Portal_PMO','Ultimo Volume Dados Registrado2_Portal_PMO','ActiveCellTime(days)_Portal_PMO', 'ActiveCellTime(days)2_Portal_PMO', 'CS_STATUS_SI', 'ALTURA_SI', 'MS_TYPE_SI', 'SI_PORT_BAND_SI', 'CST_NAME_SI', 'NGNIS_DUMP', 'ADM STATE2_DUMP', 'OP STATE2_DUMP', 'FREQ CELL_DUMP', 'FREQ SITE_DUMP','CST_NAME_DUMP', 'EARFCNDL2_DUMP', 'BW DL_DUMP', 'TAC_DUMP', 'ENODEB ID_DUMP', 'PCI_DUMP', '[S]2_DUMP', 'MIMO2_DUMP', 'dataArchive_DUMP', 'Banda_CELULAS_CRITICAS','CST_NAME_CELULAS_CRITICAS','Flag Mocn_CELULAS_CRITICAS', 'Semana do Ano_CELULAS_CRITICAS', 'Classificacao_CELULAS_CRITICAS', 'TPUT_CELULAS_CRITICAS', 'Tti_Util_LT_CELULAS_CRITICAS', 'Classificacao2_CELULAS_CRITICAS','LastClassif_CELULAS_CRITICAS', 'LastClassif2_CELULAS_CRITICAS','ClassificacaoGeralW_CELULAS_CRITICAS','GeralCritico_CELULAS_CRITICAS','GeralAlerta_CELULAS_CRITICAS','GeralBom_CELULAS_CRITICAS','GeralExcelente_CELULAS_CRITICAS', 'ORDEM COMPLEXA_PMO_CellFisico', 'PROJETO_PMO_CellFisico', 'SPRINT_PMO_CellFisico', 'SETORES 4G MMIMO_PMO_CellFisico', 'FREQ 4G_PMO_CellFisico', 'REAL ATIVACAO NETFLOW_PMO_CellFisico', 'PLO + OC_PMO_CellFisico', 'STATUS ATIVACAO_PMO_CellFisico','STATUS ATIVACAO2_PMO_CellFisico', 'dataArchive_PMO_CellFisico', 'TECNOLOGIA_PMO_CellFisico', 'FREQUENCIA ROLLOUT_PMO_CellFisico','CST_NAME_PMO_CellFisico','Periodo_SmartService_EVE','count(TOTAL)_SmartService_EVE','Numero_Open_SmartService_EVE','Status_Open_SmartService_EVE','Data de Criacao_Open_SmartService_EVE','count_Open_SmartService_EVE','Periodo_SmartService_ACESSO','Numero_SmartService_ACESSO','DataInicio_SmartService_ACESSO','Status_SmartService_ACESSO','NE ID_SmartService_ACESSO','dataArchive_SmartService_ACESSO','count(TOTAL)_SmartService_ACESSO','Numero_Open_SmartService_ACESSO','DataInicio_Open_SmartService_ACESSO','NE ID_Open_SmartService_ACESSO','count_Open_SmartService_ACESSO','Periodo_TWAMP','PacketLatJitClassifLastClass_TWAMP','PacketLatJitClassifLastClassTxt_TWAMP','PacketLatJitClassifLastClassTxt2_TWAMP','DEGRADOU_TWAMP']
    fields = ['NAME','AZI','COLOR','Hexa']
    pathImportSI = os.getcwd() + pathImport
    archiveName = pathImport[8:len(pathImport)]
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    csv_path = os.path.join(script_dir, 'export/'+'GOOGLE_ALL2')
  
    #print ('loalding files...\n')
    all_filesSI = glob.glob(pathImportSI + "/*.csv")
    all_filesSI.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    li = []
    
    for filename in all_filesSI:
        iter_csv = pd.read_csv(filename, index_col=None, encoding="UTF-8", header=0, error_bad_lines=False,dtype=str, sep = ';',iterator=True, chunksize=10000, usecols = fields )
        df = pd.concat([chunk for chunk in iter_csv])

        df2 = df[fields] # ordering labels
        li.append(df2)
    frameSI = pd.concat(li, axis=0, ignore_index=True)
    frameSI.fillna(0,inplace=True)

    latlongref = [-25.507065,-49.277478]
    

    kml = Kml(name="GOOGLE_ALL", open=1)


    xdesloc = 0.0
    ydesloc = 0.0
    count = 0
    countr = 0
    for index, row in frameSI.iterrows():
        if count > 2:
            xdesloc += 0.005
            count = 0




        fol = kml.newfolder(name=row['NAME'])
        pol = fol.newpolygon(name=row['NAME'])
        vectors = SectorGoogle.CalcPointsSector(latlongref[0]+xdesloc,latlongref[1]+ydesloc,row['AZI'])
        pol.outerboundaryis = vectors
        pol.style.linestyle.color = colorretured(row['NAME'])
        pol.style.linestyle.width = 5
        pol.style.polystyle.color = simplekml.Color.changealphaint(150,colorretured(row['NAME']))
        pol.extendeddata.newdata(name= row['NAME'], value=str(row['NAME']), displayname=None)
        count += 1
        countr += 1


    #kml.save(os.path.splitext(__file__)[0] + ".kml",format=False)
    kml.savekmz(csv_path + ".kmz",format=False)


def processArchiveSector3():
    pathImport = '\export\GOOGLE_ALL'
    #fields = ['CELL_Fisico','LOCATION','CELLName','ref','MOBILE_SITE_NAME','LATITUDE','LONGITUDE','REGIONAL','IBGE_ID','ANF','MUNICIPIO','CS_STATUS','ALTURA','MECHANICAL_TILT','AMD_TILT_E','MS_TYPE','SI_PORT_BAND','CST_NAME','AZIMUTH','Dia ID','Data Primeiro Tráfego ID','Data Último Tráfego ID','Último Volume Dados Registrado','Semana do Ano','Hora','Classificação','Classificação2','Fator_Plan_LT','Vol_Total_Dl_Allop_LT','Throu_Pdcp_Cell_Dl_LT','Throu_User _Pdcp_Dl_LT','TPUT','Act_Ue_Data_Dl_LT','Users_Rrc_Conn_Mean_LT','Cqi_Mean_LT','Prb_Util_Mean_Dl_LT','Tti_Util_LT','Util_LT','dataArchive_x','LastClassif','LastClassif2','ADM STATE','OP STATE','EARFCNDL','BW DL','TAC','ENODEB ID','CELL ID','PCI','[S]','MIMO','dataArchive_y','ORDEM COMPLEXA','ELEMENTO ID','PROJETO','SPRINT','SETORES 4G MMIMO','FREQ 4G','REAL ATIVAÇÃO NETFLOW','PLO + OC','STATUS ATIVAÇÃO','STATUS ATIVAÇÃO2','dataArchive','FREQUÊNCIA ROLLOUT']
    fields = ['CELL_Fisico_Portal_PMO','Station ID ID_Portal_PMO', 'AZIMUTH_LOCATION_Azi_ALL','Dia ID_Portal_PMO','Municipio Nome_Portal_PMO','Municipio ID_Portal_PMO', 'ANF ID_Portal_PMO', 'BTS/NodeB/ENodeB DESC_Portal_PMO', 'Celula DESC_Portal_PMO', 'Banda DESC_Portal_PMO','CST_NAME_Portal_PMO', 'Latitude Celula ID_Portal_PMO', 'Longitude Celula ID_Portal_PMO', 'Tecnologia Sigla_Portal_PMO', 'Data Primeiro Trafego ID2_Portal_PMO','Ultimo Trafego Voz Registrado2_Portal_PMO','Ultimo Volume Dados Registrado2_Portal_PMO','ActiveCellTime(days)_Portal_PMO', 'ActiveCellTime(days)2_Portal_PMO', 'CS_STATUS_SI', 'ALTURA_SI', 'MS_TYPE_SI', 'SI_PORT_BAND_SI', 'CST_NAME_SI', 'NGNIS_DUMP', 'ADM STATE2_DUMP', 'OP STATE2_DUMP', 'FREQ CELL_DUMP', 'FREQ SITE_DUMP','CST_NAME_DUMP', 'EARFCNDL2_DUMP', 'BW DL_DUMP', 'TAC_DUMP', 'ENODEB ID_DUMP', 'PCI_DUMP', '[S]2_DUMP', 'MIMO2_DUMP', 'dataArchive_DUMP', 'Banda_CELULAS_CRITICAS','CST_NAME_CELULAS_CRITICAS','Flag Mocn_CELULAS_CRITICAS', 'Semana do Ano_CELULAS_CRITICAS', 'Classificacao_CELULAS_CRITICAS', 'TPUT_CELULAS_CRITICAS', 'Tti_Util_LT_CELULAS_CRITICAS', 'Classificacao2_CELULAS_CRITICAS','LastClassif_CELULAS_CRITICAS', 'LastClassif2_CELULAS_CRITICAS','ClassificacaoGeralW_CELULAS_CRITICAS','GeralCritico_CELULAS_CRITICAS','GeralAlerta_CELULAS_CRITICAS','GeralBom_CELULAS_CRITICAS','GeralExcelente_CELULAS_CRITICAS', 'ORDEM COMPLEXA_PMO_CellFisico', 'PROJETO_PMO_CellFisico', 'SPRINT_PMO_CellFisico', 'SETORES 4G MMIMO_PMO_CellFisico', 'FREQ 4G_PMO_CellFisico', 'REAL ATIVACAO NETFLOW_PMO_CellFisico', 'PLO + OC_PMO_CellFisico', 'STATUS ATIVACAO_PMO_CellFisico','STATUS ATIVACAO2_PMO_CellFisico', 'dataArchive_PMO_CellFisico', 'TECNOLOGIA_PMO_CellFisico', 'FREQUENCIA ROLLOUT_PMO_CellFisico','CST_NAME_PMO_CellFisico','Periodo_SmartService_EVE','count(TOTAL)_SmartService_EVE','Numero_Open_SmartService_EVE','Status_Open_SmartService_EVE','Data de Criacao_Open_SmartService_EVE','count_Open_SmartService_EVE','Periodo_SmartService_ACESSO','Numero_SmartService_ACESSO','DataInicio_SmartService_ACESSO','Status_SmartService_ACESSO','NE ID_SmartService_ACESSO','dataArchive_SmartService_ACESSO','count(TOTAL)_SmartService_ACESSO','Numero_Open_SmartService_ACESSO','DataInicio_Open_SmartService_ACESSO','NE ID_Open_SmartService_ACESSO','count_Open_SmartService_ACESSO','Periodo_TWAMP','PacketLatJitClassifLastClass_TWAMP','PacketLatJitClassifLastClassTxt_TWAMP','PacketLatJitClassifLastClassTxt2_TWAMP','DEGRADOU_TWAMP']
    pathImportSI = os.getcwd() + pathImport
    archiveName = pathImport[8:len(pathImport)]
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
    csv_path = os.path.join(script_dir, 'export/'+'GOOGLE_ALL')
    legend_path = os.path.join(script_dir, 'import/legend/'+'legend2'+'.png')
    #print ('loalding files...\n')
    all_filesSI = glob.glob(pathImportSI + "/*.csv")
    all_filesSI.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    li = []
    
    for filename in all_filesSI:
        iter_csv = pd.read_csv(filename, index_col=None, encoding="UTF-8", header=0, error_bad_lines=False,dtype=str, sep = ';',iterator=True, chunksize=10000, usecols = fields )
        df = pd.concat([chunk for chunk in iter_csv])

        df2 = df[fields] # ordering labels
        li.append(df2)
    frameSI = pd.concat(li, axis=0, ignore_index=True)
    frameSI.fillna(0,inplace=True)
   
 
    
    #exclui linhas com latitude vazia antes de rodar o loop
    frameSI = frameSI[frameSI['Latitude Celula ID_Portal_PMO'].astype(bool)]
    kml = Kml(name="GOOGLE_ALL", open=1)
    screen = kml.newscreenoverlay(name='Legends')
    screen.icon.href = legend_path
    #screen.icon.href = r'C:\Users\f8059678\OneDrive - TIM\Dario\@_PYTHON\GOOGLE_ALL\import\legend\legend.png'
    screen.overlayxy = simplekml.OverlayXY(x=0,y=1,xunits=simplekml.Units.fraction,yunits=simplekml.Units.fraction)
    screen.screenxy = simplekml.ScreenXY(x=1,y=1,xunits= simplekml.Units.pixels,yunits=simplekml.Units.insetpixels)
    screen.size.x = -1
    screen.size.y = -1
    screen.size.xunits = simplekml.Units.fraction
    screen.size.yunits = simplekml.Units.fraction


    endIDlist = []
    frameSI.insert(len(frameSI.columns),'Balanceamento','')
    frameSI.insert(len(frameSI.columns),'Criticas_Prio','')
    frameSI.insert(len(frameSI.columns),'Rollout_Prio','')
    frameSI.insert(len(frameSI.columns),'TWAMP_Prio','')
    frameSI.insert(len(frameSI.columns),'ClassificacaoGeralLastW_CELULAS_CRITICAS','Bom')

    
    for index, row in frameSI.iterrows():
        if row['Station ID ID_Portal_PMO'] not in endIDlist:
            fol = kml.newfolder(name=row['Station ID ID_Portal_PMO'])
            endIDlist.append(row['Station ID ID_Portal_PMO'])

        #fol = kml.newfolder(name=row['CELL_Fisico'])
        #pnt = fol.newpoint(name=row['CELL_Fisico'], coords =[(row['LONGITUDE'].replace(',','.'),row['LATITUDE'].replace(',','.'))])
        pol = fol.newpolygon(name=row['CELL_Fisico_Portal_PMO'])

        lat = row['Latitude Celula ID_Portal_PMO'].replace(',','.')
        lon = row['Longitude Celula ID_Portal_PMO'].replace(',','.')
        az = row['AZIMUTH_LOCATION_Azi_ALL']
        vectors = SectorGoogle.CalcPointsSector(lat,lon,az)
        pol.outerboundaryis = vectors

        pol.style.linestyle.color = simplekml.Color.green
        pol.style.linestyle.width = 5
        pol.style.polystyle.color = simplekml.Color.changealphaint(120, simplekml.Color.green)
        xf = str(row['LastClassif_CELULAS_CRITICAS']).split('|')
        st = str(row['STATUS ATIVACAO_PMO_CellFisico']).split('|')
        MS_TYPE2 = str(row['Tecnologia Sigla_Portal_PMO']).split('|')
        critico = 0
        alerta = 0
        bom = 0
        excelente = 0
        count = 0
        count4g = 0

        for gh in xf:
            if len(gh) > 2:
                if gh == 'Critico':
                    critico +=1
                    count +=1
                if gh == 'Alerta':
                    alerta +=1
                    count +=1
                if gh == 'Bom':
                    bom +=1
                    count +=1
                if gh == 'Excelente':
                    excelente +=1
                    count +=1
        
        for ms in MS_TYPE2:
            if ms == '4G':
                count4g +=1

        # NO PLO
        if row['PLO + OC_PMO_CellFisico'] == '0' or row['PLO + OC_PMO_CellFisico'] == 0 or row['STATUS ATIVACAO_PMO_CellFisico'] == 'ATIVO' :
            if critico + alerta <= excelente and critico + alerta != 0:
                pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                pol.style.linestyle.width = 5
                pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.dodgerblue)# 0 - 255
                frameSI.at[index,'Balanceamento'] = 'Balanceamento'
                frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Balanceamento'
            else:
                if critico > (count/2) and critico != 0:
                    pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                    pol.style.linestyle.width = 5
                    pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.black)
                    frameSI.at[index,'Criticas_Prio'] = 'Prio_0'
                    frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                    frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'SuperCritico'
                else:
                    if 'Critico' in xf:
                        pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                        pol.style.linestyle.width = 5
                        pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.deeppink)
                        frameSI.at[index,'Criticas_Prio'] = 'Prio_1'
                        frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                        frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Critico'
                    else:
                        if 'Alerta' in xf:
                            pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                            pol.style.linestyle.width = 5
                            pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.gold)
                            frameSI.at[index,'Criticas_Prio'] = 'Prio_2'
                            frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                            frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Alerta'
                        else:
                            if count4g > 0:
                                pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                pol.style.linestyle.width = 2
                                pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.green)
                                frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))    
                            else:
                                pol.style.linestyle.color = simplekml.Color.blue
                                pol.style.linestyle.width = 5
                                pol.style.polystyle.color = simplekml.Color.changealphaint(180, simplekml.Color.green)
                                frameSI.at[index,'Rollout_Prio'] = 'Prio_4'
        # com PMO
        else:
            if row['ActiveCellTime(days)_Portal_PMO'] == '0':
                pol.style.linestyle.color = simplekml.Color.whitesmoke
                pol.style.linestyle.width = 5
                pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.white)

            else:


                if critico + alerta <= excelente and critico + alerta != 0:
                    pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                    pol.style.linestyle.width = 1
                    pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.dodgerblue)
                    frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                    frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Balanceamento'

                else:
                    if critico > (count/2) and critico != 0:
                        pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                        pol.style.linestyle.width = 1
                        pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.black)
                        frameSI.at[index,'Rollout_Prio'] = 'Prio_0'
                        frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                        frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'SuperCritico'
                    else:
                        if 'Critico' in xf:
                            pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                            pol.style.linestyle.width = 1
                            pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.deeppink)
                            frameSI.at[index,'Rollout_Prio'] = 'Prio_1'
                            frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                            frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Critico'

                        else:
                            if 'Alerta' in xf:
                                pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                pol.style.linestyle.width = 1
                                pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.gold)
                                frameSI.at[index,'Rollout_Prio'] = 'Prio_2'
                                frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                frameSI.at[index,'ClassificacaoGeralLastW_CELULAS_CRITICAS'] = 'Alerta'
                            else:
                                if count4g > 0:
                                    pol.style.linestyle.color = TWAMPcolor2(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                    pol.style.linestyle.width = 1
                                    pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.green)
                                    frameSI.at[index,'TWAMP_Prio'] = TWAMPPrio(str(row['PacketLatJitClassifLastClass_TWAMP']))
                                    

                                else:
                                    pol.style.linestyle.color = simplekml.Color.blue
                                    pol.style.linestyle.width = 2
                                    pol.style.polystyle.color = simplekml.Color.changealphaint(160, simplekml.Color.green)
                                    frameSI.at[index,'Rollout_Prio'] = 'Prio_3'

                                

        
        removefromloop0 = ['Banda DESC_Portal_PMO','CST_NAME_Portal_PMO', 'Tecnologia Sigla', 'SI_PORT_BAND_SI', 'MS_TYPE_SI','FREQ CELL_DUMP', 'FREQ SITE_DUMP','CST_NAME_DUMP', 'BW DL_DUMP','Banda_CELULAS_CRITICAS','ClassificacaoGeralW_CELULAS_CRITICAS','GeralCritico_CELULAS_CRITICAS','GeralAlerta_CELULAS_CRITICAS','GeralBom_CELULAS_CRITICAS','GeralExcelente_CELULAS_CRITICAS','FREQUENCIA ROLLOUT_PMO_CellFisico']
        legend = []
        for t in fields:
            if t not in legend and t not in removefromloop0:
                legend.append(t)



        for i in legend:
            pol.extendeddata.newdata(name= i, value=str(row[i]), displayname=None)
        
    removefromloop = ['Station ID ID_Portal_PMO','CELL_Fisico_Portal_PMO','Classificacao2_CELULAS_CRITICAS','LastClassif2_CELULAS_CRITICAS','STATUS ATIVACAO2_PMO_CellFisico','Balanceamento','Criticas_Prio','Rollout_Prio','ANF ID_Portal_PMO','Municipio Nome_Portal_PMO','Periodo_TWAMP','PacketLatJitClassifLastClass_TWAMP','PacketLatJitClassifLastClassTxt_TWAMP','PacketLatJitClassifLastClassTxt2_TWAMP','DEGRADOU_TWAMP','TWAMP_Prio']
    locationBase_top = list(frameSI.columns)
    res = list(set(locationBase_top)^set(removefromloop))
      

    #kml.save(os.path.splitext(__file__)[0] + ".kml",format=False)
    kml.savekmz(csv_path + ".kmz",format=False)



def colorretured(value):
    if value == 'chartreuse': return simplekml.Color.chartreuse
    if value == 'chocolate': return simplekml.Color.chocolate
    if value == 'coral': return simplekml.Color.coral
    if value == 'cornflowerblue': return simplekml.Color.cornflowerblue
    if value == 'cornsilk': return simplekml.Color.cornsilk
    if value == 'crimson': return simplekml.Color.crimson
    if value == 'cyan': return simplekml.Color.cyan
    if value == 'darkblue': return simplekml.Color.darkblue
    if value == 'darkcyan': return simplekml.Color.darkcyan
    if value == 'darkgoldenrod': return simplekml.Color.darkgoldenrod
    if value == 'darkgray': return simplekml.Color.darkgray
    if value == 'darkgreen': return simplekml.Color.darkgreen
    if value == 'darkgrey': return simplekml.Color.darkgrey
    if value == 'darkkhaki': return simplekml.Color.darkkhaki
    if value == 'darkmagenta': return simplekml.Color.darkmagenta
    if value == 'darkolivegreen': return simplekml.Color.darkolivegreen
    if value == 'darkorange': return simplekml.Color.darkorange
    if value == 'darkorchid': return simplekml.Color.darkorchid
    if value == 'darkred': return simplekml.Color.darkred
    if value == 'darksalmon': return simplekml.Color.darksalmon
    if value == 'darkseagreen': return simplekml.Color.darkseagreen
    if value == 'darkslateblue': return simplekml.Color.darkslateblue
    if value == 'darkslategray': return simplekml.Color.darkslategray
    if value == 'darkslategrey': return simplekml.Color.darkslategrey
    if value == 'darkturquoise': return simplekml.Color.darkturquoise
    if value == 'darkviolet': return simplekml.Color.darkviolet
    if value == 'deeppink': return simplekml.Color.deeppink
    if value == 'deepskyblue': return simplekml.Color.deepskyblue
    if value == 'dimgray': return simplekml.Color.dimgray
    if value == 'dimgrey': return simplekml.Color.dimgrey
    if value == 'dodgerblue': return simplekml.Color.dodgerblue
    if value == 'firebrick': return simplekml.Color.firebrick
    if value == 'floralwhite': return simplekml.Color.floralwhite
    if value == 'forestgreen': return simplekml.Color.forestgreen
    if value == 'fuchsia': return simplekml.Color.fuchsia
    if value == 'gainsboro': return simplekml.Color.gainsboro
    if value == 'ghostwhite': return simplekml.Color.ghostwhite
    if value == 'gold': return simplekml.Color.gold
    if value == 'goldenrod': return simplekml.Color.goldenrod
    if value == 'gray': return simplekml.Color.gray
    if value == 'green': return simplekml.Color.green
    if value == 'greenyellow': return simplekml.Color.greenyellow
    if value == 'grey': return simplekml.Color.grey
    if value == 'white': return simplekml.Color.white
    if value == 'black': return simplekml.Color.black
    if value == 'TIM': return simplekml.Color.darkblue
    if value == 'VIVO': return simplekml.Color.purple
    if value == 'CLARO': return simplekml.Color.red
    if value == 'ALGAR': return simplekml.Color.yellow        


    

















def TWAMPcolor(listx):
    listx = listx.split('|')
    rt = []
    for i in listx:
        if i == '0':
            rt.append(0)
        if i == 'BOM':
            rt.append(1)
        if i == 'ALERTA':
            rt.append(2)        
        if i == 'CRITICO':
            rt.append(3)
        if i == 'ALTA CRITICIDADE':
            rt.append(4)

    x = np.array(rt)
    y = x.astype(np.int)
    y = np.sort(y)
    
    last = y[-1:]
    #print (y, last)

    rty = simplekml.Color.green
    if last == 2:
        rty = simplekml.Color.yellow
    if last == 3:
        rty = simplekml.Color.red
    if last == 4:
        rty = simplekml.Color.black    

    return rty

def TWAMPcolor2(listx):
    listx = listx.split('|')
    rt = []
    for i in listx:
        if i == '0':
            rt.append(0)
        if i == 'BOM':
            rt.append(1)
        if i == 'ALERTA':
            rt.append(2)        
        if i == 'CRITICO':
            rt.append(3)
        if i == 'ALTA CRITICIDADE':
            rt.append(4)

    x = np.array(rt)
    y = x.astype(np.int)
    y = np.sort(y)
    
    last = y[-1:]
    #print (y, last)

    rty = simplekml.Color.green
    if last == 2:
        rty = simplekml.Color.gold
    if last == 3:
        rty = simplekml.Color.deeppink
    if last == 4:
        rty = simplekml.Color.black    

    return rty




def TWAMPPrio(listx):
    listx = listx.split('|')
    rt = []
    for i in listx:
        if i == '0':
            rt.append(0)
        if i == 'BOM':
            rt.append(1)
        if i == 'ALERTA':
            rt.append(2)        
        if i == 'CRITICO':
            rt.append(3)
        if i == 'ALTA CRITICIDADE':
            rt.append(4)

    x = np.array(rt)
    y = x.astype(np.int)
    y = np.sort(y)
    
    last = y[-1:]
    #print (y, last)

    rty = "Prio_4"
    if last == 1:
        rty = 'Prio_3'
    if last == 2:
        rty = 'Prio_2'
    if last == 3:
        rty = 'Prio_1'
    if last == 4:
        rty = 'Prio_0'    

    return rty