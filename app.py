from flask import Flask, render_template, request, jsonify
from werkzeug.serving import run_simple
from walk import get_tree, search_in_files, branch
from flask import Markup
import markdown

app = Flask(__name__)
app.debug = True
_dir = 'wiki'


# Context
@app.context_processor
def tree_context():
    tree = get_tree('wiki')

    return dict(tree=tree)

@app.route('/')
def main():
    return render_template('home.html')


@app.route('/<path:path>')
def view(path):
    text = ''
    with open(path) as file:
        text = Markup(markdown.markdown(file.read()))
    return render_template('page.html', page=path, text=text)

@app.route('/search')
def search():
    if request.args.get('q'):
        out = search_in_files('wiki', request.args.get('q'))
    return jsonify(out)

if __name__ == '__main__':
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)