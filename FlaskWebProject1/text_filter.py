from re import sub


class StringProcessor:
    SHIELDED_OPEN = '&lt'
    SHIELDED_CLOSE = '&gt'
    OPEN_HASH = hash('<')
    CLOSE_HASH = hash('>')
    CHANGED_TAG = "{}%s{}".format(OPEN_HASH, CLOSE_HASH)
    ALLOWED_TAGS = ["strong", "b", "i", "em", "small", "del"]

    def __init__(self):
        self.in_buffer = True
        self.buffer = ""
        self.tag_to_check = ""
        openings = ["<%s" % tag for tag in StringProcessor.ALLOWED_TAGS]
        closings = ["</%s" % tag for tag in StringProcessor.ALLOWED_TAGS]
        self.allowed_tags = openings + closings

    def shield(self, value):
        self._flush()

        for elem in value:
            if elem == '<':
                self._prepare_to_process_tag()
            elif elem == '>':
                self._process_tag()
                continue

            if self.in_buffer:
                self.buffer += elem
            else:
                self.tag_to_check += elem

        if self.tag_to_check:
            self.buffer += self.tag_to_check

        self.buffer = sub(str(StringProcessor.OPEN_HASH), '<', self.buffer)
        self.buffer = sub(str(StringProcessor.CLOSE_HASH), '>', self.buffer)

        return self.buffer

    def _flush(self):
        self.in_buffer = True
        self.buffer = ""
        self.tag_to_check = ""

    def _process_tag(self):
        if not self.tag_to_check:
            self.buffer += StringProcessor.SHIELDED_CLOSE
        elif self.tag_to_check in self.allowed_tags:
            self.buffer += StringProcessor.CHANGED_TAG % self.tag_to_check[1:]
        else:
            self.buffer += "%s%s%s" % (
                StringProcessor.SHIELDED_OPEN, self.tag_to_check[1:],
                StringProcessor.SHIELDED_CLOSE)
        self.in_buffer = True
        self.tag_to_check = ""

    def _prepare_to_process_tag(self):
        if not self.in_buffer:
            self.buffer += self.tag_to_check
            self.tag_to_check = ""
        self.in_buffer = False
