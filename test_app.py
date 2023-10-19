import openai

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
from decouple import config


reference_text = """ Chat bot will create collect the data and create the case and assign to corresponding queue.

It integrates with other Salesforce products and can be customized to meet the specific needs of a business. customer has question and chat bot will look into company knowledge base docs and reply back with answer.

The chatbot can be deployed on company websites, mobile apps, messaging platforms, and other customer touchpoints. This bot interacts with salesforce service and sales cloud.

It can handle multiple languages and can be trained on a company’s specific language and terminology. This feature is super helpful who had the multiple languages related customers."""




def ask_question(question, reference_file):
    #with open(reference_file, "r",encoding='utf-8') as file:
    #    context = file.read()
    context = reference_file
    prompt = f"question: {question}\ncontext: {context}\nanswer:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100,
        n=1,
        stop=None,
        
    )

    answer = response.choices[0].text.strip().split("\n")[0]

    return answer
    
    

app = dash.Dash()
server = app.server


text_prompt = dcc.Input(id='text-prompt', type='text', placeholder='Enter a question.')
submit_button = html.Button('Submit', id='submit-button')
output_area = html.Div(id='output-area')

app.layout = html.Div([
    html.H3(config('OPENAI_API_KEY2')))
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
])

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
    ##print (config('OPENAI_API_KEY2'))
    app.run_server(debug=True)
