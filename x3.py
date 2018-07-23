import itertools
import logging

from lxml import etree


def xml2tree(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = etree.parse(file)
        
    root = tree.getroot()
    if not etree.iselement(root):
        raise Exception("error")
    return tree

def xml2file(root, path):
    with open(path, mode='w') as file:
        parser = etree.XMLParser(remove_blank_text=True)
        string = str(etree.tostring(root, pretty_print=True, encoding='unicode'))
        root = etree.XML(string, parser)
        output = str(etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8'))
        file.write(output)
        logging.info('xml written to file: ' + file.name)
        

class x3:
    def __init__(self, elem):
        self._elem = elem
    
    def selectAll(self, selection):
        return x3_group([x3(x) for x in self._elem.iter(selection)])
    
    def select(self, selection):
        return x3(next(self._elem.iter(selection)))
        
    def attrib(self, key, default=None):
        return self._elem.get(key, default)

    def parent(self, selection):
        return x3(next(self._elem.iterancestors(selection)))

    def remove(self):
        self._elem.getparent().remove(self._elem)
        return None

    def getsourcefile(self):
        return (self._elem.base, self._elem.sourceline)

    def __getitem__(self, key):
        if type(key) is str:
            return self._elem.attrib[key]
        else:
            raise TypeError("Only accept str")

    def __setitem__(self, key, item):
        if type(key) is str:
            self._elem.attrib[key] = item
        else:
            raise TypeError("Only accept str")



class x3_group:
    def __init__(self, group):
        self._group = group

    def select(self, selection):
        return x3_group([next(x._elem.iter(selection)) for x in self._group])

    def selectAll(self, selection):
        selects = [x.selectAll(selection)._group for x in self._group]
        selects = list(itertools.chain.from_iterable(selects))
        return x3_group(selects)

    def parent(self, selection):
        return x3_group([x.parent(selection) for x in self._group])
            
        
    def map(self, func):
        """
        In catagory theory map is transform into another catagory.. Out of x3 catagory
        """
        return [func(x3_elem) for x3_elem in self._group]

    def remove(self):
        for x in self._group:
            x.remove()
        return None

    def filter(self, func):
        return x3_group([x3_elem for x3_elem in self._group if func(x3_elem)])

    def toarray(self):
        return [x3_elem._elem for x3_elem in self._group]

    def __len__(self):
        return len(self._group)

    def __getitem__(self, indices):
        if type(indices) is int:
            return self._group[indices]
        else:
            raise TypeError("Only accept int")
    
