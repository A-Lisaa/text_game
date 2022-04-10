from .event import Event


class EnterEvent(Event):
    def action(self):
        print("You entered Location")

    def trigger(self):
        return True


event_queue = [EnterEvent()]
for event in event_queue:
    if event.trigger():
        event.action()
