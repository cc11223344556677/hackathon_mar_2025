from langchain_core.prompts import HumanMessagePromptTemplate

def get_metadata_prompt():
    return HumanMessagePromptTemplate.from_template(
        "Classify the provided article content by assigning tags. "
        "Focus on assigning one to three tags that best describe the information from the article. "
        "If possible first assign one of the following tags: "
        "'financial crisis', 'sustainability', 'fake news', 'AI', "
        "'digitalization', 'local journalism', 'covid', 'demographics', 'innovation' "
        "If none of these tags fit, you can also provide your own tags. "
        "If you are unsure about the tags, you can also skip this task.\n "
        "Output the tags as a comma-separated list in the following format: "
        "'financial crisis, sustainability, AI' "
        "Article content: \n {article_text}"
    )
