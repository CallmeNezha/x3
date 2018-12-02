__doc__ = r"""
#
#                                                    ==(W{==========-      /===-
#                                                      ||  (.--.)         /===-_---~~~~~~~~~------____
#                                                      | \_,|**|,__      |===-~___                _,-'
#                                         -==\\        `\ ' `--'   ),    `//~\\   ~~~~`---.___.-~~
#                                     ______-==|        /`\_. .__/\ \    | |  \\           _-~`
#                               __--~~~  ,-/-==\\      (   | .  |~~~~|   | |   `\        ,'
#                            _-~       /'    |  \\     )__/==0==-\<>/   / /      \      /
#                          .'        /       |   \\      /~\___/~~\/  /' /        \   /'
#                         /  ____  /         |    \`\.__/-~~   \  |_/'  /          \/'
#                        /-'~    ~~~~~---__  |     ~-/~         ( )   /'        _--~`
#                                          \_|      /        _) | ;  ),   __--~~
#                                            '~~--_/      _-~/- |/ \   '-~ \
#                                           {\__--_/}    / \\_>-|)<__\      \
#                                           /'   (_/  _-~  | |__>--<__|      |
#                                          |   _/) )-~     | |__>--<__|      |
#                                          / /~ ,_/       / /__>---<__/      |
#                                         o-o _//        /-~_>---<__-~      /
#                                         (^(~          /~_>---<__-      _-~
#                                        ,/|           /__>--<__/     _-~
#                                     ,//('(          |__>--<__|     /                  .----_
#                                    ( ( '))          |__>--<__|    |                 /' _---_~\
#                                 `-)) )) (           |__>--<__|    |               /'  /     ~\`\
#                                ,/,'//( (             \__>--<__\    \            /'  //        ||
#                              ,( ( ((, ))              ~-__>--<_~-_  ~--____---~' _/'/        /'
#                            `~/  )` ) ,/|                 ~-_~>--<_/-__       __-~ _/
#                          ._-~//( )/ )) `                    ~~-'_/_/ /~~~~~~~__--~
#                           ;'( ')/ ,)(                              ~~~~~~~~~~
#                          ' ') '( (/
#                            '   '  `
#                   )          )              
#               ( /(       ( /(     )        
#               )\())   (  )\()) ( /(     )  
#               ((_)\   ))\((_)\  )\()) ( /(  
#               _((_) /((_)_((_)((_)\  )(_)) 
#               | \| |(_)) |_  / | |(_)((_)_  
#               | .` |/ -_) / /  | ' \ / _` | 
#               |_|\_|\___|/___| |_||_|\__,_| 
#
#                                                /    \
#               _                        )      ((    ))     (
#              (@)                      /|\      ))_ ((     /|\
#              |-|                     / | \    (@ || @)   / | \                      (@)
#              | | -------------------/--|-voV---\`||'/--Vov-|--\---------------------|-|
#              |-|                         '^`   (o  o)  '^`                          | |
#              | |                               `\VV/'                               |-|
#              |-|                                                                    | |
#              | |       Create on 26/11/2018  All rights reserved by ZIJIAN JIANG    |-|
#              |-|                                                                    | |
#              | |                                                                    |-|
#              |_|____________________________________________________________________| |
#              (@)              l   /\ /         ( (        \ /\   l                `\|-|
#                               l /   V           \ \        V   \ l                  (@)
#                               l/                _) )_           \I
#                                                 `\ /'
#
#
#  ██████╗ ██╗   ██╗██╗██╗  ██╗ ██████╗ ████████╗███████╗   ██╗  ██╗██████╗ 
# ██╔═══██╗██║   ██║██║╚██╗██╔╝██╔═══██╗╚══██╔══╝██╔════╝   ╚██╗██╔╝╚════██╗
# ██║   ██║██║   ██║██║ ╚███╔╝ ██║   ██║   ██║   █████╗      ╚███╔╝  █████╔╝
# ██║▄▄ ██║██║   ██║██║ ██╔██╗ ██║   ██║   ██║   ██╔══╝      ██╔██╗  ╚═══██╗
# ╚██████╔╝╚██████╔╝██║██╔╝ ██╗╚██████╔╝   ██║   ███████╗██╗██╔╝ ██╗██████╔╝
#  ╚══▀▀═╝  ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝╚═╝  ╚═╝╚═════╝ 
"""
# Copyright (C) 2018  ZIJIAN JIANG

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or 
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import itertools
from typing import List, Optional, Tuple, Any, Union, cast
from lxml import etree
from collections import Sequence

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

class x3(Sequence):
    def __init__(self, elem: etree._Element):
        self._elem = elem
    
    def selectall(self, selection: Xpath) -> 'x3_group':
        return x3_group([x3(x) for x in self._elem.xpath(selection)])
    
    def select(self, selection: Xpath, default: Any = None) -> Optional['x3']:
        child = next(iter(self._elem.xpath(selection)), default)
        if child is not None:
            return x3(child)
        else:
            return None
        
    def attrib(self, key, default=None) -> Optional[str]:
        return self._elem.get(key, default)

    def parent(self, selection: Optional[Xpath] = None) -> Optional['x3']:
        if selection is not None:
            return x3(next(self._elem.iterancestors(selection)))
        else:
            return x3(self._elem.getparent())

    def remove(self):
        self._elem.getparent().remove(self._elem)

    def getsourcefile(self) -> Tuple[str, int]:
        return (self._elem.base, self._elem.sourceline)

    def __getitem__(self, key):
        if type(key) is str:
            return self._elem.attrib[key]
        elif type(key) is int:
            if key >= len(self):
                raise IndexError("index out of range")
            return x3(self._elem[key])
        else:
            raise TypeError("Key error")

    def __setitem__(self, key: Union[str, int], item: Any):
        if type(key) is str:
            self._elem.attrib[key] = item
        elif type(key) is int:
            if cast(int, key) >= len(self):
                raise IndexError("index out of range")
            self._elem[key] = item
        else:
            raise TypeError("Key error")

    def __len__(self) -> int:
        return len(self._elem)

    def __hash__(self):
        return hash(self._elem)
    
    def __eq__(self, other):
        if other is None and self._elem is None:
            return True
        if type(other) is not type(self):
            return False
        return self._elem is other._elem

    @property
    def tag(self) -> str:
        return self._elem.tag




class x3_group(Sequence):
    def __init__(self, group: List[x3]):
        self._group: List[x3] = group

    #TODO: what if selection is None
    def select(self, selection: Xpath) -> 'x3_group':
        group: List[x3] = list(filter(None.__ne__, iter(x.select(selection) for x in self._group)))
        return x3_group(group)

    def selectall(self, selection: Xpath) -> 'x3_group':
        selects = [x.selectall(selection)._group for x in self._group]
        selects_group = list(itertools.chain.from_iterable(selects))
        return x3_group(selects_group)

    def parent(self, selection) -> 'x3_group':
        group: List[x3] = list(filter(None.__ne__, iter(x.parent(selection) for x in self._group)))
        return x3_group(group)
            
        
    def map(self, func) -> List[Any]:
        """
        In catagory theory map is transform into another catagory.. Out of x3 catagory
        """
        return [func(x3_elem) for x3_elem in self._group]

    def remove(self):
        for x in self._group:
            x.remove()

    def filter(self, func) -> 'x3_group':
        return x3_group([x3_elem for x3_elem in self._group if func(x3_elem)])

    def toarray(self) -> List[x3]:
        return self._group

    def __len__(self) -> int:
        return len(self._group)

    def __getitem__(self, index):
        if type(index) is int:
            return self._group[index]
        else:
            raise TypeError("index error")
    
