# Copyright (C) 2019  ZIJIAN JIANG

import gc
from collections import deque
from datetime import datetime
from typing import Any, Deque, Dict, Hashable, List, Optional

from lxml import etree


# ==========================================
#   Memory Utilities
# ==========================================
class LRUCacheItem:
    """Data structure of items stored in cache"""
    def __init__(self, key: Hashable, value: Any = None):
        self.__key = key
        self.value = value or key
        self.timestamp = datetime.now()

    def __eq__(self, other) -> bool:
        return self.key is other.key

    @property
    def key(self):
        return self.__key


class LRUCache:
    """A sample class that implements LRU algorithm"""
    def __init__(self, length: int):
        self.__length: int = length
        self.__hash: Dict[Hashable, Any] = {}
        self.__item_list: Deque[LRUCacheItem] = deque()

    def insert(self, item: LRUCacheItem):
        if item.key in self.__hash:
            self.rankup(item)
        else:
            if len(self.__item_list) == self.__length:
                lru_item = self.__item_list.pop()
                del self.__hash[lru_item.key]
                gc.collect()
            #!if
            self.__hash[item.key] = item
            self.__item_list.appendleft(item)

    def rankup(self, item: LRUCacheItem):
        item_index = self.__item_list.index(item)
        del self.__item_list[item_index]
        self.__item_list.appendleft(item)

    def get(self, key: Hashable) -> Optional[LRUCacheItem]:
        if key not in self.__hash:
            return None
        item = self.__hash[key]
        self.rankup(item)
        return item


# ==========================================
#   File Utilities
# ==========================================

def xml2tree(path: str) -> etree._Element:
    with open(path, "r", encoding="utf-8") as file:
        tree = etree.parse(file)
        
    root = tree.getroot()
    if not etree.iselement(root):
        raise Exception("error")
    return tree

def xml2file(root: etree._Element, path: str):
    with open(path, mode='wb') as file:
        parser = etree.XMLParser(encoding='utf-8',remove_blank_text=True)
        string = str(etree.tostring(root, pretty_print=True, encoding='unicode'))
        string = string.encode('utf-8')
        root = etree.XML(string, parser)
        output = b"<?xml version=\"1.0\" encoding=\"utf-8\"?>" + b"\n" + etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=False)
        file.write(output)

class XmlFilePuller:
    """Xml File Mannager for xml files and etrees and cache management
    """
    def __init__(self, *, cachesize: int):
        # CacheDict[fpath, etree]
        self.__lrucache: LRUCache = LRUCache(cachesize)
        
    def get(self, fpath: str) -> etree.ElementTree:
        item = self.__lrucache.get(fpath)
        if item:
            return item.value

        item = LRUCacheItem(fpath, xml2tree(fpath))
        self.__lrucache.insert(item)
        return item.value


class XmlElemPuller:
    """Xml Element Puller for elements with Guid quick finding
    """
    def __init__(self, xmlpuller: XmlFilePuller, *, cachesize: int):
        self.__xmlpuller = xmlpuller

        # CacheDict[fpath, Dict[lineno, etree._Element]]
        self.__lrucache: LRUCache = LRUCache(cachesize)
    
    def get(self, fpath: str, lineno: int) -> Optional[etree._Element]:
        item = self.__lrucache.get(fpath)
        if item:
            return item.value.get(lineno, None) # type: ignore
        
        lineno_elem_map = {}
        for elem in self.__xmlpuller.get(fpath).getroot().iter():
            elem_lineno: int = elem.sourceline
            lineno_elem_map[elem_lineno] = elem
        #!for
        item = LRUCacheItem(fpath, lineno_elem_map)
        self.__lrucache.insert(item)
        return item.value.get(lineno, None) # type: ignore
