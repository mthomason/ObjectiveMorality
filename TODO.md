# Morals - Todo

1. Use enum types for the responses from the moral engine, so that they can be compared. 
	1. A type of `AristotelianResponse` can be created with values of `Vicious` and `Virtuous`.
	2. Another type of `ContractualistResponse` can be created with values of `Impermissible` and `Permissible`
	3. These types are different ways of saying the same things, so that can be given the same values.
	4. Then those values can be compared.
2. Implement other moral engines to represent other philosophies
3. Create a class to represent the input
	1. Right now it's just taking a dictionary
	2. This dictionary is untyped
	3. This can create confusion as the project grows
4. Create a resolution engine, to make decisions (provide guidance), when there are conflicts between the different schools of thought
5. Maybe add typing as project grows. Right now, typing is omitted, to make it easier to read for people who do not program.
	* I have a hard time using just dictionaries without types, because it just seems a mess to me
	* I like to have more clear and well defined types, just to avoid error.
6. Create new models:
	* Nieizschean
	* Rossian
	* Ethics of Care
7. Could make more poetic or philosophical by adding axioms of truth that span across all philosophies.

_Do good work, not evil.  Leave a positive impact upon society._
