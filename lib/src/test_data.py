# __package__ = 'src'
# from . import prank

### construct test data. should make it easy for future expand 
# test---name
name_lib_str = ['david','weng','john','babala','charles','kevin','ethen',
				'G.G','max','bee','brain','gates','jobs','abama','albert',
				'adam','alan','alexander','barton','barlow','berton','chad',
				'carl','clare','colin','dean','devin','duke','felix','helen']

# test-education
school = []
for i in range(100):
	school.append('school-'+str(i))

# test-degree
degree = ['BS','MS','PHD']

# test-birth: just for test, leave this bug along
year = xrange(1950, 2015)
month = xrange(1, 13)
day = xrange(1, 32)

# test-gender
gender = ['man','woman']

# test-location
location = ['beijing','shanghai','shenzheng','hongkong',
			'guizhou','nanjing','qingdao','chongqing',
			'hangzhou','guiling','taiwan','zhejiang']

# test-field-and-skill
field_skill = {} 
temp = ['finance','computer science','marketing','sale',
		 'infrastructure','manufacture']
for i in range(len(temp)):
	field_skill[temp[i]] = []
	for j in range(10):
		field_skill[temp[i]].append(temp[i]+'-skill-'+str(j)) 

# test-hobby
hobby = []
for i in range(30):
	hobby.append('hobby-'+str(i))

if __name__ == '__main__':
	print 'dd'
	print 'ee'
	# __package__ = 'src.test_data'
	print __name__
	print __package__

	