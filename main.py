import csv
from datetime import date
import sys
import getopt

class Month:
	total_in     = 0
	total_out    = 0
	_date        = date(1980, 1, 1)

	def __init__(self, date):
		self._date = date

	def add_expence(self, value):
		self.total_out += value

	def add_income(self, value):
		self.total_in += value

	def get_month_name(self):
		return self._date.strftime('%B')

	def get_year(self):
		return self._date.year

class Watch_expences:
	watch_string           = ""
	watch_sum              = 0
	number_of_transactions = 0

	def __init__(self, string):
		self.watch_string = string

	def check_expence(self, expence_string, value):
		if expence_string.find(self.watch_string) != -1:
			self.watch_sum += value
			self.number_of_transactions += 1

	def get_total(self):
		return self.watch_sum

	def get_average(self):
		if self.watch_sum != 0:
			return self.watch_sum / self.number_of_transactions
		else:
			return 0;
def find_date(datestr):
	date_str = datestr.split(".")

	if date_str[0] == "Dato":
		return

	dt = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
	return dt

def make_real_number(num_str):
	num_str = num_str.replace('.','')
	num_str = num_str.replace(',','.')
	return num_str

def print_help():
	print "No help yet"
	sys.exit(0)

if __name__ == "__main__": 
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hs:")
	except getopt.GetoptError:
		print_help()

	watches = []

	for opt, arg in opts:
		if opt == '-h':
			print_help()
		elif opt in ("-s"):
			print "Adding expence watch: " + arg
			watches.append(Watch_expences(arg))

	with open("transaksjonliste.txt", "rb") as csvfile:
		trans = csv.reader(csvfile, delimiter=';')

		curmonth = 0
		months = []

		for row in trans:
			dt = find_date(row[0])

			if dt == None:
				continue

			if dt.month != curmonth:
				curmonth = dt.month
				m = Month(dt)
				months.append(m)

			if row[4] != "":
				months[-1].add_income(float(make_real_number(row[4])))
			elif row[3] != "":
				value = float(make_real_number(row[3]))
				months[-1].add_expence(value)

				for watch in watches:
					watch.check_expence(row[1], value)


	for month in months:
		print "Total in: " + str(month.total_in) + " total out " + str(month.total_out) + " for month: " + str(month.get_month_name()) + " year: " + str(month.get_year())


	for watch in watches:
		print "Watched expence: " + watch.watch_string + "	total expence: " + str(watch.get_total()) + "	average expence pr month: " + str(watch.get_total() / len(months)) + "	average expence pr number of expences " + str(watch.get_average())
