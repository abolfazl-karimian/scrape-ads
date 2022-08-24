from pathlib import Path


class HandleHistory:
    __sync = "history.txt"
    __source = "history.txt"
    __filePointer = ''

    def save_new_items(self, contents):
        new_items = []
        lines = self.read_from_history(self.get_source()).split("\n")
        for content in contents:
            found = False
            for line in lines:
                if str(content) == str(line):
                    found = True
            if not found:
                print(content)
                self.__append_to_file(self.get_sync(), content)
                new_items.append(content)
        return new_items

    def read_from_history(self, source):
        content = self.__read_file(source)
        return content

    def __read_file(self, fileName):
        if Path(fileName).is_file():
            with open(fileName) as file:
                return file.read()
        else:
            with open(fileName, "w+") as file:
                return file.read()

    def __append_to_file(self, fileName, new_content):
        if Path(fileName).is_file():
            with open(fileName, 'a') as file:
                file.write(str(new_content) + "\n")

    def delete_from_history(self, items):
        self.__delete_from_file(items)

    def __delete_from_file(self, items):
        lines = self.read_from_history(self.get_source())
        linesNumber = len(items)
        with open(self.get_sync(), 'w') as file:
            file.writelines(lines[:-linesNumber])

    def get_sync(self):
        return self.__sync

    def set_sync(self, name):
        self.__sync = name

    def get_source(self):
        return self.__source

    def set_source(self, name):
        self.__source = name

    def get_filePointer(self):
        return self.__filePointer

    def set_filePointer(self, file):
        self.__filePointer = file

    def close_file(self):
        if self.get_filePointer().is_open():
            self.get_filePointer().close()
