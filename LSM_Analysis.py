from bs4 import BeautifulSoup
from bs4 import element

class LSM_Analysis:
    def __init__(self, path) -> None:
        self.path = path

        if path[-3:] == ".htm":
            raise TypeError("HTML only.")
        with open(path, "r", encoding='utf-8') as f:
            self._soup = BeautifulSoup(f.read(), "html.parser")
        if "アセット" not in self._soup.title.text:
            raise TypeError("LSM only.")

    def failed_list(self):
        section = self._soup.select_one("body > section:nth-child(6)")
        failed_aseets = [elem.text for elem in section.find_all("a", attrs={"data-lomtag":"failed"})]
        return failed_aseets

    def warning_list(self):
        section = self._soup.select_one("body > section:nth-child(6)")
        tag = section.find_all("a", attrs={"data-lomtag":"warning"})
        warning_aseets = list()
        for i in tag:
            if self.iserror(i):
                warning_aseets.append(i)
        return warning_aseets

    def iserror(self, elem: element.Tag):
        wtf = elem.find_parents("div")
        parent = wtf[1].previous_siblings
        string = ""

        #  h2タグのみを取得
        for j in parent:
            if type(j) is element.Tag:
                string = string + str(j)
        kenti = BeautifulSoup(string, "html.parser")
        text = [j.text for j in kenti.find_all("h2")]
        return len(text) == 2

if __name__ == "__main__":
    loading = LSM_Analysis(r"PATH")
    aseet = loading.warning_list()
    print(aseet)

