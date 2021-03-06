wpJson4Harp
===========

Author: Ethan J. Eldridge  
Website: ejehardenberg.github.io  

Python tool to migrate WP contents to JSON for use in [harp](http://harpjs.com/)


Current Features:

1. Creates JSON for Posts
2. Creates JSON for Comments
3. Creates JSON for Nav
4. Creates JSON for Pages
5. Creates .md files for the Posts
6. Creates .md files for the pages
7. If using the PULL_TYPES, will pull down entire wp_post table and convert it into usable _data.

To Run:

    Fill out the database credentials at the top of the file
    $python wp2json4harp.py 
    You'll now have an example.jade file, and a few directories with _data.json inside.

Once you've ran the script, you'll get folders for each of the _data.json files. This makes things a bit easier to coordinate, and you can see from the example jade file how you can access the information pulled from your blog.

It's pretty heavy on I/O from all the writes, but I pulled down a sizable wordpress database within a reasonable time (less than a minute) that had 347915 rows in the postmeta, and 34617 in the posts table, so it works alright. 

If you'd like to try it out:

1. Install [Wordpress](http://teamtreehouse.com/library/how-to-make-a-wordpress-blog/getting-started-with-wordpress/the-famous-5minute-wordpress-install-2)
2. Install [Harp](http://harpjs.com/)
3. Download this script
4. Configure it to your liking using the options below
5. Run the script!
6. Move the folders and files into your harp site area.

Some configuration details:

Configuration is at the top of the script, you'll need to enter your database credentials.
Optionally, you can fully configure the script using the constants below:

Configuration of Script
------------------------------------------------------------

<table>
	<thead>
		<tr>
			<th>Constant</th><th>What it does</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>MYSQL_HOST</td>
			<td>Defines the host of the database to connect to.</td>
		</tr>
		<tr>
			<td>MYSQL_USER</td>
			<td>Defines the user to connect to the database as</td>
		</tr>
		<tr>
			<td>MYSQL_PASS</td>
			<td>Defines the password to the database</td>
		</tr>
		<tr>
			<td>MYSQL_DB</td>
			<td>Defines the database name connected to on the host.</td>
		</tr>
		<tr>
			<td>WP_PREFIX</td>
			<td>The prefix to your wordpress tables, typically this is `wp_`</td>
		</tr>
		<tr>
			<td>ONLY_PUBLISHED</td>
			<td>Only retrieve posts and pages that have been published</td>
		</tr>
		<tr>
			<td>GENERATE_PAGES</td>
			<td>Generate a markdown file for the pages being pulled from the WP database. This will exist in the PAGES_DIR</td>
		</tr>
		<tr>
			<td>GENERATE_POSTS</td>
			<td>Generate a markdown file for the posts being pulled from the WP database. This will exist in the BLOG_DIR</td>
		</tr>
		<tr>
			<td>ROOT_DIR</td>
			<td>Where to generate all the files this script creates, leave empty by default for the area where the script is being ran</td>
		</tr>
		<tr>
			<td>ENCODING</td>
			<td>The encoding to decode the content from the database in, I've defaulted it to latin to handle some annoying unicode errors</td>
		</tr>
		<tr>
			<td>OUTPUT_ENCODING</td>
			<td>The encoding to encode the _data.json files in</td>
		</tr>
		<tr>
			<td>STRIP_NON_ASCII</td>
			<td>strips out non-ascii characters from data being written into _data.json</td>
		</tr>
		<tr>
			<td>PULL_TYPES</td>
			<td>Specify this to true and all post types will be pulled out of the database and _data files created for eachs, if you use this, then the *_DIR constants mean nothing.</td>
		</tr>
		<tr>
			<td>PAGES_DIR</td>
			<td>The directory name where the pages will be stored</td>
		</tr>
		<tr>
			<td>BLOG_DIR</td>
			<td>The directory name where the blog posts will be stored</td>
		</tr>
		<tr>
			<td>NAV_DIR</td>
			<td>The directory where the navigation json will be stored</td>
		</tr>
		<tr>
			<td>COMMENTS_DIR</td>
			<td>The directory where comments will be stored. </td>
		</tr>
		<tr>
			<td>EXAMPLE_FILE</td>
			<td>The name of the file that will be generated to show some of the posts and pages.</td>
		</tr>
		<tr>
			<td>STOP_ON_ERR</td>
			<td>Boolean value that causes errors to stop the script, </td>
		</tr>
	</tbody>
</table>

TODO: 

- Taxonomy?
- Add nav stuff to the PULL_TYPES area as well to help out with navigation
- How does one pull in the comments to a post?
- Use getopt to make cmd line arguments instead of constants
- More examples!


