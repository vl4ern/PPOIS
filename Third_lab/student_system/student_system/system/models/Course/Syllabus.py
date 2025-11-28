class Syllabus:
    def __init__(self, summary: str, topics: list):
        self.summary = summary
        self.topics = topics

    def topic_count(self):
        return len(self.topics)