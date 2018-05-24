from flask import Flask,render_template,request,redirect
import requests,time,json,os

app = Flask(__name__)

ESHOST = os.environ["ES_SERVICE_SERVICE_HOST"]
ESPORT = os.environ["ES_SERVICE_SERVICE_PORT"]
esurl = lambda x: f"http://{ESHOST}:{ESPORT}{x}"

def get_all_posts():
    r = requests.get(esurl("/posts/_search"))
    d = r.json()
    if "error" in d:
        print(d)
        r = requests.put(esurl("/posts"))
    r = requests.get(esurl("/posts/_search"))
    o = r.json()["hits"]["hits"]
    return o
    
def get_single_post(id):
    u = esurl(f"/posts/post/{id}")
    print(u)
    r = requests.get(u)
    d = r.json()
    print("get response",d)
    return d

def put_post(obj):
    print("posting obj")
    print(esurl("/posts/post"))
    r = requests.post(esurl("/posts/post"),data=json.dumps(obj),headers={"Content-Type": "application/json"})

    print("post response",r.json())

@app.route("/")
def index_route():
    d = get_all_posts()
    print(d)
    return render_template("index.html",data=d)

@app.route("/add",methods=["GET","POST"])
def add_post_route():
    if request.method == "POST":
        f = request.form
        put_post({
            "subject": f["subj"],
            "body": f["body"],
            "date": time.time()
        })
        return redirect("/")
    else:
        return render_template("add.html")

@app.route("/post/<id>")
def get_single_post_route(id):
    d = get_single_post(id)
    return render_template("single_post.html",data=d["_source"])

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")