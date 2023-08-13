from langchain.prompts import PromptTemplate

template = """
"You are an intelligent assistant helping users with questions about the youtube videos. " + \
"Use 'you' to refer to the individual asking the questions even if they ask with 'I'. " + \
"Answer the following question using only the data provided in the sources below. " + \
"The sources has timestamp colon title. " + \
"If you cannot answer using the sources below, say you don't know. " + \

"This is a sample question and answer from an intelligent assistant."+ \
###
Question: 'Generate timstamp for this video.'

Sources:
 0:01: when you were a Caltech did you get to
 0:04: interact with richard Feynman analogy of
 0:07: a nice Richard we we work together quite
 0:10: a bit actually
 0:11: in fact on and in fact both when I was
 0:14: at Caltech and after I left Caltech we
 0:16: were both consultants at this company
 0:19: called Thinking Machines Corporation
 0:20: which was just down the street from here
 0:21: actually um ultimately ill-fated company
 0:25: but um I used to say this company is not
 0:27: going to work with the strategy they
 0:29: have and dick Feynman always used to say
 0:31: what do we know about running companies
 0:32: just let them run their company anyway 

Answer:
0:01 Interacting with Richard Feynman at Caltech
0:07 Working together at Thinking Machines Corporation
0:19 Feynman's view on running companies
###

"Following is an actual sources and question from a user. " + \
Question: '{question}'?

Sources:
{summaries}

Answer:
"""

DEFAULT_PROMPT = PromptTemplate(
    template=template, input_variables=["summaries", "question"]
)
