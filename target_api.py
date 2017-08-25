# cmc
# accepts inbound monitoring requests
# updates sqlite3 db
# accepts inbound monitoring removal requests
from flask import Flask, abort, request 
import json
import sqlite3

app = Flask(__name__)
#!monitor sid hostname cellno 
@app.route('/monitor', methods=['POST']) 
def add_target():
    if not request.json:
        abort(400)
    print request.json
    r = request.json
    """ check method field is in the post request """
    if 'method' not in r:
        return "cool story bro, tell it again."
    """ check method is either add or remove, nothing else """
    if r['method'] not in ['add', 'remove']:
        return "thats definetly not where i parked my car."
    conn = sqlite3.connect('db/targets.db')
    c = conn.cursor()
    if r['method'] == 'add':
        """ check we aren't already tracking this machine for this requestor """
        c.execute("select cb_sid from targets where requestor_slack_name=? and cb_sid=?", (r['requestor'],r['sid']))
        if len(c.fetchall()) > 0:
            print c.fetchall()
            return "already tracking sid for this requestor"
        """ ok, its net new, add to the db, we gon' find you, we gon' git you.. """
        c.execute(
            "insert into targets (cb_sid, cb_hostname, requestor_slack_name, requestor_cellno, active) values (?, ?, ?, ?, 1)",
            (r['sid'], r['hostname'], r['requestor'], r['cell'])
        )
        conn.commit()
        return "Shazam!" 
    if r['method'] == 'remove':
        c.execute("select cb_sid from targets where requestor_slack_name=? and cb_sid=?", (r['requestor'],r['sid']))
        if len(c.fetchall()) > 0:
            c.execute("delete from targets where cb_sid=? and requestor_slack_name=?", (r['requestor'],r['sid']))
            conn.commit()
            return "Mischief managed."
        else:
            return "I have no eyes on that target."
    """ if all else fails, send their request back to them """
    return json.dumps(request.json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12287, debug=True)
