import json


class Mailbox(object):
    def __init__(self, issue, account, username, reason):
        self.issue = issue
        self.account = account
        self.username = username
        self.reason = reason


data = {'Appeal': [], 'Protest': [], 'Quit': []}
data2 = {'Money':[]}
money_items =['Projects','Client','Developer','Money_holds','Rating']
mail_items = ['Issue','Account','Username','Reason']
mail = ['Appeal','Protest','Quit']




data['Appeal'].append({
        'Issue': 'Appeal',
        'Account': 'Client ',
        'Username': 'WU' ,
        'Status' : 'Not Decided',
        'Reason': 'I should not be warned!',
    })
data['Appeal'].append({
        'Issue': 'Appeal',
        'Account': 'Client',
        'Username': 'Filler1' ,
        'Status' : 'Not Decided',
        'Reason': 'I should not be warned!',
    })
data['Appeal'].append({
        'Issue': 'Appeal',
        'Account': 'Client',
        'Username': 'Filler2' ,
        'Status' : 'Not Decided',
        'Reason': 'I should not be warned!',
    })
data['Protest'].append({
        'Issue': 'Protest',
        'Account': 'Client',
        'Username': 'Ted',
        'Status' : 'Not Decided',
        'Reason': 'Free me from the blacklist!',
    })

data['Protest'].append({
        'Issue': 'Protest',
        'Account': 'Client',
        'Username': 'Ted2',
        'Status' : 'Not Decided',
        'Reason': 'Free me from the blacklist!',
    })

data['Protest'].append({
        'Issue': 'Protest',
        'Account': 'Client',
        'Username': 'Ted3',
        'Status' : 'Not Decided',
        'Reason': 'Free me from the blacklist!',
    })

data['Quit'].append({
        'Issue': 'Quit',
        'Account': 'Client',
        'Username': 'Eric',
        'Status' : 'Not Decided',
        'Reason': 'I am tired from this project!',
    })
data['Quit'].append({
        'Issue': 'Quit',
        'Account': 'Client',
        'Username': 'Eric1',
        'Status' : 'Not Decided',
        'Reason': 'I am tired from this project!'
    })
data['Quit'].append({
        'Issue': 'Quit',
        'Account': 'Client',
        'Username': 'Eric2',
        'Status' : 'Not Decided',
        'Reason': 'I am tired from this project!'
    })


data2['Money'].append({
    'Projects': 'Test',
    'Client' : ' Ted',
    'Developer' : 'YC',
    'Money_holds' : 1500,
    'Rating' : '2'
})
data2['Money'].append({
    'Projects': 'Test1',
    'Client' : ' Ted1',
    'Developer' : 'YC1',
    'Money_holds' : 1500,
    'Rating' : '2'
})
data2['Money'].append({
    'Projects': 'Test2',
    'Client' : ' Ted2',
    'Developer' : 'YC2',
    'Money_holds' : 1500,
    'Rating' : '2'
})






with open('mailbox','w') as outfile:
    json.dump(data,outfile,indent=4)

