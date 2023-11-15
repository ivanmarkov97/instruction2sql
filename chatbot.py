import os

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from prompt2db.hf_hub import HFHub


if __name__ == '__main__':
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = ''
    model_name = 'google/flan-t5-large'
    model_params = {'temperature': 0.7, 'max_length': 120}

    prompt_template = PromptTemplate(
        template="""
        You have to SQL tables:
        
        create table items (
            item_id INT NOT NULL,
            name VARCHAR(60) NOT NULL,
            price FLOAT NOT NULL
        );
        
        create table orders (
            order_id INT NOT NULL,
            item_id INT NOT NULL,
            date DATE NOT NULL
        );
        
        Question: {question}
        Answer: 
        """,
        input_variables=['question']
    )

    llm_model = HFHub().load_model(model_name, model_params)
    llm = LLMChain(prompt=prompt_template, llm=llm_model)

    response = llm.run(
        'Write SQL query that shows all rows.'
    )
    print(response)
