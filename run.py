from flaskr import app
#premesteno ovde zbog komplikacija sa cirularnim pokretanjem
#pokretanje
if __name__ == '__main__':
    app.run(debug=True)