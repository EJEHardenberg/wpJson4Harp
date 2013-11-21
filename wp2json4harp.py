"""
Author: Ethan Joachim Eldridge
Website: ejehardenberg.github.io
Contact me through my github.
"""

MYSQL_HOST="localhost"
MYSQL_USER=""
MYSQL_PASS=""
MYSQL_DB  =""
WP_PREFIX = "wp_"

#Required: MySQLdb python module
#On Linux: python-mysqldb
#Windows: http://sourceforge.net/projects/mysql-python/files/
#Mac: http://stackoverflow.com/questions/1448429/how-to-install-mysqldb-python-data-access-library-to-mysql-on-mac-os-x#1448476
import MySQLdb

import sys
import calendar, datetime

def default(obj):
    """Default JSON serializer."""


    if not isinstance(obj, datetime.datetime):
    	return obj.__dict__
    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    
    	
    millis = int(
        calendar.timegm(obj.timetuple()) * 1000 +
        obj.microsecond / 1000
    )
    return millis

import json


class WP_Object(object):
	def to_JSON(self):
		return json.dumps(self, default=default, sort_keys=True, indent=4)


def databaseMigrate():
	#Verify database connection
	try:
		db = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASS,  db=MYSQL_DB)
		db.close()
	except Exception as err:
		print err
		print "Could not connect to database. Aborting..."
		sys.exit(1)

	db = MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASS,  db=MYSQL_DB)
	curs = db.cursor()

	curs.execute("SELECT p.ID, u.meta_value AS nickname , p.post_date_gmt, p.post_content, p.post_title, p.post_status, pm.meta_key, pm.meta_value, p.post_type from %(WP_PREFIX)sposts p LEFT JOIN %(WP_PREFIX)spostmeta pm ON p.ID=pm.post_id JOIN %(WP_PREFIX)susermeta u ON p.post_author=u.user_id WHERE u.meta_key='nickname' ORDER BY p.ID"  % globals())

	placeholder = WP_Object()
	setattr(placeholder,'ID',-1)
	posts = [placeholder]
	for row in curs.fetchall():
		if posts[-1].ID != row[0]:
			posts.append(WP_Object())
		setattr(posts[-1],'ID',row[0])
		setattr(posts[-1],'author',row[1])
		setattr(posts[-1],'date',row[2])
		setattr(posts[-1],'content',row[3])
		setattr(posts[-1],'title',row[4])
		setattr(posts[-1],'status',row[5])
		if row[6] and row[7]:
			setattr(posts[-1],row[6],row[7])
		setattr(posts[-1],'ptype',row[8])
	
	del posts[0] #Remove placeholder
	
	#Page posts result in pages to be made.
	p = open('_pagedata.json','w')
	b = open('_blogdata.json','w')
	pcount = 0
	bcount = 0
	totalPages = sum(map(lambda x: x.ptype == "page",posts))
	totalPosts = sum(map(lambda x: x.ptype == "post",posts))
	p.write('{')
	b.write('{')
	for post in posts:
		if post.ptype == "page":
			#Throw the id onto the string to ensure unique ness of the title
			p.write(" \"%s%d\" : %s " % (post.title, post.ID, post.to_JSON()) )
			if totalPages-1 != pcount:
				p.write(',')
			pcount+=1
		elif post.ptype == "post":
			b.write(" \"%s%d\" : %s " % (post.title, post.ID, post.to_JSON()) )
			if totalPosts-1 != bcount:
				b.write(',')
			bcount+=1
	p.write('}')
	b.write('}')
	p.close()
	b.close()

	sql = "SELECT c.comment_ID, c.comment_post_ID, c.comment_author, c.comment_author_email, c.comment_author_url, c.comment_date, c.comment_content, c.user_id, u.meta_value as nickname, cm.meta_key, cm.meta_value FROM %(WP_PREFIX)scomments c LEFT JOIN %(WP_PREFIX)scommentmeta cm ON c.comment_ID=cm.comment_id JOIN %(WP_PREFIX)susermeta u ON c.user_id in (u.user_id,0) WHERE u.meta_key='nickname' ORDER BY c.comment_post_ID " % globals()
	
	curs.execute(sql)
	placeholder = WP_Object()
	setattr(placeholder,'ID',-1)
	comments = [placeholder]
	for row in curs.fetchall():
		if comments[-1].ID != row[0]:
			comments.append(WP_Object())
		setattr(comments[-1],'ID',row[0])
		setattr(comments[-1],'post_ID',row[1])
		setattr(comments[-1],'author',row[2])
		setattr(comments[-1],'author_email',row[3])
		setattr(comments[-1],'author_url',row[4])
		setattr(comments[-1],'date',row[5])
		setattr(comments[-1],'content',row[6])
		setattr(comments[-1],'user_id',row[7])
		setattr(comments[-1],'nickname',row[8])
		if row[9] is not None and row[10] is not None:
			setattr(comments[-1],row[9]. row[10])
	del comments[0]

	c = open('_commentdata.json','w')
	c.write('{')
	for comment in comments:
		c.write("\"%d-%d-%d\" : %s" % (comment.post_ID, (comment.date - datetime.datetime(1970,1,1)).total_seconds(), comment.ID, comment.to_JSON()) )
	c.write('}')
	c.close()
	

		
if __name__ == "__main__":
	databaseMigrate()