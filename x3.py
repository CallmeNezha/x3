import itertools
from typing import List, Optional, Tuple, Any, Union
from lxml import etree

Xpath = str


def xml2tree(path: str) -> etree._Element:
    with open(path, "r", encoding="utf-8") as file:
        tree = etree.parse(file)
        
    root = tree.getroot()
    if not etree.iselement(root):
        raise Exception("error")
    return tree

def xml2file(root: etree._Element, path: str):
    with open(path, mode='w') as file:
        parser = etree.XMLParser(remove_blank_text=True)
        string = str(etree.tostring(root, pretty_print=True, encoding='unicode'))
        root = etree.XML(string, parser)
        output = str(etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8'))
        file.write(output)

class x3_group:
    ...
class x3:
    ...
class x3:
    def __init__(self, elem: etree._Element):
        self._elem = elem
    
    def selectall(self, selection: Xpath) -> x3_group:
        return x3_group([x3(x) for x in self._elem.xpath(selection)])
    
    def select(self, selection: Xpath, default: Any = None) -> Optional[x3]:
        child = next(iter(self._elem.xpath(selection)), default)
        if child is not None:
            return x3(child)
        else:
            return None
        
    def attrib(self, key, default=None) -> Optional[str]:
        return self._elem.get(key, default)

    def parent(self, selection: Optional[Xpath] = None) -> Optional[x3]:
        if selection is not None:
            return x3(next(self._elem.iterancestors(selection)))
        else:
            return x3(self._elem.getparent())

    def remove(self):
        self._elem.getparent().remove(self._elem)

    def getsourcefile(self) -> Tuple[str, int]:
        return (self._elem.base, self._elem.sourceline)

    def __getitem__(self, key: str) -> Any:
        if type(key) is str:
            return self._elem.attrib[key]
        else:
            raise TypeError("Key error")

    def __setitem__(self, key:str , item: Any):
        if type(key) is str:
            self._elem.attrib[key] = item
        else:
            raise TypeError("Key error")

    @property
    def tag(self) -> str:
        return self._elem.tag




class x3_group:
    def __init__(self, group: List[x3]):
        self._group = group

    #TODO: what if selection is None
    def select(self, selection: Xpath) -> x3_group:
        return x3_group([x.select(selection) for x in self._group])

    def selectall(self, selection: Xpath) -> x3_group:
        selects = [x.selectall(selection)._group for x in self._group]
        selects = list(itertools.chain.from_iterable(selects))
        return x3_group(selects)

    def parent(self, selection) -> x3_group:
        return x3_group([x.parent(selection) for x in self._group])
            
        
    def map(self, func) -> List[Any]:
        """
        In catagory theory map is transform into another catagory.. Out of x3 catagory
        """
        return [func(x3_elem) for x3_elem in self._group]

    def remove(self):
        for x in self._group:
            x.remove()

    def filter(self, func) -> x3_group:
        return x3_group([x3_elem for x3_elem in self._group if func(x3_elem)])

    def toarray(self) -> List[x3]:
        return self._group

    def __len__(self) -> int:
        return len(self._group)

    def __getitem__(self, index: int) -> x3:
        if type(index) is int:
            return self._group[index]
        else:
            raise TypeError("index error")
    
