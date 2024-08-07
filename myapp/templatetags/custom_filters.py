from django import template

register = template.Library()

@register.filter
def status_class(status):
    positive_statuses = [
        'completed_interested', 'appointment_set', 'in_progress'
    ]
    neutral_statuses = [
        'not_contacted', 'completed_follow_up_needed', 'voicemail_left', 'call_back_later', 'no_answer'
    ]
    if status in positive_statuses:
        return 'card-positive'  # Green
    elif status in neutral_statuses:
        return 'card-neutral'  # Yellow
    else:
        return 'card-negative'  # Red

@register.filter
def dict_item(dictionary, key):
    """ Return the value for a given key in a dictionary """
    return dictionary.get(key, 0)