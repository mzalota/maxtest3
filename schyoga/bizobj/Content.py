
class Content:
    def __init__(self, content_set):
        self.content_set = content_set

    def description_from_site(self):

        result = []
        for content_item in self.content_set:
            if content_item.category == 'studio-site':
                result.append(content_item)

        return result
