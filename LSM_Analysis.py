from bs4 import BeautifulSoup
from bs4 import element
from functools import cache
from pprint import pprint

class LSM_Analysis:
    def __init__(self, path) -> None:
        self.path = path

        if path[-3:] == ".htm":
            raise TypeError("HTML only.")
        with open(path, "r", encoding='utf-8') as f:
            self._soup = BeautifulSoup(f.read(), "html.parser")
        if "アセット" not in self._soup.title.text:
            raise TypeError("LSM only.")

    @cache
    def failed_list(self):
        section = self._soup.select_one("body > section:nth-child(6)")
        failed_aseets = [elem.text for elem in section.find_all("a", attrs={"data-lomtag":"failed"})]
        return failed_aseets

    @cache
    def error_list(self):
        section = self._soup.select_one("body > section:nth-child(6)")
        tag = section.find_all("a", attrs={"data-lomtag":"warning"})

        error_aseets = list()
        warning_aseets = list()
        for i in tag:
            if len(warning_aseets) >= 1:
                warning_aseets.append(i.text)
            elif self.iserror(i):
                error_aseets.append(i.text)
            else:
                warning_aseets.append(i.text)
        return error_aseets

    def iserror(self, elem: element.Tag):
        parent = elem.find_parents("div")
        parent = parent[1].previous_siblings

        string = "".join(map(str, parent))
        # なぜかうまくいかない為、一回またsoupを作る
        soup = BeautifulSoup(string, "html.parser")
        text = [j.text for j in soup.find_all("h2")]
        return len(text) == 2

if __name__ == "__main__":
    loading = LSM_Analysis(input("PATH>>"))
    aseet = loading.error_list()
    pprint(aseet)
