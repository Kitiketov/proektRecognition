class TabDetector():
    def __init__(self) -> None:
        self.mode = False

    def _count_tab(self,cords,start_poz,tab_size,nouse):
        new_list = []
        for line in cords:
            x = line[0][0]
            new_list.append((x-start_poz+nouse)//tab_size)
        return new_list

    def _tab_size(self,cords,start_poz,nouse):
        _tab_size = -1
        for line in cords:
            x = line[0][0]
            if _tab_size == -1 and x-start_poz not in range(nouse):
                _tab_size = x-start_poz 
            elif x-start_poz not in range(nouse):
                _tab_size = min(x-start_poz,_tab_size)
        return _tab_size
    
    def add_tab(self,text,tab_count):
        new_text = ''
        for line,tab in zip(text.split('\n'),tab_count):
            new_text += '  ' * tab + line +'\n'
        return new_text

    def tab_definition(self, cords):
        sorted_cords = sorted(cords,key=lambda x: x[0][0])
        nouse = (sorted_cords[0][2][1] - sorted_cords[0][0][1])//2
        start_poz = sorted_cords[0][0][0]
        tab_size = self._tab_size(sorted_cords,start_poz,nouse)
        tab_count = self._count_tab(cords,start_poz,tab_size,nouse)

        print(start_poz,nouse,tab_size)
        return tab_count

    def switch_mode(self):
        self.mode = not self.mode
        return self.mode
            
if __name__ == "__main__":
    cords = [[[123, 166], [611, 166], [611, 204], [123, 204]],[[187, 319], [485, 319], [485, 355], [187, 355]],[[247, 356], [721, 356], [721, 395], [247, 395]],[[309, 584], [779, 584], [779, 623], [309, 623]]]
    t = TabDetector()
    print(t.tab_definition(cords))