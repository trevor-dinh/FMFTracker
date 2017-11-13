import praw
from win10toast import ToastNotifier

class RedditPost:
	def __init__(self, title, url, subreddit):
		self.title = title.lower()
		self.url = url
		self.subreddit = subreddit.lower()
	def __str__(self):
		return "{} (posted to r/{})\n\t{}".format(self.title, self.subreddit, self.url)

def retrieve_all_hot(reddit_instance: "praw.Reddit instance", mfa=False):
	result = []
	for submission in reddit_instance.subreddit('frugalmalefashion').hot(limit=30):
		
		result.append(RedditPost(submission.title, submission.url, submission.subreddit.display_name))
	for submission in reddit_instance.subreddit('sneakerdeals').hot(limit=30):
		result.append(RedditPost(submission.title, submission.url, submission.subreddit.display_name))
	if mfa:
		for submission in reddit_instance.subreddit('malefashionadvice').hot(limit=30):
			result.append(RedditPost(submission.title, submission.url, submission.subreddit.display_name))
	return result


def filter_by_keywords(posts: [RedditPost], keywords: [str]):
	if len(keywords) == 0:
		return posts
	else:
		result = []
		print("Filtering posts by keywords (may take time): {}".format(keywords))
		for k in keywords:
			for p in posts:
				if k in p.title.split():
					result.append(p)
		return result

def live_search_filter(post: RedditPost, keywords: [str]):
	if len(keywords) == 0:
		return (post, True)
	for k in keywords:
		if k in post.title.split():
			return (post, True)
	return ("Did not satisfy query", False)

def retrieve_keywords():
	result = []
	while True: #convert this to function
		raw_input = input("Add keyword(s) to input (leave blank to QUIT): ")
		if raw_input == '':
			break
		else:
			result.append(raw_input)
	return result

def format_posts(posts: [RedditPost]):
	if DEBUG_TRACE:
		print(dir(posts[0]))

	counter = 1
	for p in posts: #convert this to function
		print("\n{}\t{}\n".format(counter, p))

		counter += 1

def run_live_search(reddit_instance):
	toaster = ToastNotifier()
	counter = 1
	for submission in reddit_instance.subreddit('frugalmalefashion').stream.submissions(pause_after=0):
		if submission is None:
			continue
		print('Found submission, checking post...')
		check_post = live_search_filter(RedditPost(submission.title, 
			submission.url, submission.subreddit.display_name), search_for)
		if check_post[1]:
			print("{}  {}".format(counter,check_post[0]))
			toaster.show_toast("FMFTracker", "New post: {}".format(check_post[0]))
		elif DEBUG_TRACE:
			print("{}  {}".format(counter,check_post[0]))
		counter+= 1

DEBUG_TRACE = True

if __name__ == '__main__':
	if DEBUG_TRACE:
		print("Loading PRAW Reddit instance...")
	reddit = praw.Reddit('FMFTracker') #FMFTracker is name of script
	if reddit.read_only and DEBUG_TRACE:
		print("Reddit API read only mode is ON")

	while True:
		try:
			include_mfa = bool(input("Include r/malefashionadvice? (Leave blank otherwise): "))
			
			if DEBUG_TRACE:
				
				print(include_mfa)
			break
		except NameError:
			print("Invalid input")

	if DEBUG_TRACE:
		print("Proceeding to retrieve posts; r/mfa included? {}".format(True if include_mfa else False))
	posts = []
	posts += retrieve_all_hot(reddit, include_mfa)
	search_for = retrieve_keywords()

	print("\n\n\n------Printing hottest posts for the freshest clothes------\n\n\n")

	posts = filter_by_keywords(posts, search_for)
	format_posts(posts)
	live_search = bool(input("Turn on livesearch for desired keyword(s), if any? (Leave blank otherwise): "))
	
	if live_search: #convert this to function
		print("Warning: some posts may be old. This is due to PRAW retrieving the last 100 submissions.")
		
		run_live_search(reddit)
		# toaster = ToastNotifier()
		# counter = 1
		# for submission in reddit.subreddit('frugalmalefashion').stream.submissions():
		# 	check_post = live_search_filter(RedditPost(submission.title, 
		# 		submission.url, submission.subreddit.display_name), search_for)
		# 	if check_post[1]:
		# 		print("{}  {}".format(counter,check_post[0]))
		# 		toaster.show_toast("New post: {}".format(post))
		# 	elif DEBUG_TRACE:
		# 		print("{}  {}".format(counter,check_post[0]))
		# 	counter+= 1
	print("\n---END OF SCRIPT---")


	# for submission in reddit.subreddit('frugalmalefashion+malefashionadvice').hot(limit=50):
	#     print(submission.title, submission.url)
	    #print(dir(submission))

	'''
	for submission in reddit.subreddit('all').stream.submissions():
		print(submission.title)
	'''