# -*- coding: utf-8 -*-
from nltk.corpus import wordnet as wn

class SynsetProperties(object):
	"""docstring for SynsetProperties"""
	def __init__(self, synset):
		super(SynsetProperties, self).__init__()
		
		self.synset = synset
		self.reference_count = 0
		self.avg_depth = (self.synset.min_depth() + self.synset.max_depth()) / float(2)
	
	def increment_reference_count(self, synset_weight):
		self.reference_count += synset_weight

	#def __str__(self):
	#	return ("name: {}\n".format(self.synset.name()) +
	#			"reference_count: {}\n".format(self.reference_count) +
	#			"avg_depth: {}\n".format(self.avg_depth) +
	#			"definition: {}".format(self.synset.definition()))

	def __repr__(self):
		return self.synset.name()

class SynsetScorer(object):
	"""docstring for SynsetScorer"""
	def __init__(self):
		super(SynsetScorer, self).__init__()
		
		self.synset_dict = {}

	def _add_hypernym_path_synsetss(self, hypernym_path, synset_weight):
		for synset in hypernym_path:
			if synset.name() not in self.synset_dict:
				self.synset_dict[synset.name()] = SynsetProperties(synset)
			self.synset_dict[synset.name()].increment_reference_count(synset_weight)

	def add_hypernym_paths(self, synset, synset_weight=1):
		for hypernym_path in synset.hypernym_paths():
			self._add_hypernym_path(hypernym_path, synset_weight)

	def sort_synsets_by(self, key_func, reverse=True, display=False):
		sorted_synsets = sorted(self.synset_dict.values(), key=key_func, reverse=reverse)
		
		if display:
			for sp in sorted_synsets:
				print(sp)
				print('\n')

		return sorted_synsets

def main():
	scorer = SynsetScorer()

	dog_synsets = wn.synsets("dog")
	cat_synsets = wn.synsets("cat")
	mouse_synsets = wn.synsets("mouse")
	horse_synsets = wn.synsets("horse")

	dog = dog_synsets[0]
	cat = cat_synsets[0]
	mouse = mouse_synsets[0]
	horse = horse_synsets[0]

	scorer.add_hypernym_paths(dog)
	scorer.add_hypernym_paths(cat)
	scorer.add_hypernym_paths(mouse)
	scorer.add_hypernym_paths(horse)

	#print(sort_synsets_by(lambda synset: synset_dict[synset].reference_count))

	print(scorer.sort_synsets_by(lambda sp: sp.reference_count * sp.avg_depth))


if __name__ == '__main__':
	main()