from flask import Flask , jsonify, request
app = Flask(__name__)

sample=[{'name':'mirra'},
        {'name':'amritha'},
        {'name':'balaji'}]

@app.route('/',methods=['GET'])
def test():
##    import time
    import datetime
##    
##    #time.sleep(30)
##
##    request.id
##    for loop
##        print (requestid , loopno);
##    
    return jsonify({'message':'It works',
                    'Datetime':datetime.datetime.now()})

@app.route('/ppl',methods=['GET'])
def getAll():
    return jsonify({'People':sample})

@app.route('/ppl/<string:name>',methods=['GET'])
def get1(name):
    langs=[pl for pl in sample if pl['name'] == name]
    return jsonify({'People':langs[0]})

@app.route('/lang',methods=['POST'])
def append1():
    temp = {'name': request.json['name']}
    sample.append(temp)
    return jsonify({'People':sample})

@app.route('/del/<string:name>',methods=['DELETE'])
def delt(name):
    langs=[pl for pl in sample if pl['name'] == name]
    sample.remove(langs[0])
    return jsonify({'People': sample})


@app.route('/ppl/script/<tag>',methods=['GET'])
def getscript(tag):
    temp = None
    temp2 = None
    if tag is "1":
        import script1
        temp = script1.a
        temp2 = script1.function1()
        
    elif tag is "2":
        import script2
        temp= script2.b
        temp2= script2.function2()
        
    return jsonify({"Value": temp, "Value2": temp2})

if __name__ == '__main__':
    app.run(port=8090,threaded=True)
