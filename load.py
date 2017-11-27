import csv


# Global variables to avoid typing lots of strings later
q = 'q'
w = 'w'
a = 'a'
t = 't'

courses_to_q = dict()


def helper(s):
	print "S is {}".format(s)
	if len(s) == 0:
		return None
	else:
		return float(s)


def store(filename):
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter = ",")
		first = True

		for row in reader:
			if first:
				first = False
				continue
			course = row[0]
			courses_to_q[course] = dict()
			courses_to_q[course][q] = helper(row[2])
			courses_to_q[course][w] = helper(row[3])
			courses_to_q[course][a] = helper(row[4])
			courses_to_q[course][t] = row[5]
		print courses_to_q

store('courses.csv')
			
