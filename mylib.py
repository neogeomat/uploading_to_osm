def convert(input): #this converts unicode object to string object in the decoded json file
    if isinstance(input, dict):
        return dict([(convert(key), convert(value)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def formhub_to_database_district(str):
	if(str == 'district_kathmandu'):
		str = 'KATHMANDU'
	return str

def formhub_to_database_vdc(str):
	if(str == 'vdc_kmc'):
		str = 'KMC'
	return str

def formhub_to_database_ward(str):
	return str