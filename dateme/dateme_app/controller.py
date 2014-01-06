#from datetime import date, datetime, time
import datetime
from dateme_app import models
from dateme_app.serializers import *
import random

# shamelessly stolen from http://stackoverflow.com/questions/2217488/age-from-birthdate-in-python/2259711#2259711
def calculate_age(born):
    born = born.date()
    today = datetime.date.today()
    try: 
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


def get_messages(user, lastTime, num_messages, status):

    # TODO: should lastTime variable
    
    status["success"] = False
    messages = models.Message.objects.filter(sender=user).order_by('timestamp')
    
    if num_messages:
        messages = messages[:num_messages]
    status["data"]["messages"] = messages
    status["success"] = True

    return status

def add_message(user, message, status):

    # TODO: this needs a lot more work to handle the different content types
    #       for now this should work for text

    try:
        status["success"] = False

        # create the message object to be saved to database
        m = models.Message(
            contentType = models.ContentType.objects.get(pk=message.contentType.id),
            sender = user,
            value = message.value,
            conversation = models.Conversation.objects.get(pk=message.conversation.id)
        )

        # if m.contentType.name is 'Challenge':
        #     m.messagechallenge_set.create(
        #         challenge=models.Challenge.objects.get(value=message.value),
        #         isComplete=False
        #     )

            # mc.save()
        
        # save message object to the database
        m.save()
        
        if m.contentType.name == "Challenge":
            m.messagechallenge_set.create(
                challenge=models.Challenge.objects.get(value=message.value),
                isComplete=False
            )

        # assume it works and return success and the data we just saved
        # it probably doesn't need to return the data we saved as it is just overhead...
        status["data"]["messages"] = [m]
        status["success"] = True

    except Exception as e:
        status["exception"] += str(e)
        status["error"] += "\nThere was an issue."


    return status

def save_person(user, person, status):
    
    status["success"] = False
    
    # update the person object in the database
    m = models.Person.objects.get(username=user)
    person.pk = m.pk
    
    # save person object to the database
    person.save()
    
    # set success
    status["success"] = True

    return status
    
def get_person(user, status):

    status["success"] = False

    # get current person object from database
    m = models.Person.objects.get(username=user)
    
    # return person object and set success
    status["data"]["person"] = m
    status["success"] = True

    return status

def complete_challenge(user, challenge, status):

    status["success"] = False

    mc = models.MessageChallenge.objects.select_related('message__conversation').get(message__pk=challenge.message.pk, challenge__pk=challenge.challenge.pk, user=user)
    challenge.pk = mc.pk
    challenge.isComplete = True
    challenge.save()

    # update the level they are authorized for if they have completed all the ones at a level
    # TODO: this should only work if all sides have completed the challenge
    level_up = True
    conversation_id = mc.message.conversation.pk
    mcs = models.MessageChallenge.objects.filter(message__conversation__pk=conversation_id).values_list('challenge__pk', flat=True).order_by('challenge__pk')
    challenges = models.Challenge.objects.filter(level=mc.message.conversation.level)
    for challenge in challenges:
        if challenge.pk not in mcs:
            level_up = False

    if level_up:
        conversation = models.Conversation.objects.get(pk=conversation_id)
        conversation.level += 1
        conversation.save()

    status["success"] = True

    return status
    
def match(user, status):

    status["success"] = False
    
    #calculate the birthdate ranges
    old_date = datetime.date.today() - datetime.timedelta(days=user.age_end*365.24)
    young_date = datetime.date.today() - datetime.timedelta(days=user.age_start*365.24)
    your_age = calculate_age(user.birthday)

    # Retrieve users fitting criteria:
    # Exclude yourself
    people = models.Person.objects.exclude(username__iexact=user.username)
    # Exclude users who are too young or too old
    people = people.exclude(birthday__lte=old_date).exclude(birthday__gte=young_date)
    # Exclude users who think YOU are too young or too old
    people = people.exclude(age_start__gte=your_age).exclude(age_end__lte=your_age)
    # Get users with appropriate orientation
    people = people.filter(orientation__name__contains=user.gender.name).filter(gender__in=user.orientation.all())
    
    #If 5 or more people match the user's criteria, pick 5 random people; else, just pull the people who actually fit criteria
    match_five = random.sample(people, min(5, people.count()))
    print match_five
        
    #setup data for return to JSON
    status["success"] = True
    status["data"]["people"] = match_five
    print status
    return status

def get_photos(user, status):
    
    status["success"] = False

    # retrieve photos from user
    # this should probably be ordered by time
    photos = models.PhotoLink.objects.filter(user=user)
    # photos = models.PhotoLink.objects.filter(user=user).order_by('timestamp')
    
    status["data"]["photos"] = photos
    status["success"] = True

    return status

def set_photos(user, photos, status):
    
    status["success"] = False
    
    # update the photo object in the database
    # I can't figure out how to update multiple objects, so we'll just delete them for now
    # and then save the new photos
    m = models.PhotoLink.objects.filter(user=user).delete()
    
    # save photo object to the database
    photos.save()
    
    # set success
    status["success"] = True

    return status