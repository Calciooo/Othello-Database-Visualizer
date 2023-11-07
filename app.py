from shiny import ui, render, App, reactive
import shinyswatch
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel('othello.xlsx',sheet_name=1)
df = pd.DataFrame.dropna(df,axis=0,how='all')
df = pd.DataFrame.dropna(df,axis=1,how='all')


speakers = df['SPEAKER'].unique()
speakers_dict = {'all':'EVERYONE'}
for i in speakers:
    if not pd.isnull(i):
        speakers_dict[i]=i

addressee = df['ADDRESSEE'].unique()
addressee_dict = {'all':'EVERYONE'}
for i in addressee:
    if not pd.isnull(i):
        addressee_dict[i]=i


logic = df['LOGIC'].unique()
logic_dict = {'all':'ALL'}
for i in logic:
    if not pd.isnull(i):
        logic_dict[i]=i
        
#Logic Grouping
for j in range(5,7):
    for i in range(248):
        if not pd.isnull(df.iloc[i,5]):
            df.iloc[i,4]=str(df.iloc[i,4])+", "+str(df.iloc[i,5])
    df.drop(columns="Unnamed: "+str(j),inplace=True)


df['SEMANTICS']=df['SEMANTICS'].str.strip()
sem = df['SEMANTICS'].unique()
sem_dict = {'all':'ALL'}
for i in sem:
    if not pd.isnull(i):
        sem_dict[i]=i
        
#Semantics Grouping
for j in range(8,11):
    for i in range(248):
        if not pd.isnull(df.iloc[i,6]):
            df.iloc[i,5]=str(df.iloc[i,5])+", "+str(df.iloc[i,6])
    df.drop(columns="Unnamed: "+str(j),inplace=True)

#Words Grouping
for j in range(12,25):
    for i in range(248):
        if not pd.isnull(df.iloc[i,7]):
            df.iloc[i,6]=str(df.iloc[i,6])+", "+str(df.iloc[i,7])
    df.drop(columns="Unnamed: "+str(j),inplace=True)


df.dropna(subset='SPEAKER',inplace=True,axis=0)



















#UI
app_ui = ui.page_fluid(
    shinyswatch.theme.darkly(),
    
    # ui.input_select(
    #     "selection_mode",
    #     "Selection mode",
    #     {"none": "(None)", "single": "Single", "multiple": "Multiple"},
    #     selected="none",
    # ), 

    ui.row(
        # ui.column(
        #     2, 
        #     ui.input_switch(
        #         "display_speakers", 
        #         ui.tags.h5(ui.HTML("<b>Speaker Frequency</b>")), 
        #         True
        #     ),
        #     ui.input_switch(
        #         "display_addressee", 
        #         ui.tags.h5(ui.HTML("<b>Addressee Frequency</b>")), 
        #         True
        #     ),     
        #     ui.input_switch(
        #         "display_logic", 
        #         ui.tags.h5(ui.HTML("<b>Logic Frequency</b>")), 
        #         True
        #     ),
        #     ui.input_switch(
        #         "display_semantics", 
        #         ui.tags.h5(ui.HTML("<b>Semantics Frequency</b>")), 
        #         True
        #     )      
        # ),
        
        #ui.column(3, ui.output_plot("speaker_plot")),
        #ui.column(3, ui.output_plot("addressee_plot")),
        ui.column(4, ui.output_plot("logic_plot")),
        ui.column(8, ui.output_plot("sem_plot")),
    ),


    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select(
                "speaker",
                ui.HTML("<em><b>Speaker</b></em>"),   
                speakers_dict,
                selected="all"
            ),
            
            ui.input_select(
                "addressee",
                ui.HTML("<em><b>Addressee</b></em>"),   
                addressee_dict,
                selected="all"
            ),
            
            ui.input_select(
                "logic",
                ui.HTML("<em><b>Logic</b></em>"),   
                logic_dict,
                selected="all"
            ),

            ui.input_select(
                "sem",
                ui.HTML("<em><b>Semantics</b></em>"),   
                sem_dict,
                selected="all"
            ),
            
            ui.input_slider(
                id="size",
                label="Graph Size",
                min=0,
                max=12,
                value=4,                
            ),
            
            width=3,
        ),
        
        ui.panel_main(
            ui.output_data_frame("grid"),
        )
    )
)




















#SERVER
def server(input, output, session):
    
    @reactive.Calc
    def r():
        if input.speaker() == "all":
            out = df
        else:
            out = df[df.SPEAKER==input.speaker()]
        
        if input.addressee() =="all":
            out = out
        else:
            out = out[out.ADDRESSEE==input.addressee()]
        
        if input.logic() =="all":
            out = out
        else:            
            out = out[out['LOGIC'].str.contains(input.logic(), na=False)] 
        
        if input.sem() =="all":
            out = out
        else:            
            out = out[out['SEMANTICS'].str.contains(input.sem(), na=False)]
        
        
        return out
        
        
    @output    
    @render.data_frame
    def grid():
        return render.DataGrid(
            r(),
            #row_selection_mode=input.selection_mode(),
            height=None,
            width='100%',
            summary=False
        )
        
    @output
    @render.plot(alt="Speakers Graph")
    def speaker_plot():
        data = r().value_counts('SPEAKER')   
        if len(data)==0:
            return    
        if input.display_speakers(): return data.plot(kind='bar',color='mediumaquamarine')  
        else: return
        
    @output
    @render.plot(alt="Addressee Graph")
    def addressee_plot():
        data = r().value_counts('ADDRESSEE')    
        if len(data)==0:
            return
        if input.display_addressee(): return data.plot(kind='bar',color='mediumaquamarine')  
        else: return

    @output
    @render.plot(alt="Logic Graph")
    def logic_plot():
        data = r().value_counts('LOGIC')
        if len(data)==0:
            return       
        #if input.display_logic(): 
        return data.plot(kind='bar',color='mediumaquamarine')  
        #else: return
    
    @output
    @render.plot(alt="Semantics Graph")
    def sem_plot():
        data = r().value_counts('SEMANTICS')
        if len(data)==0:
            return       
        #if input.display_semantics(): 
        return data.plot(kind='bar',color='mediumaquamarine')  
        #else: return
    
app = App(app_ui, server)

