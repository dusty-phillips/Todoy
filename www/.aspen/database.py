from mongoengine import connect

def startup(website):
    website.db = connect("todoy")