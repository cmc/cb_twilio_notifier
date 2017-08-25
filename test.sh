curl -vvv -i -H "Content-Type: application/json" -X POST -d '{"sid":"62919","hostname":"rando_dell","requestor":"cmc1","cell":"+16505186084", "method":"add"}' http://localhost:12287/monitor
curl -vvv -i -H "Content-Type: application/json" -X POST -d '{"sid":"66","hostname":"cmc-666-laptop","requestor":"cmc11","cell":"+16505186084", "method":"remove"}' http://localhost:12287/monitor
