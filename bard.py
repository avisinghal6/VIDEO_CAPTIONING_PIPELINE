from Bard import Chatbot
token = "VAhopPDCHWYe9Xi1QJxKeZiCew4H1hBup3Ggrpj3W4ZHlgCnyAmvNo9-k9ZLb6uuw1E7xw."
chatbot = Chatbot(token)

def get_captions_from_bard(captions):
  for i in captions:
    bard_output = chatbot.ask('Given a text, rephrase each sentence, give only instructions of a recipe, do not give additional tips and ingredients:\
              text: '+ captions[i])
    bard_output = bard_output['content'].lower()
    captions[i] = bard_output
  return captions