import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from spacy.matcher import Matcher
from spacy.tokens import Span
from fuzzywuzzy import fuzz


nlp = spacy.load("en_core_web_sm")

# Define the training data as a list of Examples
training_data = []

def Train(intents):
    global nlp
    for intent, data in intents.items():
        for pattern in data["patterns"]:
            doc = nlp.make_doc(pattern)
            example = Example.from_dict(doc, {"cats": {intent: 1.0}})
            training_data.append(example)

    # Initialize the spaCy model and create the pipeline
    nlp = spacy.blank("en")

    ner = nlp.create_pipe("ner")
    nlp.add_pipe("ner", last=True)

    for intent in intents:
        ner.add_label(intent)

    # Train the model
    nlp.begin_training()
    for i in range(20):
        losses = {}
        batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            nlp.update(batch, losses=losses, drop=0.5)


# Define the chatbot function
def chatbot(intents, text):
    global nlp
    # Load the saved model if it exists, otherwise train a new model
    try:
        nlp = spacy.load("chatbot_model")
    except OSError:
        Train(intents)
        nlp.to_disk("chatbot_model")
    # Train(intents)
    # Define the matcher to find keywords in user input
    matcher = Matcher(nlp.vocab)
    for intent, data in intents.items():
        for pattern in data["patterns"]:
            # matcher.add(intent, [[{"LOWER": token.lower()} for token in pattern.split()]])
            matcher.add(intent, [[{"LOWER": {"IN": [pattern.lower()]}}]])
    doc = nlp(text)
    matches = matcher(doc)
    max_score = -1
    max_intent = None
    for intent, start, end in matches:
        span = Span(doc, start, end, label=intent)
        doc.ents = list(doc.ents) + [span]
    for ent in doc.ents:
        if ent.label_ in intents:
            return intents[ent.label_]["responses"][0]
    for intent, data in intents.items():
        for pattern in data["patterns"]:
            score = fuzz.partial_ratio(text.lower(), pattern.lower())
            if score > max_score:
                max_score = score
                max_intent = intent
    if max_score > 70: # threshold for fuzzy matching
        return intents[max_intent]["responses"][0]
    else:
        return "I'm sorry, I don't understand. Can you rephrase?"
