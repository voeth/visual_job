from flask import Flask,render_template,request,escape
from vsearch import search4letters
from view_log import log_request

app = Flask(__name__)

def search4letters(phrase:str,letters:str)->set:
    """return a set of the 'letters' found in 'phrase'."""
    return set(letters).intersection(set(phrase))

@app.route('/hello')
def hello_flask():
    return render_template('hello.html') # 函数的调用

@app.route('/')
@app.route('/entry')
def entry() -> 'html':
    return render_template('entry.html',
                           the_title='')

def log_request(req,res):
    with open("vsearch.log","a") as log:
        print(req.form,req.remote_addr,req.user_agent,res,file=log,sep='|')

@app.route('/search4',methods=['POST'])

def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase,letters))
    log_request(request,results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)

@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open("vsearch.log") as log:
        for line in log:  # 一行一行地读
           contents.append([])
           for item in line.split('|'):   # split可以让我们按照特定符号对句段进行拆分,生成一个列表
              contents[-1].append(escape(item))
    titles = ('Form Data','Remote_addr','User_agent','Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,)


if __name__ == '__main__':
    app.run(debug=True)
