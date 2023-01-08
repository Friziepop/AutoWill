from io import TextIOBase


class ColoredMultilineRedirector(TextIOBase):
    def __init__(self, color: str, multiline):
        self._multiline = multiline
        self.color = color

    def write(self, data):
        self._multiline.print(data, text_color=self.color)
