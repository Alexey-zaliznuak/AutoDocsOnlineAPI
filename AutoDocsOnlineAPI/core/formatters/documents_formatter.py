from docx import Document
from io import BytesIO

# thanks
# https://github.com/ivanbicalho/python-docx-replace/blob/main/src/python_docx_replace/key_changer.py
class KeyChanger:
    def __init__(self, p, key, value) -> None:
        self.p = p
        self.key = key
        self.value = value
        self.run_text = ""
        self.runs_indexes = []
        self.run_char_indexes = []
        self.runs_to_change = {}

    def _initialize(self) -> None:
        run_index = 0
        for run in self.p.runs:
            self.run_text += run.text
            self.runs_indexes += [run_index for _ in run.text]
            self.run_char_indexes += [char_index for char_index, char in enumerate(run.text)]
            run_index += 1

    def replace(self) -> None:
        self._initialize()
        parsed_key_length = len(self.key)
        index_to_replace = self.run_text.find(self.key)

        for i in range(parsed_key_length):
            index = index_to_replace + i
            run_index = self.runs_indexes[index]
            run = self.p.runs[run_index]
            run_char_index = self.run_char_indexes[index]

            if not self.runs_to_change.get(run_index):
                self.runs_to_change[run_index] = [char for char_index, char in enumerate(run.text)]

            run_to_change = self.runs_to_change.get(run_index)  # type: ignore[assignment]
            if index == index_to_replace:
                run_to_change[run_char_index] = self.value
            else:
                run_to_change[run_char_index] = ""

        # make the real replace
        for index, text in self.runs_to_change.items():
            run = self.p.runs[index]
            run.text = "".join(text)


class DocumentsFormatter:
    def __init__(self, path, templates_values):
        self.document = Document(path)
        self.data = self.__get_primitive_templates_values(
            templates_values
        )

    def format(self) -> BytesIO:
        print(self.data)
        for p in self.all_paragraphs:
            for key, val in self.data.items():
                i = 0
                while key in p.text:
                    i += 1
                    print(f'iter - {i}')
                    KeyChanger(p, key, val).replace()

        file_stream = BytesIO()
        self.document.save(file_stream)

        file_stream.seek(0)

        return file_stream

    def __get_primitive_templates_values(self, templates_values):
        res = {}
        for tv in templates_values:
            res[tv.template.name_in_document] = tv.value
        return res

    @property
    def all_paragraphs(self):
        all_paragraphs = list(self.document.paragraphs)
        for t in self.document.tables:
            for row in t.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        all_paragraphs.append(paragraph)

        return all_paragraphs
