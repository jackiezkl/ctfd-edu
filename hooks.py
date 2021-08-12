from sqlalchemy.event import listen
from CTFd.models import Solves, db
from CTFd.schemas.notifications import NotificationSchema
from flask import current_app, request

def on_challenge_solve(mapper, conn, solve):
  print("mapper: ", mapper)
  print("conn: ", conn)
  print("solve: ", solve)
  
  req = "{'title': 'challenge solved', 'content': 'one of the challenge is solved by xxx', 'type': 'alert', 'sound': True)"
  schema = NotificationSchema()
  result = schema.load(req)
  
  db.session.add(result.data)
  db.session.commit()
  
  response = schema.dup(result.data)
  
  notif_type = req.get("type","alert")
  notif_sound = req.get("sound",True)
  response.data["type"] = notif_type
  response.data["sound"] = notif_sound
  
  current_app.events_manaager.publish(data=response..data, type="notification")
  return{"success":True, "data": response.data}

def load_hooks():
  listen(Solves, "after_insert", on_challenge_solve)
