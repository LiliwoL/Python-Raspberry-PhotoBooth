#!/usr/bin/env python
import pytumblr

consumer_key = 'dNIsilcQIb9DW7437WTAdt1oqgPJz5fp3xdGBpvxNYEI5pFNiA'
consumer_secret = '2FuEZr246XV4EiD0ZKTW5Z6NO78m09a03xQ1bojYfDJpa9E9cH'
token_key = 'lhFChO7YhjYTJyI2ob29eWb3Tcfau9FURgqo6VaCMtpoQQQPNV'
token_secret = 'y5wqIRtacPfRccxHipVE6MXaeo0e51C4M6hm1Z9TOK0cTeiys1'

client = pytumblr.TumblrRestClient( 
	consumer_key,
	consumer_secret,
	token_key, 
	token_secret
)

def uploadToTumblr( image ):

	client.create_photo(
		'oneideaperminute', 
		state="published",
		tags=["raspberry", "photobooth"], 
		data=image
	)
	return "uploaded"
