from youtube_comments import get_comments
from gensim import corpora, models
import pprint
from gensim.utils import simple_preprocess


def get_topics(video_id:str):
    comments = get_comments(video_id)
    # Create a dictionary from the preprocessed comments
    preprocessed_comments = [simple_preprocess(comment, deacc=True) for comment in comments]

    dictionary = corpora.Dictionary(preprocessed_comments)

    # Create a document-term matrix
    doc_term_matrix = [dictionary.doc2bow(comment) for comment in preprocessed_comments]

    # Define the number of topics
    num_topics = 5

    # Build the LDA model
    lda_model = models.LdaModel(
        corpus=doc_term_matrix,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,  # for reproducibility
        passes=10,        # number of iterations over the corpus
    )

    # Print the topics and their top words
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(lda_model.print_topics(num_topics=num_topics, num_words=5))

    # Assign topics to comments
    comment_topics = []
    for doc in doc_term_matrix:
        topics = lda_model[doc]
        comment_topics.append(topics)

        topic_lab = [max(topics, key=lambda x: x[1])[0] for topics in comment_topics]

    topic_comments = {i:[] for i in range(5)}
    topics_num = {i:0 for i in range(5)}

    for i, topic in enumerate(comment_topics):
        prob = float(max(topic, key=lambda x: x[1])[1])
        topics_num[topic_lab[i]]+=1
        topic_comments[topic_lab[i]].append([comments[i],prob])


    for i in range(5):
        topic_comments[i]=sorted(topic_comments[i], key=lambda x:x[1],reverse=True)[:5]

    topics = {"top_topics":topic_comments,"topic_num":topics_num}
    return topics
