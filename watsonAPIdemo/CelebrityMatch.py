import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights


def analyze(handle):
    twitter_consumer_key = 'SQJlKR8ou3IAL8OGSlZwWBXVq'
    twitter_consumer_secret = 'CZHwDGRURo1EWTOISJwlf9HNpfoxHwstRfo7XxzersOBg0zr8g'
    twitter_access_token = '817229625948590084-lIHZ3w9XfS5OsEew9yCYT1nNxad6zTd'
    twitter_access_secret = '8yifgI2Wfsi9bmlZTpKiqm4ASCjUYxcwxNiMvxQ0jlx6a'

    twitter_api = twitter.Api(consumer_key = twitter_consumer_key, consumer_secret = twitter_consumer_secret,
                              access_token_key = twitter_access_token, access_token_secret = twitter_access_secret)

    statuses = twitter_api.GetUserTimeline(screen_name = handle, count = 200, include_rts = False)

    text = ""

    for status in statuses:
        text += status.text

    # The IBM Bluemix credentials for Personality Insights!
    pi_username = '69ff47f4-5bf2-4dd1-898c-323ad0dc3660'
    pi_password = 'TBDR4cAKhiRn'

    personality_insights = PersonalityInsights(username = pi_username, password = pi_password)

    pi_result = personality_insights.profile(text)
    return pi_result


def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                            data[c3['id']] = c3['percentage']
    return data


def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
            compared_data[keys] = abs(dict1[keys] - dict2[keys])
    return compared_data


user_handle = "@Codecademy"
celebrity_handle = "@IBM"

user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

user = flatten(user_result)
celebrity = flatten(celebrity_result)

compared_results = compare(user, celebrity)

sorted_result = sorted(compared_results.items(), key = operator.itemgetter(1))

for keys, value in sorted_result[:5]:
    print(keys),
    print(user[keys]),
    print('->'),
    print(celebrity[keys]),
    print('->'),
    print(compared_results[keys])