# Morals - Todo

- [x] Use enum types for the responses from the moral engine, so that they can be compared. 
	1. A type of `AristotelianResponse` can be created with values of `Vicious` and `Virtuous`.
	2. Another type of `ContractualistResponse` can be created with values of `Impermissible` and `Permissible`
	3. These types are different ways of saying the same things, so that can be given the same values.
	4. Then those values can be compared.
- [x] Implement other moral engines to represent other philosophies
- [x] Create a class to represent the input
	1. Right now it's just taking a dictionary
	2. This dictionary is untyped
	3. This can create confusion as the project grows
- [ ] Create a resolution engine, to make decisions (provide guidance), when there are conflicts between the different schools of thought
- [x] Maybe add typing as project grows. Right now, typing is omitted, to make it easier to read for people who do not program.
	* I have a hard time using just dictionaries without types, because it just seems a mess to me
	* I like to have more clear and well defined types, just to avoid error.
- [x] Create new models:
	* Nieizschean
	* Rossian
	* Ethics of Care
- [ ] Could make more poetic or philosophical by adding axioms of truth that span across all philosophies.  This would basically be adding my own philosophy.  Currently it's summing up all philosophies, which is useful.
- [ ] Output context along with results.
- [ ] Provide output in markdown.
- [ ] Allow JSON input.

_Do good work, not evil.  Leave a positive impact upon society._
