

def store_csv():
	'''
	'''
	f = file('contact.csv', 'w')
	res = ['NO,Name,Phone,Phone_1,Phone_2,Email\n']
	for i in file('contact.txt', 'r'):
		i = i.replace('\n', '').replace('intern', '')
		t = i.split(' ')
		while '' in t:
			t.remove('')
		temp = ''
		if len(t)==6:
			temp = ','.join(t)
		temp += '\n'
		res.append(temp)

	while '\n' in res:
		res.remove('\n')

	f.writelines(res)
	f.close()

def company_data():
	'''
	load company_data
	'''
	from pandas import read_csv as rc
	csv_data = rc('contact.csv')
	Email = csv_data['Email']
	name_lib_str = []
	for i in Email:
		name_lib_str.append(i.split('@')[0])
	# print name_lib_str
	return name_lib_str

name_lib_str = company_data()

if __name__ == '__main__':
	# store_csv()
	name_lib_str = company_data()
	for i in name_lib_str:
		print i
	