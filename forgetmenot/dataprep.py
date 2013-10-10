import soundcloud

def getData():
	# create client object with app credentials
	client = soundcloud.Client(client_id='4172958b52e31b5f1e0270600d02aa63',
	                           client_secret='d1f3656edbd4f2cdf10ced0dce112c4f',
	                           username = 'zunayed@gmail.com', 
	                           password = 'soundcloud718')

	page_size = 3000

	fav = client.get('/me/favorites/', limit=page_size)
	playlist = {}
	for track in fav:
		playlist[track.user['username']] = track.title

	return playlist