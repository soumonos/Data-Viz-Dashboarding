# Importing dependencies

import jupyterlab_dash
import dash
import dash_html_components as html
import dash_core_components as dcc
import seaborn as sns
from dash.dependencies import Output,Input
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import os

# Reading the first dataset

df= pd.read_csv("bank-full.csv",sep=";")
df_cat= df.select_dtypes(include=['object'])
df_cat.rename(columns={'y':'substat'})
df_cont= df.select_dtypes(include=['int64'])
df_cont['substat']= df['y']
df_contc= df_cont.drop(columns=['campaign','pdays','previous'])
df_cont_bi=df_contc.copy()
df_cont_bi['substat']= df_cat['y']

# Reading the second dataset
df_port= pd.read_csv("portugal mod.csv")
df_port.drop(columns=['Unnamed: 1','Unnamed: 3','Country Name'],inplace=True)
df_port.head()
l= list(df_port['Indicator Name'])
dfff= pd.DataFrame(df_port.transpose())
df_f= dfff[1:]
df_f.columns= l
df_f.head()
df_f.reset_index(inplace=True)
df_mod1= df_f.astype(int)




#Starting Dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout =html.Div(children= [
	html.H1('Case study: A Bank marketing campaign in Portugal and Economic indicator of the Nation',style= {'textAlign' : 'center'}),
	html.H2('By Soumonos Mukherjee',style= {'fontSize': 20,'textAlign' : 'center'}),
	html.Div([
	    html.Div([
	        html.Div([
	        	html.H3('Univariate analysis for categorical features. Plot type: CountPlot',style={'color': 'black', 'fontSize': 20,'textAlign':'center'}),
	        	html.P('Choose an option:'),
	            dcc.Dropdown(id="dropdown1",
	                options= [
	                          {'label':"Job status", 'value':"job"},
	                          {'label':"Marital status", 'value':"marital"},
	                          {'label':"Education-level",'value':"education"},
	                          {'label':"Defaulter's-status",'value':"default"},
	                          {'label':"Loan-history",'value':"loan"},
	                          {'label':"Contact-method",'value':"contact"},
	                          {'label':"Contact-month",'value':"month"},
	                          {'label':"Outcome in the previous campaign",'value':"poutcome"},
	                          {'label':"Subscription status",'value':"y"}
	                    ],
	                    optionHeight= 35,
	                    value= "job",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),

	        html.Div([
	            dcc.Graph(id="univariate1")
	        ]),
	    ], className="six columns"),
	    html.Div([    
	        html.Div([
	        	html.H3('Univariate analysis for Numerical features. Plot type: Histogram',style={'color': 'black', 'fontSize': 20,'textAlign':'center'}),
	        	html.P('Choose an option:'),
	            dcc.Dropdown(id="dropdown2",
	                options= [
	                          {'label':"Age ", 'value':"age"},
	                          {'label':"Bank Balance ", 'value':"balance"},
	                          {'label':"Total num of days contacted",'value':"day"},
	                          {'label':"last contact duration(sec)",'value':"duration"},
	                          {'label':"number of times client contacted during campaign",'value':"campaign"},
	                          {'label':"number of times client contacted previously",'value':"previous"}

	                    ],
	                    optionHeight= 35,
	                    value= "age",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),
	        html.Div([
	            dcc.Graph(id="univariate2")
	        ]),
	    ], className= "six columns"),
	],className="row"),
    html.Div([
	    html.Div([
	          html.Div([
	          	html.H3('Bivariate Analysis- Categorical vs Numerical. Plot type: Box plots',style={'color': 'black', 'fontSize': 20,'textAlign':'center'}),
		        html.P('Choose X axis (Categorical):'),
	            dcc.Dropdown(id="xcolumnbar",
	                options= [
	                          {'label':"Job status", 'value':"job"},
	                          {'label':"Marital status", 'value':"marital"},
	                          {'label':"Education-level",'value':"education"},
	                          {'label':"Defaulter's-status",'value':"default"},
	                          {'label':"Loan-history",'value':"loan"},
	                          {'label':"Contact-method",'value':"contact"},
	                          {'label':"Contact-month",'value':"month"},
	                          {'label':"Outcome in the previous campaign",'value':"poutcome"},
	                          {'label':"Subscription status",'value':"y"}

	                    ],
	                    optionHeight= 35,
	                    value= "job",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),
	        html.Div([
	        	html.P('Choose Y axis (Numerical):'),
	            dcc.Dropdown(id="ycolumnbar",
	                options= [
	                          {'label':"Age ", 'value':"age"},
	                          {'label':"Bank Balance ", 'value':"balance"},
	                          {'label':"Total num of days contacted",'value':"day"},
	                          {'label':"last contact duration(sec)",'value':"duration"},
	                          {'label':"number of times client contacted during campaign",'value':"campaign"},
	                          {'label':"number of times client contacted previously",'value':"previous"}

	                    ],
	                    optionHeight= 35,
	                    value= "age",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),
	        html.Div([
	        	html.P('Choose a grouping variable (categorical):'),
	            dcc.Dropdown(id="groupbar",
	                options= [
	                          {'label':"Job status", 'value':"job"},
	                          {'label':"Marital status", 'value':"marital"},
	                          {'label':"Education-level",'value':"education"},
	                          {'label':"Defaulter's-status",'value':"default"},
	                          {'label':"Loan-history",'value':"loan"},
	                          {'label':"Contact-method",'value':"contact"},
	                          {'label':"Contact-month",'value':"month"},
	                          {'label':"Outcome in the previous campaign",'value':"poutcome"},
	                          {'label':"Subscription status",'value':"y"}

	                    ],
	                    optionHeight= 35,
	                    value= "marital",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),
	        html.Div([
	            dcc.Graph(id="bivariate1")
	        ]),
	    ],className= "six columns"),
	     html.Div([
	          html.Div([
	          	html.H3('Bivariate Analysis- Numerical vs Numerical. Plot type: Bubble plot',style={'color': 'black', 'fontSize': 20,'textAlign':'center'}),
		        html.P('Choose X axis:'),
	            dcc.Dropdown(id="xcolumnbub",
	                options= [
	                          {'label':"Age ", 'value':"age"},
	                          {'label':"Bank Balance ", 'value':"balance"},
	                          {'label':"Total num of days contacted",'value':"day"},
	                          {'label':"last contact duration(sec)",'value':"duration"},
	                          {'label':"number of times client contacted during campaign",'value':"campaign"},
	                          {'label':"number of times client contacted previously",'value':"previous"}

	                    ],
	                    optionHeight= 35,
	                    value= "age",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),
	        html.Div([
	        	html.P('Choose Y axis:'),
	            dcc.Dropdown(id="ycolumnbub",
	                options= [
	                          {'label':"Age ", 'value':"age"},
	                          {'label':"Bank Balance ", 'value':"balance"},
	                          {'label':"Total num of days contacted",'value':"day"},
	                          {'label':"last contact duration(sec)",'value':"duration"},
	                          {'label':"number of times client contacted during campaign",'value':"campaign"},
	                          {'label':"number of times client contacted previously",'value':"previous"}

	                    ],
	                    optionHeight= 35,
	                    value= "duration",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),
	        html.Div([
	        	html.P('Choose 1st grouping variable (size-wise):'),
	            dcc.Dropdown(id="sizebub",
	                options= [
	                          {'label':"Age ", 'value':"age"},
	                          {'label':"Bank Balance ", 'value':"balance"},
	                          {'label':"Total num of days contacted",'value':"day"},
	                          {'label':"last contact duration(sec)",'value':"duration"},
	                          {'label':"number of times client contacted during campaign",'value':"campaign"},
	                          {'label':"number of times client contacted previously",'value':"previous"}

	                    ],
	                    optionHeight= 35,
	                    value= "day",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),
	        html.Div([
	        	html.P('Choose 2nd grouping variable (Color-wise):'),
	            dcc.Dropdown(id="groupbub",
	                options= [
	                          {'label':"Job status", 'value':"job"},
	                          {'label':"Marital status", 'value':"marital"},
	                          {'label':"Education-level",'value':"education"},
	                          {'label':"Defaulter's-status",'value':"default"},
	                          {'label':"Loan-history",'value':"loan"},
	                          {'label':"Contact-method",'value':"contact"},
	                          {'label':"Contact-month",'value':"month"},
	                          {'label':"Outcome in the previous campaign",'value':"poutcome"},
	                          {'label':"Subscription status",'value':"y"}

	                    ],
	                    optionHeight= 35,
	                    value= "job",
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select...",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),
	        html.Div([
	            dcc.Graph(id="bubbleplot")
	        ]),
	    ],className= "six columns"),
], className= "row"),
html.Div([
    html.Div([    
        html.Div([
        	html.H3('Trivariate Analysis- All Numericals. Plot type: 3D Scatter Plot',style={'color': 'black', 'fontSize': 20,'textAlign':'center'}),
	        html.P('Choose X axis:'),
            dcc.Dropdown(id="xcolumn",
                options= [
                          {'label':"Age ", 'value':"age"},
                          {'label':"Bank Balance ", 'value':"balance"},
                          {'label':"Total num of days contacted",'value':"day"},
                          {'label':"last contact duration(sec)",'value':"duration"},
                          {'label':"number of times client contacted during campaign",'value':"campaign"},
                          {'label':"number of times client contacted previously",'value':"previous"}

                    ],
                    optionHeight= 35,
                    value= "age",
                    disabled= False,
                    multi= False,
                    searchable= True,
                    search_value= '',
                    placeholder= "Please select the X axis",
                    clearable= True,
                    style= {'width':"100%"},
                    persistence= True,
                    persistence_type= "memory"
             ),
        ]),  
        html.Div([
        	html.P('Choose Y axis:'),
            dcc.Dropdown(id="ycolumn",
                options= [
                          {'label':"Age ", 'value':"age"},
                          {'label':"Bank Balance ", 'value':"balance"},
                          {'label':"Total num of days contacted",'value':"day"},
                          {'label':"last contact duration(sec)",'value':"duration"},
                          {'label':"number of times client contacted during campaign",'value':"campaign"},
                          {'label':"number of times client contacted previously",'value':"previous"}
                          
                    ],
                    optionHeight= 35,
                    value= "balance",
                    disabled= False,
                    multi= False,
                    searchable= True,
                    search_value= '',
                    placeholder= "Please select the Y axis",
                    clearable= True,
                    style= {'width':"100%"},
                    persistence= True,
                    persistence_type= "memory"
             ),
        ]), 
        html.Div([
        	html.P('Choose Z axis:'),
            dcc.Dropdown(id="zcolumn",
                options= [
                          {'label':"Age ", 'value':"age"},
                          {'label':"Bank Balance ", 'value':"balance"},
                          {'label':"Total num of days contacted",'value':"day"},
                          {'label':"last contact duration(sec)",'value':"duration"},
                          {'label':"number of times client contacted during campaign",'value':"campaign"},
                          {'label':"number of times client contacted previously",'value':"previous"}
                          
                    ],
                    optionHeight= 35,
                    value= "day",
                    disabled= False,
                    multi= False,
                    searchable= True,
                    search_value= '',
                    placeholder= "Please select the Z axis",
                    clearable= True,
                    style= {'width':"100%"},
                    persistence= True,
                    persistence_type= "memory"
             ),
        ]),  
        html.Div([
        	html.P('Choose 1st grouping variable (Color-wise):'),
            dcc.Dropdown(id="grouping1",
                options= [
                          {'label': "No, I don't want to select one", 'value':None},
                          {'label':"Job status", 'value':"job"},
                          {'label':"Marital status", 'value':"marital"},
                          {'label':"Education-level",'value':"education"},
                          {'label':"Defaulter's-status",'value':"default"},
                          {'label':"Loan-history",'value':"loan"},
                          {'label':"Contact-method",'value':"contact"},
                          {'label':"Contact-month",'value':"month"},
                          {'label':"Outcome in the previous campaign",'value':"poutcome"},
                          {'label':"Subscription status",'value':"substat"}

                    ],
                    optionHeight= 35,
                    value= "marital",
                    disabled= False,
                    multi= False,
                    searchable= True,
                    search_value= '',
                    placeholder= "Please select a grouping variable",
                    clearable= True,
                    style= {'width':"100%"},
                    persistence= True,
                    persistence_type= "memory"
             ),
        ]),    
        html.Div([
        	html.P('Choose 2nd grouping variable (Symbol-wise):'),
            dcc.Dropdown(id="grouping2",
                options= [
                          {'label': "No, I don't want to select one", 'value':None},
                          {'label':"Job status", 'value':"job"},
                          {'label':"Marital status", 'value':"marital"},
                          {'label':"Education-level",'value':"education"},
                          {'label':"Defaulter's-status",'value':"default"},
                          {'label':"Loan-history",'value':"loan"},
                          {'label':"Contact-method",'value':"contact"},
                          {'label':"Contact-month",'value':"month"},
                          {'label':"Outcome in the previous campaign",'value':"poutcome"},
                          {'label':"Subscription status",'value':"y"}

                    ],
                    optionHeight= 35,
                    value= "education",
                    disabled= False,
                    multi= False,
                    searchable= True,
                    search_value= '',
                    placeholder= "Please select a second grouping variable",
                    clearable= True,
                    style= {'width':"100%"},
                    persistence= True,
                    persistence_type= "memory"
             ),
        ]),
        html.Div([
            dcc.Graph(id="scatterplot")
        ]),
    ],className="six columns"),
		html.Div([
			html.Div([
				html.H3('Economic indicator on Portugal (Timeseries- Merchendise import from Mid-Low economic nations of following regions as percentage of Total merchandise import ',style={'color': 'black', 'fontSize': 20,'textAlign':'center'}),
		        html.P('Choose a region:'),
	            dcc.Dropdown(id="line1",
	                options= [
	  
	                          {'label':"From Subsaharan Africa", 'value':' Sub-Saharan Africa '},
	                          {'label':"From South Asia", 'value':' South Asia'},
	                          {'label':"From Middle East and North Africa ",'value':'Middle East & North Africa '},
	                          {'label':"From Latin America and The Caribbean",'value':' Latin America & the Caribbean'},
	                          {'label':"From Europe & Central Asia",'value':' Europe & Central Asia '},
	                          {'label':"From East Asia & Pacific",'value':' East Asia & Pacific '},
	                          {'label':"From outside region",'value':' outside region '}

	                    ],
	                    optionHeight= 35,
	                    value= ' Sub-Saharan Africa ',
	                    disabled= False,
	                    multi= False,
	                    searchable= True,
	                    search_value= '',
	                    placeholder= "Please select a second grouping variable",
	                    clearable= True,
	                    style= {'width':"100%"},
	                    persistence= True,
	                    persistence_type= "memory"
	             ),
	        ]),    
	        html.Div([
	        	dcc.Graph(id="Lineplot")
	        ]),
	    ],className="six columns"),
	],className="row"),

],style={'width': '100%', 'display': 'inline-block'})

@app.callback(
        dash.dependencies.Output(component_id="univariate1",component_property="figure"),
        [dash.dependencies.Input(component_id="dropdown1",component_property="value")]

)


def build_univariate_cat(column_chosen):
    dff= df_cat.copy()
    #barplot= sns.barplot(data=dff,x=list(dict(dropdown1.value_counts()).keys()),y=list(dict(dropdown1.value_counts()).values()))
    hist= px.histogram(dff,x=column_chosen,color=column_chosen,color_discrete_sequence=px.colors.qualitative.G10)
    return (hist)

@app.callback(
        dash.dependencies.Output(component_id="univariate2",component_property="figure"),
        [dash.dependencies.Input(component_id="dropdown2",component_property="value")]
)
    
def build_univariate_cont(col_chos):
    dff1= df_cont.copy()
    dff_us= dff1.sort_values(by=[col_chos],ascending=False).head(2000)
    dist= px.histogram(dff_us,x=col_chos) #dist= ff.create_distplot(list(dff1[col_chos]))
    return (dist)

@app.callback(
        dash.dependencies.Output(component_id="bivariate1",component_property="figure"),
        [dash.dependencies.Input(component_id="xcolumnbar",component_property="value"),
         dash.dependencies.Input(component_id="ycolumnbar",component_property="value"),
         dash.dependencies.Input(component_id="groupbar",component_property="value")]

)

def build_bivariate_cont(xcolb,ycolb,grb):
    dff2= df.copy()
    biv1= px.box(dff2,x= xcolb,y= ycolb,color=grb,notched=True)
    return (biv1)
@app.callback(
        dash.dependencies.Output(component_id="bubbleplot",component_property="figure"),
        [dash.dependencies.Input(component_id="xcolumnbub",component_property="value"),
         dash.dependencies.Input(component_id="ycolumnbub",component_property="value"),
         dash.dependencies.Input(component_id="sizebub",component_property="value"),
         dash.dependencies.Input(component_id="groupbub",component_property="value")]

)
def build_bubble(xcolbb,ycolbb,sizebb,grbb):
    dffbub= df.copy()
    dffinal1= dffbub.sort_values(by= xcolbb, ascending=False).head(2000)
    biv2= px.scatter(dffinal1, x=xcolbb,y=ycolbb,size=sizebb,color=grbb)
    return (biv2)


@app.callback(
        dash.dependencies.Output(component_id="scatterplot",component_property="figure"),
        [dash.dependencies.Input(component_id="xcolumn",component_property="value"),
         dash.dependencies.Input(component_id="ycolumn",component_property="value"),
         dash.dependencies.Input(component_id="zcolumn",component_property="value"),
         dash.dependencies.Input(component_id="grouping1",component_property="value"),
         dash.dependencies.Input(component_id="grouping2",component_property="value")]
)

def build_scatter3d(xcol,ycol,zcol,group1,group2):
    dff3= df.copy()
    dffinal2= dff3.sort_values(by= xcol, ascending=False).head(2000)
    visul= px.scatter_3d(dffinal2, x= xcol, y=ycol,z=zcol, color=group1, symbol= group2, opacity=0.8)
    return (visul)
@app.callback(
        dash.dependencies.Output(component_id="Lineplot",component_property="figure"),
        [dash.dependencies.Input(component_id="line1",component_property="value")]

)

def build_lineplot(val):
	figline = go.Figure()
	figline.add_trace(go.Scatter(x=df_mod1['index'], y=df_mod1[val],mode='lines+markers',name= val))
	figline.update_xaxes(rangeslider_visible= True)
	return(figline)



if __name__=='__main__':
    app.run_server(port=4050)