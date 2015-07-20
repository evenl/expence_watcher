import csv
from datetime import date
import sys
import getopt
import numpy as np
import matplotlib.pyplot as plt

class Month():
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

class Watch_expences():
	def __init__(self, string):
		print "Watching " + string
		self.watch_string = string
		self.values                 = []
		self.number_of_transactions = 0
		self.watch_sum              = 0

	def check_expence(self, expence_string, value):
		if expence_string.find(self.watch_string) != -1:
			print "Adding expence " + str(value) + " to " + self.watch_string
			self.watch_sum += value
			self.values.append(value)
			self.number_of_transactions += 1

	def get_total(self):
		return self.watch_sum

	def get_values(self):
		tmp_val = self.values
		return tmp_val

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
		x = np.arange(1, len(watch.get_values())+1, 1)
		y = np.array(watch.get_values())
		y_mean = [np.mean(y) for i in x]

		z = np.polyfit(x, y, 1)
		p = np.poly1d(z)

		plt.plot(x,p(x),"r--")
		plt.plot(x, y, 'b-')
		plt.plot(x, y_mean, "g--")

		plt.ylabel(watch.watch_string)
		plt.show()

		print "Expence: " + watch.watch_string + " samples: " + str(len(watch.get_values())) + " Total: " + str(watch.get_total()) + " Avg/month: " + str(watch.get_total() / len(months)) + " Avg/expences: " + str(watch.get_average())
