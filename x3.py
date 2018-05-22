

class x3:
	def __init__(self, elem):
		self._elem = elem
	
	def selectAll(self, selection):
		return x3_selection([x3_group([x3(x) for x in self._elem.iter(selection)])])

	def select(self, selection):
		return x3(next(self._elem.iter(selection)))
		
	def attrib(self, key, default=None):
		return self._elem.get(key, default)

	def parent(self, selection):
		return x3(next(self._elem.iterancestors(selection)))

class x3_selection:
	def __init__(self, groups):
		if False == isinstance(groups, list):
			raise Exception('Arg Error')
		self._groups = groups
	
	def select(self, selection):
		return x3_selection([x.select(selection) for x in self._groups])
	
	def selectAll(self, selection):
		new_groups = []
		for group in self._groups:
			new_groups += group.selectAll(selection)
		return x3_selection(new_groups)

	def _returnUniqueGroup(self):
		if len(self._groups) != 1:
			raise Exception('Call Error')
		return self._groups[0]


class x3_group:
	def __init__(self, group):
		self._group = group

	def select(self, selection):
		return x3_group([next(x._elem.iter(selection)) for x in self._group])

	def selectAll(self, selection):
		retval = []
		for x in self._group:
			x_seletion = x.selectAll(selection)
			unique_group = x_seletion._returnUniqueGroup()
			retval.append(unique_group)
		return retval
		
	def map(self, func):
		"""
		In catagory theory map is transform into another catagory.. Out of x3 catagory
		"""
		return [func(x3_elem) for x3_elem in self._group]
	
	def filter(self, func):
		return x3_group([x3_elem for x3_elem in self._group if func(x3_elem)])

	def toarray(self):
		return [x3_elem._elem for x3_elem in self._group]

def TEST():
	from lxml import etree
	root = etree.XML("""
	<a>
		<b id="1">
			<c id="11"><d id="111"/></c>
			<c id="12"><d id="121"/></c>
		</b>
		<b id="2">
			<c id="21"><d id="211"/></c>
			<c id="22"><d id="221"/></c>
		</b>
	</a>
	""" )
	ret = x3(root).select('a')
	ret = x3(root).selectAll('b')
	ret = ret.selectAll('c')
	ret1 = ret.selectAll('d') # different behavior
	ret2 = ret.select('d')    # different behavior
	ret
	
if __name__ == "__main__":
	TEST()