import openai

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
from decouple import config


reference_text = """ CDP - The Automated Algorithm Next generation data solutions are required to stay ahead in the marketplace Introduction Modern customer engagement requires a different approach to succeed.________________The customer experience has shifted significantly over the past decade due to disruptive shifts in buying patterns, technology innovation and a dynamic global marketplace that is ever more interconnected. Today’s customers have in many cases what seem to be infinite choices among highly personalized experiences throughout their customer journey. This happens at every touch point and across multiple channels. Those who create, sell and distribute products have had to significantly evolve their business models to staycompetitive and increasingly invest in tools and processes to stay in touch and relevant with customers. Massive amounts of customer data is being generated and collected across multiple sources from websites, digital channels and campaigns to mobile applications. Also the very product itself that consumers areusing is generating data. Retailers who sell, manufacturers who build and organizations that market products and services have more potential insights than ever. The problem is not in accessing the data, it’s in creating an operational model based on data to make effective decisions at scale. Responding to a customer insight at scale is very difficult to do when the view is fragmented across multiple channels, products, touch points and regions. In some scenarios it’s possible to develop a true customer insight orunderstanding but it comes long after it’s relevant - often at the point of trying to understand why a customer was lost. Furthermore developing a personalized customer experience at scale is very difficult when other factors such as old data, disconnected systems and processes and integration complexities are factored into the mix. These operational disconnects can lead to an unhappy customer, disconnected experience and deliver a below"""


api_key = os.environ.get('OPENAI_API_KEY2')

def ask_question(question, reference_file):
    #with open(reference_file, "r",encoding='utf-8') as file:
    #    context = file.read()
    context = reference_file
    prompt = f"question: {question}\ncontext: {context}\nanswer:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=3000,
        api_key = api_key,
        n=1,
        stop=None,
        
    )

    #answer = response.choices[0].text.strip().split("\n") + "\n" + response.choices[1].text.strip().split("\n")
    answer = response.choices[0].text.strip().split("\n")
    answer.append("\n")
    answer.append(response.choices[1].text.strip().split("\n"))
    
    return answer
    
    

app = dash.Dash()
server = app.server



#print ("the api keys are                                            :   ",api_key)
#print ("--------------------------------------------------------------------------")
text_prompt = dcc.Input(id='text-prompt', type='text', placeholder='Enter a question.', style={'width':'100px'})
submit_button = html.Button('Submit', id='submit-button')
output_area = html.Div(id='output-area')

app.layout = html.Div([
    #html.H3("Enter Prompt"),
    text_prompt, 
    html.Br(),
    html.Br(),
    submit_button,
    html.Br(),
    html.Br(),
    #output_area
    
    dcc.Loading(
        id="load-genai",
        type="default",
        children=

            html.Div(id="load-output-genai",children = [html.Div(id="output-area",className="row",style={'whiteSpace': 'pre-line'})], className="pretty_container"),                  
        ),
], style={'font-size': '18px',‘font-family’:‘Arial’})

@app.callback(
    Output('output-area', 'children'),
    Input('submit-button', 'n_clicks'),
    State('text-prompt', 'value')
)
def update_output(n_clicks, text_prompt_value):
    if n_clicks > 0:
        # TODO: Process the text prompt value and generate an output.
        output = 'This is the output of the text prompt "' + text_prompt_value + '".'
        output =  ask_question(text_prompt_value, reference_text)
        return output
    else:
        return ''

if __name__ == '__main__':
    #print (config('OPENAI_API_KEY2'))
    app.run_server(debug=True)
