# IS211_FinalProject

Project: Blog Application

Along with the project requirements, I have also expanded it to:
-Allow multiple users / blogs
-Added permalinks to blog posts (visible when reading an individual post)
-Users can inactivate a post without deleting it
-Posts have categories

The site can be accessed via the initial URL http://127.0.0.1:5000/
From there, you have the choice of blogs to view (there are currently two). 
Clicking on a blog takes you to the Dashboard page where you can see the active posts. Clicking the login button and successfully logging in will allow access to advanced features on the login page.

The login status for each user is stored in the SQL table and resets every time program is loaded.

This program assumes one blog per user, and one category per post. The publish date automatically is recorded as date of publication.

The two logins to test are:

user: gwashington
pass: america

And

user: tedison
pass: electric