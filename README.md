target_api.py - 

creates a flask api endpoint which accepts POST's at /monitor/, tracks monitoring requests in sqlite3 db.
            
               fields required:
                     sid (carbonblack sensor id)
                     hostname (can be anything, its what you know this machine/case by)
                     requestor_slack_name (your nick, passed by irbot by default)
                     requestor_cell (where you want to be notified, must be a cell #)
                     method - this can be 'add' or 'remove'

target_monitor.py - 

uses python scheduler, checks in with CB api every 15m and checks all monitoring targets within the sqlite3 db. If one is found to be online, it sends an SMS. You will continue to get SMS every 15m for as long as this machine remains online.

Example curl commands to interact w/ monitoring endpoint:

add a target for monitoring -

curl -vvv -i -H "Content-Type: application/json" -X POST -d '{"sid":"62919","hostname":"rando_dell","requestor":"cmc1","cell":"+16505186084", "method":"add"}' http://localhost:12287/monitor


remove a target for monitoring -

curl -vvv -i -H "Content-Type: application/json" -X POST -d '{"sid":"66","hostname":"cmc-666-laptop","requestor":"cmc11","cell":"+16505186084", "method":"remove"}' http://localhost:12287/monitor

irbot commands (todo) -

!notify <sid> <hostname> <cell>

!unnotify <sid> <hostname> <cell>
