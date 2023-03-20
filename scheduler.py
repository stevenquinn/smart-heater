import json
import datetime


class Scheduler:

    def __init__(self):

        self.file = 'schedule.json'
        self.schedule_ran_today = False


    def get_schedule(self):

        with open(self.file, 'r') as f:
            return json.load(f)


    def set_schedule(self, request, schedule):

        with open(self.file, 'w') as f:
            json.dump(schedule, f)

        
    def has_schedule(self):

        return self.get_schedule() is not None


    def set_ran_today(self, ran_today = True):
            
        self.schedule_ran_today = ran_today

    
    def should_reset(self):

        day_of_week = datetime.today().weekday()
        hour = datetime.today().hour
        minutes = datetime.today().minute
        current_minutes = hour * 60 + minutes
        schedule = self.get_schedule()
        current_schedule = schedule[day_of_week]
        off = current_schedule['off']
        off_minutes = off['hour'] * 60 + off['minute']

        return current_minutes >= off_minutes and self.schedule_ran_today


    def should_turn_on(self):

        if self.schedule_ran_today:
            return False

        day_of_week = self.get_day_of_week_name(datetime.today().weekday())
        hour = datetime.today().hour
        minutes = datetime.today().minute
        current_minutes = hour * 60 + minutes
        schedule = self.get_schedule()
        current_schedule = schedule[day_of_week]
        on = current_schedule['on']
        on_minutes = on['hour'] * 60 + on['minute']
        off = current_schedule['off']
        off_minutes = off['hour'] * 60 + off['minute']

        return current_minutes >= on_minutes and current_minutes < off_minutes


    def get_day_of_week_name(self, day_of_week_index):

        day_of_week_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        return day_of_week_names[day_of_week_index]
        




