# CS50 - Network project
## Table of contents
- [Introduction](#introduction)
  * [Description and requirements](#description-and-requirements)
  * [Installation](#installation)
- [Implementation](#implementation)
  * [Models](#models)
    + [User Profile](#user-profile)
    + [Post](#post)
    + [Following](#following)
  * [Views](#views)
    + [index](#index)
    + [user_profile](#user-profile)
    + [like-dislike](#like-dislike)
    + [following-user-posts](#following)
    + [handle-following](#follow-unfollow)
    + [login_view](#login-view)
    + [logout_view](#logout-view)
    + [register](#register)
  * [Tests](#tests)

# Introduction
## Description and requirements
Using Python, JavaScript, HTML, and CSS, complete the implementation of a social network that allows users to make posts, follow other users, and *like* posts. 

All requirements can be viewed here: https://cs50.harvard.edu/web/2020/projects/4/network/

You must be registered to use options such as commenting, profile picture, following and so on.

## Installation
To set up this project on your computer:
1. Clone the project
2. Install all necessary dependencies
    ```python
        pip install -r requirements.txt
    ```
3. Make a migration
    ```python
        python manage.py migrate
    ```

# Implementation
## Models

### USER
Abstract django user
* get_following_user - return all followings
* is_like - is user like that post?
* is_dislike - is user dislike that post?

### User Profile
Contains User Model extension with additional fields.

Fields:
* name - user's name
* username - id of user

### Post 
Contains all post info.

Fields:
* user - who posted the post
* content - post's inner text
* date - post's publication date
* like - many to many with user
* dislike - many to many with user



### Following 
Contains all who follows who info.

Fields:
* user - user who is following
* user_followed - user who is being followed

## Views
### index
Here you can:
* View all posts
* Edit posts (if you are the post's creator; only for logged-in users)
* Like them (only for logged-in users)
* Create a new post (only for logged-in users)


### user_profile
(only for logged-in users)

Here you can:
* View all user's posts
* Edit posts (if you are the post's creator)
* Like them 
* Follow the user (if you are not this user)

### like - dislike
(only for logged-in users)

Controls all actions regarding liking:
* Add a new like (change like btn color)
* Add a new Dislike (change dislike btn color)
* toggle between like and dislikes

### following
(only for logged-in users)

Here you can:
* View all posts created by followed users
* Like them

### follow_unfollow
(only for logged-in users)

Controls following/unfollowing users (only POST method allowed).

### login_view
Controls logging in.

### logout_view
Controls logging out.

### register
Controls registration.
