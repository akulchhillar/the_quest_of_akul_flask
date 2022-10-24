from flask import Flask,render_template,request,url_for,redirect,abort
import markdown
from bs4 import BeautifulSoup as soup
import httpx
import os, random

app = Flask(__name__)

def get_latest_article():
    url = "https://api.github.com/repos/akulchhillar/the_quest_of_akul/git/trees/main?recursive=1"
    r = httpx.get(url)
    path = r.json()["tree"][0]["path"]
    url2 = f'https://raw.githubusercontent.com/akulchhillar/the_quest_of_akul/main/{path}'
    r = httpx.get(url2)
    return r.text

def get_post(id):
    url = f'https://raw.githubusercontent.com/akulchhillar/the_quest_of_akul/main/{id}'
    r = httpx.get(url)
    return r.text

def get_all_posts():
    headings = list()
    url = "https://api.github.com/repos/akulchhillar/the_quest_of_akul/git/trees/main?recursive=1"
    r = httpx.get(url)
    tree = r.json()["tree"]
    for t in tree:
        if(t["path"].startswith('assests')==False):
            headings.append({"url":"post/?q="+t["path"],"title":" ".join(t["path"].split(" ")[:-1])})
    return headings

@app.route("/")
def hello_world():
    
    article = markdown.markdown(get_latest_article())
    ht = soup(article)
    heading = ht.h1
    meta_heading = heading.text
    ht.h1.decompose()
    img = "https://raw.githubusercontent.com/akulchhillar/the_quest_of_akul_flask/main/static/assests/transparent/"+random.choice(os.listdir(r".\static\assests\transparent"))
    
    return render_template('index.html',article=ht,meta_heading=meta_heading,img=img)

@app.route("/posts")
def posts():
    return render_template('posts.html',posts=get_all_posts())

@app.route("/post/",methods=['GET'])
def post():
    try:
        article = markdown.markdown(get_post(request.args.get('q')))
        ht = soup(article)
        heading = ht.h1
        meta_heading = heading.text
        ht.h1.decompose()
        img = "https://raw.githubusercontent.com/akulchhillar/the_quest_of_akul_flask/main/static/assests/transparent/"+random.choice(os.listdir(r".\static\assests\transparent"))
    except:
        abort(404,"nf")
    return render_template('post.html',article=ht,meta_heading=meta_heading,img=img)

@app.route("/about",methods=['GET'])
def about():
     return render_template('about.html')

@app.errorhandler(404)
def error(e):
    return render_template('404.html')

if __name__ =="__main__":
    app.run(debug=True)